#Intensity: Notes played per second -> influences probability of note output, velocity, pitch etc.
#Intensity increased every time note is played, decays over time slowlyluq
import random


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
    def __init__(self):
        self.bass_voice_range = list(range(36,59)) # bass midi range TODO: scales!
        self.aux_voice_range = list(range(36,59)) #aux midi range TODO: scales!
        self.lead_voice_range = list(range(72, 95))  # lead midi range TODO: scales!
        print(self.bass_voice_range)
        print(self.aux_voice_range)
        print(self.lead_voice_range)

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