import threading
import time

import pyaudio

import utils



class Audio:
    def __init__(self, sig_gen, repeat=10):
        self.sig_gen = sig_gen
        self.repeat = repeat
        self.playing = True

    def start_audio(self):
        thread = threading.Thread(target=self._play_audio)
        thread.start()

    def stop_audio(self):
        self.playing = False

    def callback(self, in_data, frame_count, time_info, status):
        data = self.sig_gen.generate_tone(frame_count)
        return (data, pyaudio.paContinue)

    def _play_audio(self):

        pya = pyaudio.PyAudio()
        stream = pya.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sig_gen.sample_rate,
            output=True,
            stream_callback=self.callback
        )
        stream.start_stream()

        while self.playing and stream.is_active():
            time.sleep(0.1)

        stream.stop_stream()
        stream.close()
        pya.terminate()
