from pyo import EventDrunk, Pattern

from data.MusicalScales import MusicalScale


class Voice:
    def __init__(self,
             server,
                 voice_range=None,
             max_step = 2,
             pattern_timer = 0.25,
             decay = 50,
                 note_length_ms = 500
             ):
        if voice_range is None:
            voice_range = MusicalScale.MINOR_HARMONIC.transpose(-1)
        self.server = server
        self.voice_range = voice_range
        self.pitch = EventDrunk(self.voice_range, maxStep=max_step)
        self.pattern = Pattern(self.midi_event, pattern_timer)
        self.vel = 0
        self.dur = 0
        self.note_length_ms = note_length_ms
        self.decay = decay

    def midi_event(self):
        pitch = int(self.pitch.next())
        print("playing pitch: %d, velocity: %d, duration: %d ms" % (pitch, self.vel, self.note_length_ms))
        self.server.makenote(pitch=pitch,velocity=self.vel,duration=self.note_length_ms)
        self.vel -= self.decay
        if self.vel <= 0 : self.pattern.stop()

    def play(self, velocity = 100, duration = 15):
        self.vel = velocity
        self.dur = duration
        self.pattern.play(dur=duration)

    def play_one_note(self, velocity = 100, duration = 15):
        self.vel = velocity
        self.dur = duration
        self.midi_event()
