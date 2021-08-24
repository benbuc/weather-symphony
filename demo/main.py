import asyncio
import json
import tempfile
from asyncio import create_subprocess_exec, subprocess
from datetime import date
from pathlib import Path

from aiohttp import ClientError, ClientSession, ClientTimeout, DummyCookieJar
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from mido import MidiFile

from demo.open_weather_api import write_weather_data
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
cache_path: Path = Path("cache")


@app.on_event("startup")
async def startup_event():
    timeout = ClientTimeout(connect=4, total=16)
    cookie_jar = DummyCookieJar()
    global session
    session = await ClientSession(timeout=timeout, cookie_jar=cookie_jar).__aenter__()
    cache_path.mkdir(exist_ok=True)


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
    date_string: str = Query(..., alias="date", regex="^\\d{4}-\\d{2}-\\d{2}$"),
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
    date_obj: date = date.fromisoformat(date_string)

    def progressReportPacket(
        step_name, progress=None, from_cache=False, failed=False, filename=None
    ):
        return (
            json.dumps(
                {
                    "step": step_name,
                    "progress": progress,
                    "cached": from_cache,
                    "failed": failed,
                    "filename": filename,
                }
            )
            + "\n\n"
        )

    async def iterfile():
        filename = f"{latitude}_{longitude}_{date_obj}"

        # Call Weather API ------------------------------------------
        yield progressReportPacket("Call Weather API", progress=None)
        global session
        json_weather_data_file: Path = cache_path / f"{filename}.json"
        if json_weather_data_file.exists():
            print("API cache hit=", json_weather_data_file)
            yield progressReportPacket(
                "Call Weather API",
                progress=100,
                from_cache=True,
                filename=f"{filename}.json",
            )
        else:
            try:
                await write_weather_data(
                    session,
                    json_weather_data_file,
                    date_obj,
                    latitude,
                    longitude,
                    apiKey,
                )
                yield progressReportPacket(
                    "Call Weather API", progress=100, filename=f"{filename}.json"
                )
            except ClientError as ex:
                print("API call failed=", ex)
                yield progressReportPacket("Call Weather API", failed=True)
                return

        # Generate MIDI ---------------------------------------------
        yield progressReportPacket("Generate MIDI", progress=None)
        midi_data_file: Path = cache_path / f"{filename}.midi"
        if midi_data_file.exists():
            print("MIDI cache hit=", midi_data_file)
            yield progressReportPacket(
                "Generate MIDI",
                progress=100,
                from_cache=True,
                filename=f"{filename}.midi",
            )
        else:
            try:
                print("MIDI write file=", midi_data_file)
                midi_data: MidiFile = get_mido(json_weather_data_file, seed)
                midi_data.save(midi_data_file)
                print("MIDI write file sucess=", midi_data_file)
                yield progressReportPacket(
                    "Generate MIDI", progress=100, filename=f"{filename}.midi"
                )
            except Exception as ex:
                print("MIDI generation failed=", ex)
                yield progressReportPacket("Generate MIDI", failed=True)
                return

        # Convert to audio ------------------------------------------
        yield progressReportPacket("Convert to audio", progress=None)

        async def execute_async(executable_name, arguments=[]):
            process = await create_subprocess_exec(
                executable_name, *arguments, stdin=None, stdout=subprocess.DEVNULL
            )
            return await process.wait()

        audio_ogg_file: Path = cache_path / f"{filename}.ogg"
        audio_mp3_file: Path = cache_path / f"{filename}.mp3"
        not_exist_count = 0
        if not audio_ogg_file.exists():
            not_exist_count += 1
        if not audio_mp3_file.exists():
            not_exist_count += 1
        if not_exist_count == 0:
            print("Audio cache hit=", audio_ogg_file, audio_mp3_file)
            yield progressReportPacket(
                "Convert to audio",
                progress=100,
                from_cache=True,
                filename=f"{filename}.ogg",
            )
        else:
            yield progressReportPacket("Convert to audio", progress=0)
            with tempfile.NamedTemporaryFile(
                mode="w+b", suffix=".raw", delete=True
            ) as temp_file:
                print("Audio write temp file=", temp_file.name)
                # fmt: off
                fluidsynth_args = [
                    "-F", temp_file.name,
                    "/usr/share/sounds/sf2/FluidR3_GM.sf2",
                    "-O", "float",
                    "-L", "1",
                    "-r", "48000",
                    "-T", "raw",
                    "-E", "little",
                    midi_data_file,
                ]
                # fmt: on
                return_code = await execute_async("fluidsynth", fluidsynth_args)

                if return_code == 0:
                    yield progressReportPacket("Convert to audio", progress=30)
                    if not audio_ogg_file.exists():
                        print("Audio write file=", audio_ogg_file)
                        # fmt: off
                        ffmpeg_ogg_args = [
                            "-y",
                            "-f", "f32le",
                            "-ar", "48000",
                            "-ac", "2",
                            "-i", temp_file.name,
                            "-c:a", "libopus",
                            "-b:a", "52K",
                            "-compression_level", "10",
                            "-vbr", "on",
                            "-frame_duration", "40",
                            "-application", "audio",
                            "-mapping_family", "0",
                            audio_ogg_file,
                        ]
                        # fmt: on
                        return_code = await execute_async("ffmpeg", ffmpeg_ogg_args)
                        if return_code == 0:
                            print("Audio write file sucess=", audio_ogg_file)
                            yield progressReportPacket(
                                "Convert to audio",
                                progress=100 if not_exist_count == 1 else 65,
                                filename=f"{filename}.ogg",
                            )
                        else:
                            print("Audio conversion failed=", return_code)
                            yield progressReportPacket("Convert to audio", failed=True)
                    if not audio_mp3_file.exists():
                        print("Audio write file=", audio_mp3_file)
                        # fmt: off
                        ffmpeg_mp3_args = [
                            "-y",
                            "-f", "f32le",
                            "-ar", "48000",
                            "-ac", "2",
                            "-i", temp_file.name,
                            "-c:a", "libmp3lame",
                            "-b:a", "64k",
                            audio_mp3_file,
                        ]
                        # fmt: on
                        return_code = await execute_async("ffmpeg", ffmpeg_mp3_args)
                        if return_code == 0:
                            print("Audio write file sucess=", audio_mp3_file)
                            yield progressReportPacket(
                                "Convert to audio",
                                progress=100,
                                filename=f"{filename}.mp3",
                            )
                        else:
                            print("Audio conversion failed=", return_code)
                            yield progressReportPacket("Convert to audio", failed=True)
                else:
                    print("Audio conversion failed=", return_code)
                    yield progressReportPacket("Convert to audio", failed=True)

    return StreamingResponse(iterfile(), media_type="text/plain")
