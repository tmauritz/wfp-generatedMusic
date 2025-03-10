from enum import Enum


class MusicalScale(Enum):
    MAJOR = ("major", 7)
    MINOR_HARMONIC = ("minorH", 7)
    MINOR_MELODIC = ("minorM", 7)
    IONIAN = ("ionian", 7)
    DORIAN = ("dorian", 7)
    PHRYGIAN = ("phrygian", 7)
    LYDIAN = ("lydian", 7)
    MIXOLYDIAN = ("mixolydian", 7)
    AEOLIAN = ("aeolian", 7)
    LOCRIAN = ("locrian", 7)
    WHOLE_TONE = ("wholeTone", 6)
    MAJOR_PENTATONIC = ("majorPenta", 5)
    MINOR_PENTATONIC = ("minorPenta", 5)
    EGYPTIAN = ("egyptian", 5)
    MAJOR_BLUES = ("majorBlues", 6)
    MINOR_BLUES = ("minorBlues", 6)
    MINOR_HUNGARIAN = ("minorHungarian", 7)

    def __init__(self, scale_name, num_notes):
        self.scale_name = scale_name
        self.num_notes = num_notes
