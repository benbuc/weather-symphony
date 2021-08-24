import argparse
import logging
import random
from pathlib import Path

from mido import MidiFile

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


def get_mido(filepath, seed=0):
    random.seed(seed)

    logging.debug("Weather Symphony Generator started")

    data_loader = APIFileLoader(filepath)
    weather_data = data_loader.get_weather_data()

    scene_parser = SceneParser(weather_data)
    scenes = scene_parser.get_scenes()

    harmony_generator = HarmonyGenerator(weather_data, scenes)
    harmony = harmony_generator.get_harmony()

    performances = performSections(weather_data, scenes, harmony)

    mid = MidiFile()
    mid.ticks_per_beat = Meter.ticks_per_beat
    for performance in performances:
        mid.tracks.append(performance)

    return mid


def main(args):
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)

    logging.debug(f"Loading input from file {args.output}")
    midi_data: MidiFile = get_mido(args.input)
    midi_data.save(args.output)
    logging.debug(f"Saved midi file to {args.output}")


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=Path, required=True)
    parser.add_argument("-o", "--output", type=Path, required=True)

    args = parser.parse_args()
    main(args)
