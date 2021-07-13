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


def match_scene(hour, data):
    if hour < 5 or hour > 23:
        if data["temperature"] < 5:
            return Scene.NIGHT_CHILLY
        elif data["temperature"] < 12 and data["wind"] > 8:
            return Scene.NIGHT_CHILLY

        if data["temperature"] > 22:
            return Scene.NIGHT_WARM

        logging.warn("night but not chilly and not warm")

    if data["clouds"] > 98:
        if data["weather_condition"] > 200 and data["weather_condition"] < 300:
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


class SceneParser:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def get_scenes(self):
        scenes = []
        for hour in range(24):
            weather = self.weather_data.items()
            hour_data = {key: value[hour] for (key, value) in weather}

            scenes += [match_scene(hour, hour_data)] * (Meter.total_bars // 24)

        return scenes
