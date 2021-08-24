import asyncio
import json
import os.path
from datetime import date

from aiohttp import ClientError, ClientSession, ClientTimeout, DummyCookieJar
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse

from demo.open_weather_api import get_weather_data
from weather_symphony.main import get_mido

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session: ClientSession = None


@app.on_event("startup")
async def startup_event():
    timeout = ClientTimeout(connect=4, total=16)
    cookie_jar = DummyCookieJar()
    global session
    session = await ClientSession(timeout=timeout, cookie_jar=cookie_jar).__aenter__()


@app.on_event("shutdown")
async def shutdown_event():
    await asyncio.sleep(0)
    global session
    if session is not None:
        await session.__aexit__(None, None, None)
        session = None


@app.get("/")
async def root():
    return FileResponse("./demo/index.html")


@app.get("/api/")
async def api(
    date_string: str = Query(..., regex="^\\d{4}-\\d{2}-\\d{2}$"),
    latitude: str = Query(
        ...,
        regex="^(\\+|-)?(?:90(?:(?:\\.0{1,8})?)|(?:[0-9]|[1-8][0-9])(?:(?:\\.[0-9]{1,8})?))$",  # noqa: E501
    ),
    longitude: str = Query(
        ...,
        regex="^(\\+|-)?(?:180(?:(?:\\.0{1,8})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\\.[0-9]{1,8})?))$",  # noqa: E501
    ),
    seed: str = Query(0, max_length=64),
    apiKey: str = Query(..., regex="^[0-9a-f]{32}$"),
):
    latitude: float = round(float(latitude) * 1000) / 1000
    longitude: float = round(float(longitude) * 1000) / 1000
    date_obj = date.fromisoformat(date_string)

    def progressReportPacket(step_name, progress=None, from_cache=False, failed=False):
        return (
            json.dumps(
                {
                    "step": step_name,
                    "progress": progress,
                    "cached": from_cache,
                    "failed": failed,
                }
            )
            + "\n\n"
        )

    async def iterfile():
        yield progressReportPacket("Call Weather API", progress=None)
        global session
        filename = f"cache/{latitude}_{longitude}_{date}.json"
        if os.path.isfile(filename):
            print("request cached=", filename)
            yield progressReportPacket(
                "Call Weather API", progress=100, from_cache=True
            )
        else:
            try:
                await get_weather_data(
                    session, filename, date, latitude, longitude, apiKey
                )
            except ClientError as ex:
                print("api call failed=", ex)
                yield progressReportPacket(
                    "Call Weather API", progress=None, failed=True
                )
                return
        yield progressReportPacket("Generate MIDI", progress=None)
        get_mido(date_obj, 0)  # TODO
        await asyncio.sleep(1.5)
        yield progressReportPacket("Convert to audio", progress=0)
        await asyncio.sleep(1.5)
        yield progressReportPacket("Convert to audio", progress=50)
        await asyncio.sleep(1.5)
        yield progressReportPacket("Convert to audio", progress=100)

    return StreamingResponse(iterfile(), media_type="text/plain")


# with tempfile.NamedTemporaryFile(mode="w+b", suffix=".png", delete=False) as FOUT:
#     FOUT.write(img)
#     return FileResponse(FOUT.name, media_type="image/png")
