from weather_symphony.music import util as mutil


class Key:
    def __init__(self, root):
        self.root = mutil.default_octave(root)
        self.intervals = []

    def get_note(self, degree, octave=1):
        """
        Returns the note for a specific
        scale degree in the base octave.
        """
        return mutil.at_octave(self.root + sum(self.intervals[: degree - 1]), octave)


class Major(Key):
    def __init__(self, *args):
        super().__init__(*args)

        self.intervals = [2, 2, 1, 2, 2, 2, 1]
