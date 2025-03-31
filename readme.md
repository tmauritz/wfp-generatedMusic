# WFP1 - a work in progress

This project aims to generate electronic music based on live drumming input.

## Installation
Install Python, then install Pyo using Pip
``` shell
pip install pyo
```
Run _main.py_ for an example setup.

### IMPORTANT: Windows wants extra configuration
Pyo Servers require extra arguments when running under Windows, requiring you to modify the individual classes to avoid errors. See https://belangeo.github.io/pyo/winaudioinspect.html for more information. Cross-platform-compatibility is on the TODO-List.

### MIDI Bridges
To interface between the different modules, virtual MIDI bridges are needed.
On Linux, Midi Through ports are created by the **snd-seq-dummy** kernel module. To change the number of ports unload it with`sudo modprobe -r snd-seq-dummy` and then reload it with the desired number of ports e.g. `sudo modprobe snd-seq-dummy ports=3`. To make this permanent create e.g. `/etc/modprobe.d/midi.conf` with the text `options snd-seq-dummy ports=3`
Then, use the JACK patch bay **(qjackctl)** to configure routing between the virtual MIDI devices.
On Windows,

### Setting input/output devices
Before running _main.py_, run _settings.py_ to get a list of all available audio and MIDI devices. Then, set the correct indices in _main.py_. I'm working on a global settings module, I promise.