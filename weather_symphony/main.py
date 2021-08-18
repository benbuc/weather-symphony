import argparse
import datetime
import logging
import os
import random
from pathlib import Path

import mido

from weather_symphony.components import HarmonyGenerator, SceneParser
from weather_symphony.components.sections import (
    FluteMelody,
    GlockenspielMelody,
    PercussionSection,
    StringsSection,
    TrumpetsSection,
    TubaSection,
    UpperStringsSection,
    XylophoneMelody,
)
from weather_symphony.data_loaders import APIFileLoader
from weather_symphony.music import Meter

logging.basicConfig(level=logging.DEBUG)

ACTIVE_SECTIONS = [
    StringsSection,
    UpperStringsSection,
    TrumpetsSection,
    FluteMelody,
    TubaSection,
    XylophoneMelody,
    PercussionSection,
    GlockenspielMelody,
]


def performSections(weather_data, scenes, harmony):
    performances = []
    section_num = 0
    for s in ACTIVE_SECTIONS:
        section = s(section_num, weather_data, scenes, harmony)
        performances.append(section.perform())
        section_num += 1

    return performances


def get_mido(date, seed=0):
    random.seed(seed)

    logging.debug("Weather Symphony Generator started")

    data_loader = APIFileLoader("./weather_data/berlin_2021_07_06_edited.json", date)
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

    return mid


def main(args):
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)

    date = args.date
    if not date:
        date = datetime.date.today()
    mid = get_mido(args.date)

    if args.output:
        mid.save(args.output)
    if os.name == "nt":  # Windows
        logging.info("Starting live audio for windows")
        output = mido.open_output()
        for msg in mid.play(meta_messages=True):
            if msg.is_meta:
                continue
            output.send(msg)
    else:
        if args.output:
            os.system(f"timidity {args.output}")


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", default=None, type=datetime.date.fromisoformat)
    parser.add_argument("-o", "--output", type=Path)

    args = parser.parse_args()
    main(args)
