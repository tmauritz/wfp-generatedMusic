from pyo import *

def test_sound_Windows():
    s=Server(duplex=1, winhost="mme").boot()
    s.start()
    a = Sine(mul=0.01).out()
    s.gui(locals())

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Starting Server...")
    test_sound_Windows()
