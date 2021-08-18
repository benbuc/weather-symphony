from weather_symphony.music import util as mutil


class Chord:
    intervals = {
        "maj": [4, 3],
        "min": [3, 4],
        "dim": [3, 3],
        "aug": [4, 4],
        "maj7": [4, 3, 4],
        "min7": [3, 4, 4],
    }

    def __init__(self, root, quality):
        assert quality in ["maj", "min", "maj7"]

        self.root = mutil.default_octave(root)
        self.quality = quality

    def get_all_notes(self):
        intervals = Chord.intervals[self.quality]
        return [self.root + sum(intervals[:i]) for i in range(len(intervals) + 1)]
