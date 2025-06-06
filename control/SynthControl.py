import random
import sys
import time

from pyo import Server, Phasor, Pattern, TrigFunc, Notein, Input

from AudioInputTriggers import create_trigger
from data.SongPart import SongPart
from settings.Settings import ControlSettings


class SampleControlServer:

    def __init__(self, midi_input_device, midi_output_device, audio_inout_device, name="ControlServer"):
        self.trigger1 = None
        self.trigger2 = None
        self.trigger3 = None
        self.input3 = None
        self.input2 = None
        self.input1 = None
        self.input = None
        print("Initializing Control Server...")
        self.midi_input = midi_input_device
        self.midi_output = midi_output_device
        self.name = name
        self.count = 0
        self.server = Server()
        self.server.setIchnls(3)
        self.server.setSamplingRate(48000)  # replace with the correct sampling rate for your interface
        self.server.setInOutDevice(16)  # replace with your USB interface's input index
        self.server.setMidiInputDevice(midi_input_device)
        self.server.setMidiOutputDevice(midi_output_device)
        self.server.boot()
        print("Waiting for pyo server boot...")
        while not self.server.getIsBooted(): time.sleep(0.5)
        self.pitch = None
        self.vel = 0
        self.dur = 0
        self.notes = None
        self.pattern = None
        self.trigON = None
        self.trigOFF = None
        self.current_SongPart = SongPart(self.server) #TODO: make dynamic
        self.control_settings = ControlSettings() #TODO: make dynamic
        print("Control Server initialized.")

    def start(self):
        print("Starting Control Server...")
        self.server.start()
        self.notes = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)
        self.input1 = Input(0, mul=2)
        self.input2 = Input(1, mul=2)
        self.input3 = Input(2, mul=2)
        print("Creating Triggers...")
        self.trigger1 = create_trigger(input_channel=self.input1, trigger_function=self.current_SongPart.onBassOn)
        self.trigger2 = create_trigger(input_channel=self.input2, trigger_function=self.current_SongPart.onLeadOn, cutoff=30)
        self.trigger3 = create_trigger(input_channel=self.input3, trigger_function=self.current_SongPart.onAuxOn)

        # These functions are called when Notein receives a MIDI note event.
        def noteon(voice):
            """Prints pitch and velocity for noteon event."""
            pit = int(self.notes["pitch"].get(all=True)[voice])
            vel = int(self.notes["velocity"].get(all=True)[voice] * 127)
            dur = vel
            print("Input: voice = %d, pitch = %d, velocity = %d" % (voice, pit, vel))

            #figure out what input was triggered
            match pit:
                case self.control_settings.bass_midi_input:
                    print("Playing Bass Pattern")
                    self.current_SongPart.onBassOn(velocity=vel, duration = vel)
                case self.control_settings.lead_midi_input:
                    print("Playing Lead")
                    self.current_SongPart.onLeadOn(velocity=vel, duration = vel)
                case self.control_settings.aux_midi_input:
                    print("Playing Aux")
                    self.current_SongPart.onAuxOn(velocity=vel, duration = vel)

        # TrigFunc calls a function when it receives a trigger. Because notes["trigon"]
        # contains 10 streams, there will be 10 caller, each one with its own argument,
        # taken from the list of integers given at `arg` argument.
        self.trigON = TrigFunc(self.notes["trigon"], noteon, arg=list(range(10)))

        print(f"Control Server started. Listening on MIDI Input {self.midi_input}")

    def showGUI(self):
        self.notes.keyboard(title="SynthControl Keyboard")
        self.server.gui(locals(), title=self.name)  # TODO: This blocks the thread!

    def play_pattern(self):
        self.pitch = Phasor(freq=11, mul=48, add=36)

        def midi_event():
            # Retrieve the value of the pitch audio stream and convert it to an int.
            pit = int(self.pitch.get())

            # If the count is 0 (down beat), play a louder and longer event, otherwise
            # play a softer and shorter one.
            if self.count == 0:
                self.vel = random.randint(90, 110)
                self.vel = 500
            else:
                self.vel = random.randint(30, 50)
                self.vel = 125

            # Increase and wrap the count to generate a 4 beats sequence.
            self.count = (self.count + 1) % 4

            print("playing pitch: %d, velocity: %d, duration: %d" % (pit, self.vel, self.vel))

            # The Server's `makenote` method generates a noteon event immediately
            # and the corresponding noteoff event after `duration` milliseconds.
            self.server.makenote(pitch=pit, velocity=self.vel, duration=self.vel)

        # Generates a MIDI event every 125 milliseconds.
        self.pattern = Pattern(midi_event, 0.125).play()

def main():
    if len(sys.argv) == 4:
        control_server = SampleControlServer(midi_input_device=int(sys.argv[1]), midi_output_device=int(sys.argv[2]), audio_inout_device=int(sys.argv[3]))
    else:
        print("Please specify midi input device, midi output device, and an audio input/output device.")
        exit(0)
    control_server.start()
    #control_server.play_pattern()
    control_server.showGUI()

if __name__ == "__main__":
    main()