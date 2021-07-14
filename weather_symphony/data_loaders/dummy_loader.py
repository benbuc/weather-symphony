import random

from weather_symphony.data_loaders.data_loader import DataLoader


class DummyLoader(DataLoader):
    def get_weather_data(self):
        rain = [random.random() for _ in range(24)]

        return {"rain_percentage": rain}
