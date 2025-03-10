from pyo import EventInstrument, Phasor, Expseg, Compare, ButLP, ButHP


class SampleInstrument(EventInstrument):
    def __init__(self, **args):
        EventInstrument.__init__(self, **args)

        self.freq*=10

        # self.freq is derived from the 'degree' argument.
        self.phase = Phasor([self.freq, self.freq * 1.003])

        # self.dur is derived from the 'beat' argument.
        self.duty = Expseg([(0, 0.05), (self.dur, 0.5)], exp=4).play()

        self.osc = Compare(self.phase, self.duty, mode="<", mul=1, add=-0.5)

        # EventInstrument created the amplitude envelope as self.env.
        self.filt = ButLP(self.osc, freq=400, mul=self.env).out()