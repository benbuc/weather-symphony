import json

from weather_symphony.data_loaders.DataLoader import DataLoader


class APIFileLoader(DataLoader):
    def __init__(self, file, date):
        super().__init__(date)
        self.file = file

    def get_weather_data(self):
        json_data = json.load(open(self.file, "r"))
        hourly_data = json_data["hourly"]

        return [
            {
                "hour": hour,
                "temperature": data["feels_like"] - 273.15,
                "humidity": data["humidity"],
                "clouds": data["clouds"],
                "wind": data["wind_speed"],
                "visibility": data["visibility"],
                # https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
                "weather_condition": data["weather"][0]["id"],
                "rain": data["rain"]["1h"] if ("rain" in data) else 0,
                "snow": data["snow"]["1h"] if ("snow" in data) else 0,
            }
            for (hour, data) in enumerate(hourly_data)
        ]
