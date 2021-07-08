class HarmonyGenerator:
    def __init__(self, weather_data, scenes):
        self.weather_data = weather_data
        self.scenes = scenes

    def get_harmony(self):
        return [0]*24