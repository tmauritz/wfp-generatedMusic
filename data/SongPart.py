import random

from pyo import Pattern, Phasor, EventDrunk, RandInt


#Intensity: Notes played per second -> influences probability of note output, velocity, pitch etc.
#Intensity increased every time note is played, decays over time slowlyluq
#Mod trigger -> lambda function (switch ti next song part, variation 2-1 etc)

#Song structure:
#- key
#- parts
#- mod functions
#-  intensity probability trigger curve
#-  main voice
#-  aux voice
#-  bass

class SongPart:
    def __init__(self, server):
        self.bass_voice_range = list(range(35,55)) # bass midi range TODO: scales!
        self.aux_voice_range = list(range(45,70)) #aux midi range TODO: scales!
        self.lead_voice_range = list(range(72, 95))  # lead midi range TODO: scales!
        self.bass_pitch = EventDrunk(self.bass_voice_range, maxStep=4) #performs a random walk over the bass values
        self.bass_pattern = Pattern(self.bass_midi_event, 0.25)
        self.bass_vel = 0
        self.bass_decay = 15
        self.count = 0
        self.bass_dur = 2
        self.server = server
        print(self.bass_voice_range)
        print(self.aux_voice_range)
        print(self.lead_voice_range)

    def bass_midi_event(self):
        pitch = int(self.bass_pitch.next())
        if self.bass_vel > 0:
            print("playing pitch: %d, velocity: %d, duration: %d" % (pitch, self.bass_vel, self.bass_dur))
            self.server.makenote(pitch=pitch, velocity = self.bass_vel, duration = int(self.bass_dur))
            self.bass_vel -= self.bass_decay

    def Bass(self):
        return random.choice(self.bass_voice_range)

    def Lead(self):
        return random.choice(self.lead_voice_range)

    def Aux(self):
        return random.choice(self.aux_voice_range)

    def BassRange(self):
        return self.bass_voice_range

    def LeadRang(self):
        return self.lead_voice_range

    def AuxRange(self):
        return  self.aux_voice_range

    def onBassOn(self, velocity = 500, duration = 15):
        self.bass_pattern.stop()
        self.bass_vel = velocity
        self.bass_dur = duration
        self.bass_pattern.play(dur=duration)