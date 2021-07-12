class Key:

    def __init__(self, root):

        # map notes to the lowest piano octave
        # MIDI Code for C1 is 24 
        # octaves are calculated based on this C
        self.root = root % 12 + 24
        self.intervals = []

    def get_note(self, degree, octave=1):
        """
        Returns the note for a specific
        scale degree in the base octave.
        """
        return self.root + sum(self.intervals[:degree-1]) + 12*(octave-1)

class Major(Key):

    def __init__(self, *args):
        super().__init__(*args)

        self.intervals = [2,2,1,2,2,2,1]

