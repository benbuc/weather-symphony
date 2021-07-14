from abc import abstractmethod


class Section:
    def __init__(self, channel_num, weather_data, scenes, harmonic_outline):
        self.channel_num = channel_num
        self.weather_data = weather_data
        self.scenes = scenes
        self.harmonic_outline = harmonic_outline
        self.keys = harmonic_outline["keys"]
        self.chords = harmonic_outline["chords"]

    @abstractmethod
    def perform(self):
        pass
