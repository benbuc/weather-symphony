import asyncio
import datetime
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse

from weather_symphony.main import get_mido

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return FileResponse("./demo/index.html")


@app.get("/api/")
async def api():
    def progressReportPacket(step_name, progress=None):
        return json.dumps({"step": step_name, "progress": progress}) + "\n\n"

    async def iterfile():
        yield progressReportPacket("Call Weather API", progress=None)
        await asyncio.sleep(0.5)
        yield progressReportPacket("Generate MIDI", progress=None)
        get_mido(datetime.date.today(), 0)  # TODO
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
