import random

from pyo import Server, Phasor, Pattern, TrigFunc, Notein


class SampleControlServer:

    def __init__(self, midi_input_device, midi_output_device, audio_output_device, name="ControlServer"):
        print("Initializing Control Server...")
        self.midi_input = midi_input_device
        self.midi_output = midi_output_device
        self.name = name
        self.server = Server()
        self.count = 0
        self.server.setMidiInputDevice(midi_input_device)
        self.server.setMidiOutputDevice(midi_output_device)
        self.server.setOutputDevice(audio_output_device)
        self.server.boot()
        self.pitch = None
        self.vel = 0
        self.dur = 0
        self.notes = None
        self.pattern = None
        self.trigON = None
        self.trigOFF = None
        print("Control Server initialized.")

    def start(self):
        print("Starting Control Server...")
        self.server.start()
        self.notes = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)

        # These functions are called when Notein receives a MIDI note event.
        def noteon(voice):
            "Print pitch and velocity for noteon event."
            pit = int(self.notes["pitch"].get(all=True)[voice])
            vel = int(self.notes["velocity"].get(all=True)[voice] * 127)
            print("Noteon: voice = %d, pitch = %d, velocity = %d" % (voice, pit, vel))
            self.server.makenote(pit, vel, vel*10)

        def noteoff(voice):
            "Print pitch and velocity for noteoff event."
            pit = int(self.notes["pitch"].get(all=True)[voice])
            vel = int(self.notes["velocity"].get(all=True)[voice] * 127)
            print("Noteoff: voice = %d, pitch = %d, velocity = %d" % (voice, pit, vel))

        # TrigFunc calls a function when it receives a trigger. Because notes["trigon"]
        # contains 10 streams, there will be 10 caller, each one with its own argument,
        # taken from the list of integers given at `arg` argument.
        self.trigON = TrigFunc(self.notes["trigon"], noteon, arg=list(range(10)))
        self.trigOFF = TrigFunc(self.notes["trigoff"], noteoff, arg=list(range(10)))

        print(f"Control Server started. Listening on MIDI Input {self.midi_input}")

    def showGUI(self):
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
