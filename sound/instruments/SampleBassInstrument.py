from pyo import EventInstrument, Phasor, Expseg, Compare, ButLP, ButHP, WGVerb, Delay, Compress


class SampleBassInstrument(EventInstrument):
    def __init__(self, **args):
        EventInstrument.__init__(self, **args)

        self.freq*=5

        # self.freq is derived from the 'degree' argument.
        self.phase = Phasor([self.freq, self.freq * 1.003])

        # self.dur is derived from the 'beat' argument.
        self.duty = Expseg([(0, 0.05), (self.dur, 0.5)], exp=4).play()

        self.osc = Compare(self.phase, self.duty, mode="<", mul=.4, add=-0.5)

        # EventInstrument created the amplitude envelope as self.env.
        self.filt = ButLP(self.osc.mix(2), freq=100, mul=self.env)

        #self.delay = Delay(self.filt.mix(2), delay=[.94, .3], feedback=.5, mul=.1).out()

        # Apply reverb to the filtered signal (stereo output)
        #self.rev = WGVerb(self.delay.mix(2), feedback=[.2,.2], cutoff=5000, bal=.25, mul=.3).out()

        self.limiter = Compress(self.filt).out()