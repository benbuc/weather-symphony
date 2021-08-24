import calendar
from datetime import date

from aiohttp import ClientResponseError, ClientSession

chunk_size = 4096


async def write_weather_data(
    session: ClientSession,
    filename: str,
    date_obj: date,
    latitude: str,
    longitude: str,
    apiKey: str,
):
    utc_timestamp = calendar.timegm(date_obj.timetuple())
    url = "http://api.openweathermap.org/data/2.5/onecall/timemachine"
    params = {"lat": latitude, "lon": longitude, "dt": utc_timestamp, "appid": apiKey}
    print("querying api=", url, params)
    async with session.get(
        url,
        params=params,
        headers={"Accept": "application/json"},
        allow_redirects=False,
    ) as response:
        content_type = response.headers["content-type"].split(";")[0].strip()
        if (not response.ok) or (content_type != "application/json"):
            raise ClientResponseError(
                request_info=response.request_info,
                status=response.status,
                message="API call failed",
                headers=response.headers,
                history=response.history,
            )
        else:
            print("API cache file=", filename)
            with open(filename, "xb") as fd:
                while True:
                    chunk = await response.content.read(chunk_size)
                    if not chunk:
                        break
                    fd.write(chunk)
