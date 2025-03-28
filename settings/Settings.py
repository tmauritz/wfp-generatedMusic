from pyo import *

def displayMIDIDevices():
    pm_list_devices()

def displaySoundDevices():
    pa_list_devices()

# TODO: functions for setting input and output, and persistence (saving to file)

if __name__ == '__main__':
    displayMIDIDevices()
    displaySoundDevices()