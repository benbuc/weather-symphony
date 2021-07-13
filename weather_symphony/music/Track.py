import mido

from weather_symphony.music import Meter


class Track:
    def __init__(self, program, channel):

        self.program = program
        self.channel = channel

        # contains tuples of (time, note_id, note on or off)
        self.notes = []

    def add_note(self, note, start, duration, velocity=127):
        self.notes.append((start, note, "note_on", velocity))
        self.notes.append((start + duration, note, "note_off", velocity))

    def midi_time_for_note(self, note_time):
        multiplier = (Meter.ticks_per_beat * Meter.beats_per_bar) // Meter.max_subdivs
        return note_time * multiplier

    def export(self):
        self.notes.sort()

        track = mido.MidiTrack()
        track.append(
            mido.Message(
                "program_change", program=self.program, channel=self.channel, time=0
            )
        )
        track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(Meter.bpm)))

        last_message_time = 0

        for note in self.notes:
            current_time = self.midi_time_for_note(note[0])
            time_diff = current_time - last_message_time
            last_message_time = current_time

            msg = mido.Message(
                note[2],
                note=note[1],
                velocity=note[3],
                channel=self.channel,
                time=time_diff,
            )
            track.append(msg)

        return track
