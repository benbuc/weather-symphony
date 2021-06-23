import logging

from .Section import Section

class StringSection(Section):

    def perform(self):
        logging.debug("Performing Strings")