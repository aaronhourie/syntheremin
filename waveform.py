from scipy import signal
from numpy import pi, sin, ndarray


# Generic parent class for generating wavetables based on a callback
class Waveform:
    def __init__(self, callback, offset=0, magnitude=0.5):
        # type: (callable, float, float) -> Waveform
        self.callback = callback
        self.offset = offset
        self.magnitude = magnitude

    def generate_wave(self, t, frequency):
        return self.callback(t, frequency, self.offset, self.magnitude)


### Pre-built callbacks. ###

def sine_wave(t, frequency, offset, magnitude):
    # type: (ndarray, float, float, float, float) -> ndarray
    return sin(frequency * 2 * pi * t + offset) * magnitude


def square_wave(t, frequency, offset, magnitude):
    # type: (ndarray, float, float, float, float) -> ndarray
    return signal.square(frequency * 2 * pi * t + offset) * magnitude


def saw_wave(t, frequency, offset, magnitude):
    # type: (ndarray, float, float, float, float) -> ndarray
    return signal.sawtooth(frequency * 2 * pi * t + offset) * magnitude

