from time import sleep

from pyo import *
from pyotools import FatBass

from sound.instruments.SampleInstrument import SampleInstrument


def test_sound_windows():
    s=Server(duplex=1, winhost="mme").boot()
    s.start()
    a = FatBass(freq=110, mul=0.01,octave=0).out()
    s.gui()

def play_sample_sequence(seconds = 100):
    s=Server(duplex=1, winhost="mme").boot() # Boot up Server

    scale = EventScale(root="C", scale="minorH", first=1, octaves=1) # Generate Sequence of pitches
    volumes=[]
    for i in range(0, len(scale)):                                  # Generate Sequence of volumes
        if i % 4 == 0: volumes.append(0.2)
        elif i % 4 == 1: volumes.append(0.4)
        elif i % 4 == 2: volumes.append(0.8)
        elif i % 4 == 3: volumes.append(0)

    # create event object containing all sequences, pitch(scale) will be sequenced in order, and volume(amp) randomly
    event = Events(
        instr=SampleInstrument,
        freq=EventSeq(scale),
        amp=EventDrunk(volumes,maxStep=3),
        beat = 1/4,
        durmul=0.5,
        dur=0.5
    )

    s.start()
    event.play()
    sleep(seconds) # sleep() is necessary to keep server alive, even if it is not stopped afterward
    event.stop()
    s.stop()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Starting Server...")
    play_sample_sequence(10)
