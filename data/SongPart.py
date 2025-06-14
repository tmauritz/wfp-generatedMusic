import random

from pyo import Pattern, Phasor, EventDrunk, RandInt

from data.MusicalScales import MusicalScale
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
    def __init__(self, server, bpm = 120):
        self.server = server
        self.bpm = bpm
        self.bps = bpm
        self.bass_voice = Voice(server,
                                voice_range = MusicalScale.MINOR_HARMONIC.transpose(-2),
                                max_step=4,
                                pattern_timer=self.bps,
                                decay=10)
        self.lead_voice = Voice(server,
                                voice_range = MusicalScale.MINOR_BLUES.transpose(0),
                                max_step=2,
                                pattern_timer=self.bps/4,
                                decay=10)
        self.aux_voice = Voice(server,
                               voice_range= MusicalScale.MINOR_HARMONIC.transpose(-1),
                               max_step=2,
                               pattern_timer=self.bps/8,
                               decay=20)
        
    def Bass(self):
        return self.bass_voice

    def Lead(self):
        return self.lead_voice

    def Aux(self):
        return self.aux_voice

    def onBassOn(self, velocity = 50, duration = 15):
        self.bass_voice.play(velocity, duration)

    def onLeadOn(self, velocity = 50, duration = 15):
        self.lead_voice.play(velocity, duration)

    def onAuxOn(self, velocity = 50, duration = 15):
        self.aux_voice.play(velocity, duration)