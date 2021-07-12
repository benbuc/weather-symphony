from abc import abstractmethod

class Section:
    def __init__(self, weather_data, scenes, harmonic_outline):
        self.weather_data = weather_data
        self.scenes = scenes
        self.harmonic_outline = harmonic_outline
        self.key = harmonic_outline['key']
    
    @abstractmethod
    def perform(self):
        pass