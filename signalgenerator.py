import numpy as np

class SignalGenerator:
    def __init__(self, waves, crossfade=5, sample_rate=22050):
        # type: (list) -> SignalGenerator
        self.waves = waves
        self.sample_rate = sample_rate
        self.frequency = 440.0
        self.volume = 1.0
        self.last_sample = 0.0
        self.crossfade = crossfade

    def generate_wavetable(self, width, height, repeat=1):
        magnitude = float(height)/2.0 - (float(height)/16.0)
        frequency = 1.0/float(width)*float(repeat)
        t = np.arange(1, width, 1)
        combined = None
        for wave in self.waves:
            gen = wave.generate_wave(t, frequency)
            if combined is None:
                combined = gen
            else:
                combined += gen
        combined *= magnitude
        return combined

    def generate_tone(self, frame_count):
        combined = None
        t = np.arange(0.0, float(frame_count)/self.sample_rate, 1.0/self.sample_rate)
        for wave in self.waves:
            if combined is None:
                combined = (wave.generate_wave(t, self.frequency) * wave.magnitude)
            else:
                combined += (wave.generate_wave(t, self.frequency) * wave.magnitude)
        combined = (combined * self.volume).astype(np.float32)
        self.last_sample = combined[frame_count-1]
        return combined
