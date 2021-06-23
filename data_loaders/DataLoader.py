from abc import abstractmethod

class DataLoader:
    @abstractmethod
    def get_weather_data(self):
        pass