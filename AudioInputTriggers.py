from pyo import *

def create_trigger(input_channel, trigger_function = lambda : None, cutoff=10,maxthresh=4, minthresh=-20):
    # thresh = Thresh(input=input_channel, threshold=threshold, dir=0) # basic
    # Smooth signal to avoid jitter (optional)
    attack = AttackDetector(input_channel, deltime=0.005, cutoff=cutoff, maxthresh=maxthresh, minthresh=minthresh, reltime=0.05)

    trigger = TrigFunc(input=attack, function=trigger_function)
    return trigger


def trigger_test(name = "Trigger"):
    """
    Creates a Trigger that triggers a function every time the input signal is above threshold.
    :return: a Trigger set up for the specified input channel
    """
    print("detected ", name)


def main():
    """
    Displays a scope for audio testing. edit sampling rate, input devices and channels to match your setup.
    :return: nothing
    """
    s = Server()
    s.setIchnls(3)
    s.setSamplingRate(48000) # replace with the correct sampling rate for your interface
    s.setInOutDevice(16)  # replace with your USB interface's input index
    s.boot()
    while not s.getIsBooted():
        time.sleep(1)
    s.start()

    inputs = Input([0,1,2], mul=2) # add all inputs to be monitored into the list
    input1 = Input(0, mul=2)
    input2 = Input(1, mul=2)
    input3 = Input(2, mul=2)

    scope1 = Spectrum(input=inputs, wintitle="Input")

    trigger1 = create_trigger(input_channel=input1, trigger_function=lambda : trigger_test("Bass"))
    trigger2 = create_trigger(input_channel=input2, trigger_function=lambda: trigger_test("Snare"),cutoff=30)
    trigger3 = create_trigger(input_channel=input3, trigger_function=lambda: trigger_test("Aux"))

    s.gui(locals())

if __name__ == "__main__":
    main()