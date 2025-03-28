import sys

from pyo import *
from sqlalchemy.util import namedtuple


class SampleSynthServer:
    server = None
    # Generates an audio ramp from 36 to 84, from
    # which MIDI pitches will be extracted.
    # Global variable to count the down and up beats.
    notes = None
    pitch = None
    freqs = None
    amps = None
    sigL = None
    sigR = None
    outL = None
    outR = None

    def __init__(self,inout_device, midi_input_device, name="SynthServer"):
        self.inout = inout_device
        self.midi = midi_input_device
        self.name = name
        self.server = Server()
        self.server.setInOutDevice(inout_device)
        self.server.setMidiInputDevice(midi_input_device)
        self.server.boot()
        self.notes = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)
        self.notes.keyboard(title = "Synth Server Keyboard")
        # Notein["pitch"] retrieves pitch streams.
        # Converts MIDI pitch to frequency in Hertz.
        self.freqs = MToF(self.notes["pitch"])

        # Notein["velocity"] retrieves normalized velocity streams.
        # Applies a portamento on the velocity changes.
        self.amps = Port(self.notes["velocity"], risetime=0.005, falltime=0.5, mul=0.1)

        # Creates two groups of oscillators (10 per channel), slightly detuned.
        self.sigL = RCOsc(freq=self.freqs, sharp=0.5, mul=self.amps)
        self.sigR = RCOsc(freq=self.freqs * 1.003, sharp=0.5, mul=self.amps)

        # Mixes the 10 voices per channel to a single stream and send the
        # signals to the audio output.
        self.outL = self.sigL.mix(1).out()
        self.outR = self.sigR.mix(1).out(1)

    def start(self):
        self.server.start()
        print("Synth Server started, listening on Midi Device", self.midi)
        return self

    def showGUI(self):
        self.server.gui(locals(), title=self.name) #TODO: This blocks the thread!

def main():
    print(sys.argv)
    if len(sys.argv) == 3:
        synthServer = SampleSynthServer(inout_device=sys.argv[1], midi_input_device=int(sys.argv[2]))
    else:
        synthServer = SampleSynthServer(inout_device=0, midi_input_device=3)
    synthServer.start()
    synthServer.showGUI()

if __name__ == "__main__":
    main()