from enum import Enum


class MusicalScale(Enum):
    MAJOR = [60, 62, 64, 65, 67, 69, 71]  # C D E F G A B
    MINOR_HARMONIC = [60, 62, 63, 65, 67, 68, 71]  # C D Eb F G Ab B
    MINOR_MELODIC = [60, 62, 63, 65, 67, 69, 71]  # C D Eb F G A B (ascending only)
    IONIAN = [60, 62, 64, 65, 67, 69, 71]  # Same as Major
    DORIAN = [60, 62, 63, 65, 67, 69, 70]  # C D Eb F G A Bb
    PHRYGIAN = [60, 61, 63, 65, 67, 68, 70]  # C Db Eb F G Ab Bb
    LYDIAN = [60, 62, 64, 66, 67, 69, 71]  # C D E F# G A B
    MIXOLYDIAN = [60, 62, 64, 65, 67, 69, 70]  # C D E F G A Bb
    AEOLIAN = [60, 62, 63, 65, 67, 68, 70]  # C D Eb F G Ab Bb
    LOCRIAN = [60, 61, 63, 65, 66, 68, 70]  # C Db Eb F Gb Ab Bb
    WHOLE_TONE = [60, 62, 64, 66, 68, 70]  # C D E F# G# A#
    MAJOR_PENTATONIC = [60, 62, 64, 67, 69]  # C D E G A
    MINOR_PENTATONIC = [60, 63, 65, 67, 70]  # C Eb F G Bb
    EGYPTIAN = [60, 62, 65, 67, 70]  # C D F G Bb (suspended pentatonic)
    MAJOR_BLUES = [60, 62, 63, 64, 67, 69]  # C D Eb E G A
    MINOR_BLUES = [60, 63, 65, 66, 67, 70]  # C Eb F Gb G Bb
    MINOR_HUNGARIAN = [60, 62, 63, 66, 67, 68, 71]  # C D Eb F# G Ab B

    def transpose(self, octaves=1):
        """
        Return the scale transposed by the given number of octaves.

        Parameters:
            octaves (int): Number of octaves to transpose. Positive = up, Negative = down.

        Returns:
            list of int: Transposed MIDI note numbers.
        """
        return [note + 12 * octaves for note in self.value]
