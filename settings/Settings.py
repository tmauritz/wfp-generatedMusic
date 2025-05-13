from pyo import *

def displayMIDIDevices():
    pm_list_devices()

def displaySoundDevices():
    pa_list_devices()

# TODO: functions for setting input and output, and persistence (saving to file)
class ControlSettings:
    def __init__(self):
        self.bass_midi_input = 36 #C2
        self.lead_midi_input = 60 #C4
        self.aux_midi_input = 48  #C3

if __name__ == '__main__':
    displayMIDIDevices()
    displaySoundDevices()