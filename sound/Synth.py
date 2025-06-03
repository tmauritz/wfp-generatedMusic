from pyo import *


class SampleSynthServer:

    def __init__(self,inout_device, midi_input_device, name="SynthServer"):
        self.inout = inout_device
        self.midi = midi_input_device
        self.name = name
        self.server = Server()
        self.server.setInOutDevice(inout_device)
        self.server.setMidiInputDevice(midi_input_device)
        self.server.boot()
        self.notes = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)
        self.notes.keyboard(title = "Synth Server Keyboard") #Uncomment this to play the synth directly via on-screen keyboard
        # Notein["pitch"] retrieves pitch streams.
        # Converts MIDI pitch to frequency in Hertz.
        self.freqs = MToF(self.notes["pitch"])

        # Notein["velocity"] retrieves normalized velocity streams.
        # Applies a portamento on the velocity changes.
        self.amps = Port(self.notes["velocity"], risetime=0.005, falltime=.5, mul=0.1)

        self.sigL = RCOsc(freq=self.freqs, sharp=0.5, mul=self.amps)
        self.sigR = RCOsc(freq=self.freqs * 1.003, sharp=0.5, mul=self.amps)

        self.cutoff = Sine(freq=0.2, mul=2250, add=2750)

        # Apply low-pass filters to each signal
        self.filteredL = ButLP(self.sigL, freq=self.cutoff)  # You can adjust cutoff frequency
        self.filteredR = ButLP(self.sigR, freq=self.cutoff)

        self.outL = self.filteredL.mix(1).out()
        self.outR = self.filteredR.mix(1).out(1)

    def start(self):
        self.server.start()
        print("Synth Server started, listening on Midi Device", self.midi)
        return self

    def showGUI(self):
        self.server.gui(locals(), title=self.name) #TODO: This blocks the thread!

def main():
    if len(sys.argv) == 3:
        synthServer = SampleSynthServer(inout_device=sys.argv[1], midi_input_device=int(sys.argv[2]))
    else:
        print("Please specify inout device and midi input device.")
        exit(0)
    synthServer.start()
    synthServer.showGUI()

if __name__ == "__main__":
    main()