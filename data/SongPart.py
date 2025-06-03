import random

from pyo import Pattern, Phasor, EventDrunk, RandInt

from data.Voice import Voice


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

        self.bass_voice = Voice(server, voice_range = list(range(35,55)), max_step=4, pattern_timer=0.5)

        self.aux_voice_range = list(range(45,70)) #aux midi range TODO: scales!
        self.lead_voice_range = list(range(72, 95))  # lead midi range TODO: scales!
        self.count = 0
        self.server = server

    def Bass(self):
        return self.bass_voice

    def Lead(self):
        return random.choice(self.lead_voice_range)

    def Aux(self):
        return random.choice(self.aux_voice_range)

    def BassRange(self):
        return self.bass_voice

    def LeadRang(self):
        return self.lead_voice_range

    def AuxRange(self):
        return  self.aux_voice_range

    def onBassOn(self, velocity = 500, duration = 15):
        self.bass_voice.play(velocity, duration)