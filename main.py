from time import sleep

from pyo import *
from pyotools import FatBass

from data.MusicalScales import MusicalScale
from sound.instruments.SampleBassInstrument import SampleBassInstrument
from sound.instruments.SampleInstrument import SampleInstrument


def test_sound_windows():
    s=Server(duplex=1, winhost="mme").boot()
    s.start()
    a = FatBass(freq=110, mul=0.01,octave=0).out()
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
        durmul=1,
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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Starting Server...")
    play_sample_sequence(20)