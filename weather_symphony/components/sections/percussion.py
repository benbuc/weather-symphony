import logging

from weather_symphony.components.sections.section import Section
from weather_symphony.music import Track


class PercussionSection(Section):
    def __init__(self, *args):
        super().__init__(*args)

        self.track = Track(47, 10)

    def perform(self):
        logging.debug(f"Performing {type(self).__name__}")

        self.track.add_note(38, 0, 16)

        return self.track.export()
