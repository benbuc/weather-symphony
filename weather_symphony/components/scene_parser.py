import logging
from enum import Enum, auto

from weather_symphony.music import Meter


class Scene(Enum):
    ANY = auto()
    OVERCAST_THUNDERSTORM = auto()
    OVERCAST_WINDY = auto()
    BROKEN_RAINY = auto()
    BROKEN_GUSTY = auto()
    SCATTERED_WINDY = auto()
    SCATTERED_SWELTRY = auto()
    CLEAR_BROILING = auto()
    CLEAR_NICE = auto()
    NIGHT_CHILLY = auto()
    NIGHT_WARM = auto()


class SceneParser:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def match_scene(self, data):
        if data["hour"] < 5 or data["hour"] > 23:
            if data["temperature"] < 5:
                return Scene.NIGHT_CHILLY
            elif data["temperature"] < 12 and data["wind"] > 8:
                return Scene.NIGHT_CHILLY

            if data["temperature"] > 22:
                return Scene.NIGHT_WARM

            logging.warn("night but not chilly and not warm")

        if data["clouds"] > 98:
            for weather_condition in data["weather_condition"]:
                if weather_condition > 200 and weather_condition < 300:
                    return Scene.OVERCAST_THUNDERSTORM

            if data["wind"] > 8:
                return Scene.OVERCAST_WINDY

            logging.warn("overcast but no thundering and no wind")

        elif data["clouds"] > 50:
            if data["rain"] > 0:
                return Scene.BROKEN_RAINY

            if data["wind"] > 8:
                return Scene.BROKEN_GUSTY

            logging.warn("broken but no rain and no wind")

        elif data["clouds"] > 15:
            if data["humidity"] > 80 and data["temperature"] > 24:
                return Scene.SCATTERED_SWELTRY

            if data["wind"] > 8:
                return Scene.SCATTERED_WINDY

            logging.warn("scattered but not sweltry and no wind")

        else:
            if data["temperature"] > 32:
                return Scene.CLEAR_BROILING
            elif data["temperature"] > 26 and data["wind"] < 1:
                return Scene.CLEAR_BROILING

            if data["temperature"] > 16 and data["rain"] == 0:
                return Scene.CLEAR_NICE

            logging.warn("clear but not broiling and not nice")

        return Scene.ANY

    def get_scenes(self):
        scenes = []
        for hour in self.weather_data:
            scene = self.match_scene(hour)
            logging.debug(scene)
            scenes += [scene] * Meter.bars_per_hour
        return scenes
