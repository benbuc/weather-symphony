from weather_symphony.music.Key import Major

class HarmonyGenerator:
    def __init__(self, weather_data, scenes):
        self.weather_data = weather_data
        self.scenes = scenes

    def get_harmony(self):
        return {
            'key': Major(24), # C Major
            'chords': [0]*24
        }