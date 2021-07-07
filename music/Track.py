import mido

from . import Meter

class Track:
    def __init__(self, program):

        self.program = program

        # contains tuples of (time, note_id, note on or off)
        self.notes = []

    def addNote(self, note, start, duration):
        self.notes.append((start, note, 'note_on'))
        self.notes.append((start+duration, note, 'note_off'))

    def export(self):
        self.notes.sort()

        track = mido.MidiTrack()
        track.append(mido.Message('program_change', program=self.program, time=0))
        track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(Meter.bpm)))

        last_message_time = 0

        for note in self.notes:
            current_time = note[0] * (Meter.ticks_per_beat // Meter.max_subdivs)
            time_diff = current_time - last_message_time
            last_message_time = current_time

            msg = mido.Message(note[2], note=note[1], velocity=127, time=time_diff)
            track.append(msg)

        return track