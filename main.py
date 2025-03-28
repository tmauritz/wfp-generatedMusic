from time import sleep

from pyo import *
# from pyotools import FatBass

from data.MusicalScales import MusicalScale
from sound.Synth import SampleSynthServer
from sound.instruments.SampleBassInstrument import SampleBassInstrument
from sound.instruments.SampleInstrument import SampleInstrument


def demo_sound_windows():
    s=Server(duplex=1, winhost="mme").boot()
    s.start()
    # a = FatBass(freq=110, mul=0.01,octave=0).out()
    s.gui()

def play_sample_sequence(seconds = 100):
    # Path of the recorded sound file.
    path = "synth.wav"
    s=Server(duplex=1, winhost="mme").boot() # Boot up Server
    # Record for 10 seconds a 24-bit wav file.
    s.recordOptions(dur=20, filename=path, fileformat=0, sampletype=1)

    scale_bass = EventScale(root="C", scale=MusicalScale.MINOR_BLUES.scale_name, first=1, octaves=1) # Generate Sequence of pitches
    scale_treble = EventScale(root="C", scale=MusicalScale.MINOR_MELODIC.scale_name, first=1, octaves=1)  # Generate Sequence of pitches
    volumes_bass=[]
    for i in range(0, len(scale_bass)):  # Generate Sequence of volumes
        if i % 4 == 0: volumes_bass.append(0.2)
        elif i % 4 == 1: volumes_bass.append(0.4)
        elif i % 4 == 2: volumes_bass.append(0.8)
        elif i % 4 == 3: volumes_bass.append(0)

    # create event object containing all sequences, pitch(scale) will be sequenced in order, and volume(amp) randomly
    event_bass = Events(
        instr=SampleBassInstrument,
        freq=EventDrunk(scale_bass, maxStep=3),
        amp=EventSeq(volumes_bass),
        beat = 1/2,
        durmul=3,
        bpm = 120,
    )
    event_treble = Events(
        instr=SampleInstrument,
        freq=EventDrunk(scale_treble, maxStep=1),
        amp=EventDrunk([0, 0.5, 0.2, 0,.7, 0.5, 0.2, .04, 0, .1], maxStep=3),
        beat=1/4,
        durmul=0.5,
        bpm=120,
    )

    s.start()
    s.recstart()
    event_bass.play()
    event_treble.play()

    sleep(seconds-5) # sleep() is necessary to keep server alive, even if it is not stopped afterward
    event_bass.stop()
    event_treble.stop()
    s.recstop()
    s.stop()

def midi_demo():
    s = Server()
    s.setMidiInputDevice(3)  # Change as required
    s.boot()
    s.start()
    notes = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)

    # User can show a keyboard widget to supply MIDI events.
    notes.keyboard()

    # Notein["pitch"] retrieves pitch streams.
    # Converts MIDI pitch to frequency in Hertz.
    freqs = MToF(notes["pitch"])

    # Notein["velocity"] retrieves normalized velocity streams.
    # Applies a portamento on the velocity changes.
    amps = Port(notes["velocity"], risetime=0.005, falltime=0.5, mul=0.1)

    # Creates two groups of oscillators (10 per channel), slightly detuned.
    sigL = RCOsc(freq=freqs, sharp=0.5, mul=amps)
    sigR = RCOsc(freq=freqs * 1.003, sharp=0.5, mul=amps)

    # Mixes the 10 voices per channel to a single stream and send the
    # signals to the audio output.
    outL = sigL.mix(1).out()
    outR = sigR.mix(1).out(1)

    # Notein["trigon"] sends a trigger when a voice receive a noteon.
    # Notein["trigoff"] sends a trigger when a voice receive a noteoff.

    # These functions are called when Notein receives a MIDI note event.
    def noteon(voice):
        "Print pitch and velocity for noteon event."
        pit = int(notes["pitch"].get(all=True)[voice])
        vel = int(notes["velocity"].get(all=True)[voice] * 127)
        print("Noteon: voice = %d, pitch = %d, velocity = %d" % (voice, pit, vel))

    def noteoff(voice):
        "Print pitch and velocity for noteoff event."
        pit = int(notes["pitch"].get(all=True)[voice])
        vel = int(notes["velocity"].get(all=True)[voice] * 127)
        print("Noteoff: voice = %d, pitch = %d, velocity = %d" % (voice, pit, vel))

    # TrigFunc calls a function when it receives a trigger. Because notes["trigon"]
    # contains 10 streams, there will be 10 caller, each one with its own argument,
    # taken from the list of integers given at `arg` argument.
    tfon = TrigFunc(notes["trigon"], noteon, arg=list(range(10)))
    tfoff = TrigFunc(notes["trigoff"], noteoff, arg=list(range(10)))

    s.gui(locals())

count = 0
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Starting Server...")

    pa_list_devices()
    pm_list_devices()

    #exit(0)

    synthServer = SampleSynthServer(inout_device=0, midi_input_device=1)
    synthServer.start()

    #generator_server = Server(nchnls=1)
    #generator_server.setOutputDevice(10)
    #generator_server.setMidiInputDevice(7)
    #generator_server.setMidiOutputDevice(2)
    #generator_server.boot()
    pitch = Phasor(freq=11, mul=48, add=36)

    def midi_event():
        global count
        # Retrieve the value of the pitch audio stream and convert it to an int.
        pit = int(pitch.get())

        # If the count is 0 (down beat), play a louder and longer event, otherwise
        # play a softer and shorter one.
        if count == 0:
            vel = random.randint(90, 110)
            dur = 500
        else:
            vel = random.randint(50, 70)
            dur = 125

        # Increase and wrap the count to generate a 4 beats sequence.
        count = (count + 1) % 4

        print("PLAYING: pitch: %d, velocity: %d, duration: %d" % (pit, vel, dur))

        # The Server's `makenote` method generates a noteon event immediately
        # and the corresponding noteoff event after `duration` milliseconds.
        synthServer.server.makenote(pitch=pit, velocity=vel, duration=dur)

    #generator_server.start()
    # Generates a MIDI event every 125 milliseconds.
    pat = Pattern(midi_event, 0.125).play()

    synthServer.server.gui(locals(), title="Synth Server GUI")

    sleep(1000)