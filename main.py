import subprocess
from time import sleep

from control.SynthControl import SampleControlServer

control_server_midi_input = 5
control_server_midi_output = 0
control_server_audio_output = 0
synth_midi_input = 3
synth_audio_inout = 0

def main():

    #TODO: Add persistence layer to store input and output devices

    print("Starting subprocesses...")
    synthProcess = subprocess.Popen(["python", "./sound/Synth.py", f"0", "3"])
    sleep(2)  # Wait a bit before initializing control server

    print("Starting main control server...")
    control_server = SampleControlServer(midi_input_device=7, midi_output_device=0, audio_output_device=0)
    control_server.start()
    control_server.play_pattern()
    control_server.showGUI()

if __name__ == '__main__':
    main()