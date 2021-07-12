import mido

from . import Meter

class Track:
    def __init__(self, program):

        self.program = program

        # contains tuples of (time, note_id, note on or off)
        self.notes = []

    def add_note(self, note, start, duration):
        self.notes.append((start, note, 'note_on'))
        self.notes.append((start+duration, note, 'note_off'))

    def midi_time_for_note(self, note_time):
        multiplier = (Meter.ticks_per_beat * Meter.beats_per_bar) // Meter.max_subdivs
        return note_time * multiplier

    def export(self):
        self.notes.sort()

        track = mido.MidiTrack()
        track.append(mido.Message('program_change', program=self.program, time=0))
        track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(Meter.bpm)))

        last_message_time = 0

        for note in self.notes:
            current_time = self.midi_time_for_note(note[0])
            time_diff = current_time - last_message_time
            last_message_time = current_time

            msg = mido.Message(note[2], note=note[1], velocity=127, time=time_diff)
            track.append(msg)

        return track