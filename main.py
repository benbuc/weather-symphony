import argparse
import datetime
import logging
from pathlib import Path
import os

import mido

from data_loaders import APIFileLoader
from components import SceneParser, HarmonyGenerator
from components.sections import StringSection
from music import Meter

logging.basicConfig(level=logging.DEBUG)

ACTIVE_SECTIONS = [StringSection]

def performSections(weather_data, scenes, harmony):
    performances = []
    for s in ACTIVE_SECTIONS:
        section = s(weather_data, scenes, harmony)
        performances.append(section.perform())

    return performances

def main(args):
    logging.debug("Weather Symphony Generator started")

    args.output.parent.mkdir(parents=True, exist_ok=True)

    # date = args.date
    # if not date:
    #     date = datetime.date.today()
    date =  datetime.date(2021, 7, 6)
    
    data_loader = APIFileLoader("./weather_data/berlin_2021_07_06.json", date)
    weather_data = data_loader.get_weather_data()

    scene_parser = SceneParser(weather_data)
    scenes = scene_parser.get_scenes()

    harmony_generator = HarmonyGenerator(weather_data, scenes)
    harmony = harmony_generator.get_harmony()

    performances = performSections(weather_data, scenes, harmony)

    mid = mido.MidiFile()
    mid.ticks_per_beat = Meter.ticks_per_beat
    for performance in performances:
        mid.tracks.append(performance)
    
    mid.save(args.output)
    if os.name == "nt": # Windows
        logging.info("Starting live audio for windows")
        output = mido.open_output()
        for msg in mid.play(meta_messages=True):
            if msg.is_meta:
                continue
            output.send(msg)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--date', default=None, type=datetime.date.fromisoformat)
    parser.add_argument('-o', '--output', default=Path(__file__).absolute().parent / "output/ws.midi", type=Path)

    args = parser.parse_args()
    main(args)