import json
from pathlib import Path

import yaml


class APIFileLoader:
    def __init__(self, file: Path):
        self.file = file

    def get_weather_data(self):
        if self.file.suffix == ".json":
            hourly_data = json.load(open(self.file, "r"))["hourly"]
        elif self.file.suffix == ".yaml":
            hourly_data = yaml.safe_load(open(self.file, "r"))
        else:
            raise ValueError("unknown file type")

        return [
            {
                "hour": hour,
                "temperature": data["feels_like"] - 273.15,
                "humidity": data["humidity"],
                "clouds": data["clouds"],
                "wind": data["wind_speed"],
                "visibility": data["visibility"],
                # https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
                "weather_condition": [
                    weather_condition["id"] for weather_condition in data["weather"]
                ],
                "rain": data["rain"]["1h"] if ("rain" in data) else 0,
                "snow": data["snow"]["1h"] if ("snow" in data) else 0,
            }
            for (hour, data) in enumerate(hourly_data)
        ]
