from pyo import EventDrunk, Pattern

from midi_out_test import midi_event

class Voice:
    def __init__(self,
             server,
                 voice_range=None,
             max_step = 2,
             pattern_timer = 0.25,
             decay = 0
             ):
        if voice_range is None:
            voice_range = list(range(45, 70))
        self.server = server
        self.voice_range = voice_range
        self.pitch = EventDrunk(self.voice_range, maxStep=max_step)
        self.pattern = Pattern(self.midi_event, pattern_timer)
        self.vel = 0
        self.dur = 0
        self.decay = decay

    def midi_event(self):
        pitch = int(self.pitch.next())
        print("playing pitch: %d, velocity: %d, duration: %d" % (pitch, self.vel, self.dur))
        self.server.makenote(pitch=pitch,velocity=self.vel,duration=int(self.dur))
        self.vel -= self.decay
        if self.vel <= 0 : self.pattern.stop()

    def play(self, velocity = 100, duration = 15):
        self.vel = velocity
        self.dur = duration
        self.pattern.play(dur=duration)

    def play_one_note(self, velocity = 100, duration = 15):
        self.vel = velocity
        self.dur = duration
        midi_event()
