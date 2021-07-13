from abc import abstractmethod


class DataLoader:
    def __init__(self, date):
        self.date = date

    @abstractmethod
    def get_weather_data(self):
        pass
