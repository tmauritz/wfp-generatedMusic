from pyo import EventInstrument, Phasor, Expseg, Compare, ButLP, ButHP, WGVerb, Compress


class SampleInstrument(EventInstrument):
    def __init__(self, **args):
        EventInstrument.__init__(self, **args)

        self.freq*=10

        # self.freq is derived from the 'degree' argument.
        self.phase = Phasor([self.freq, self.freq * 1.001])

        # self.dur is derived from the 'beat' argument.
        self.duty = Expseg([(0, 0.05), (self.dur, 0.5)], exp=4).play()

        self.osc = Compare(self.phase, self.duty, mode="<", mul=.5, add=-0.5)

        # EventInstrument created the amplitude envelope as self.env.
        self.filt = ButLP(self.osc, freq=700, mul=self.env)

        self.limiter = Compress(self.filt).out()