import numpy as np

"""
 Class which generates signals for audio and display in the form
 of 1d and 2d arrays.
"""

class SignalGenerator:
    def __init__(self, waves, crossfade=5, sample_rate=22050):
        # type: (list, int, int) -> SignalGenerator
        self.waves = waves
        self.sample_rate = sample_rate
        self.frequency = 440.0
        self.volume = 1.0
        self.last_sample = 0.0
        self.crossfade = crossfade

    # Generate a 2d "wavetable" for display purposes.
    def generate_wavetable(self, width, height, repeat=1):
        # type: (int, int, int) -> np.array
        # Determine a magnitude which will take up most of the screen.
        magnitude = float(height)/2.0 - (float(height)/16.0)
        # Determine a fequency which will repeat the chosen numer of times.
        frequency = 1.0/float(width)*float(repeat)
        # time series
        t = np.arange(1, width, 1)
        combined = None
        # Combine waveforms
        for wave in self.waves:
            gen = wave.generate_wave(t, frequency)
            if combined is None:
                combined = gen
            else:
                combined += gen
        # Adjust for magnitude
        combined *= magnitude
        return combined

    def generate_tone(self, frame_count):
        # type: (int) -> np.array
        combined = None
        # Generate a time series based on the signal generator's properties.
        t = np.arange(0.0, float(frame_count)/self.sample_rate, 1.0/self.sample_rate)
        # Combine all wave forms by summation
        for wave in self.waves:
            if combined is None:
                combined = (wave.generate_wave(t, self.frequency) * wave.magnitude)
            else:
                combined += (wave.generate_wave(t, self.frequency) * wave.magnitude)
        # Adjust for master volume
        combined = (combined * self.volume).astype(np.float32)
        # Keep track of last sample (will be used in the future for determining
        # the start point for the next set of samples)
        self.last_sample = combined[frame_count-1]
        return combined
