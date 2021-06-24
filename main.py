import argparse
import datetime
import logging

from data_loaders import DummyLoader
from components import SceneParser, HarmonyGenerator
from components.sections import StringSection

logging.basicConfig(level=logging.DEBUG)

def main(args):
    logging.debug("Weather Symphony Generator started")

    date = args.date
    if not date:
        date = datetime.date.today()
    
    data_loader = DummyLoader(date)
    weather_data = data_loader.get_weather_data()

    scene_parser = SceneParser(weather_data)
    scenes = scene_parser.get_scenes()

    harmony_generator = HarmonyGenerator(weather_data, scenes)
    harmony = harmony_generator.get_harmony()

    sections = [StringSection]

    for s in sections:
        section = s(weather_data, scenes, harmony)
        performance = section.perform()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--date', default=None, type=datetime.date.fromisoformat)

    args = parser.parse_args()
    main(args)