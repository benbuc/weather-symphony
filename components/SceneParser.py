from enum import Enum, auto

class Scene(Enum):
    THUNDERSTORM = auto()
    MILD_SUMMER = auto()

class SceneParser:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def get_scenes(self):
        scenes = []
        for i in range(24):
            if self.weather_data['rain_percentage'][i] > 0.5:
                scenes.append(Scene.THUNDERSTORM)
            else:
                scenes.append(Scene.MILD_SUMMER)

        return scenes