import json

from weather_symphony.data_loaders.DataLoader import DataLoader


class APIFileLoader(DataLoader):
    def __init__(self, file, date):
        super().__init__(date)
        self.file = file

    def get_weather_data(self):
        json_data = json.load(open(self.file, "r"))
        hourly_data = json_data["hourly"]

        return {
            "temperature": [(hour["feels_like"] - 273.15) for hour in hourly_data],
            "humidity": [hour["humidity"] for hour in hourly_data],
            "clouds": [hour["clouds"] for hour in hourly_data],
            "wind": [hour["wind_speed"] for hour in hourly_data],
            "visibility": [hour["visibility"] for hour in hourly_data],
            "weather_condition": [hour["weather"][0]["id"] for hour in hourly_data],
            "rain": [
                hour["rain"]["1h"] if ("rain" in hour) else 0 for hour in hourly_data
            ],
            "snow": [
                hour["snow"]["1h"] if ("snow" in hour) else 0 for hour in hourly_data
            ],
        }
