import time
import threading
import RPi.GPIO as GPIO
import numpy as np

import VL53L0X
import Adafruit_ADS1x15 as adslib

from audio import Audio
from waveform import Waveform, sine_wave, saw_wave, square_wave
from signalgenerator import SignalGenerator

from PIL import Image

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

connected = True

TOF1_XSHUT = 27
TOF0_XSHUT = 17

ANALOG_GAIN=1

serial_oled = i2c(port=1, address=0x3c)
device_oled = sh1106(serial_oled)

sig_gen = None

def main():
    global sig_gen
    start_oled()
    tof0, tof1 = start_sensors()
    audio, sig_gen = start_audio()
    adc = start_adc()
    theremin_loop(tof0, tof1, audio, adc, sig_gen)

def theremin_loop(tof0, tof1, audio, adc, sig_gen):
    global connected
    try:
        timing = tof0.get_timing()
        if (timing < 20000):
            timing = 20000
        while connected:
            pitch = 150 + tof0.get_distance()
            volume = 2.0 - (float(tof1.get_distance()) / 100)
            analog_value = adc.read_adc(0, gain=ANALOG_GAIN) / 32000.0
            if pitch != 0 and pitch < 800:
                sig_gen.frequency = float(pitch)
            if volume > 0:
                sig_gen.volume= volume
            if analog_value > 0:
                sig_gen.waves[1].magnitude = analog_value
            time.sleep(timing/1000000.00)

    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Exiting...")
        connected = False
    finally:
        tof0.stop_ranging()
        tof1.stop_ranging()
        audio.stop_audio()


def start_audio():
    saw = Waveform(saw_wave)
    sine = Waveform(sine_wave)
    square = Waveform(square_wave)
    sine.magnitude = 0.7
    saw.magnitude = 0.3
    saw.offset = 0.1
    square.magnitude = 0.0
    square.offset = 0.3

    sig_gen = SignalGenerator([sine, saw, square])
    audio = Audio(sig_gen, 5)
    audio.start_audio()
    return audio, sig_gen


def start_sensors():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TOF0_XSHUT, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(TOF1_XSHUT, GPIO.OUT, initial=GPIO.LOW)

    # Keep all low for 500 ms or so to make sure they reset
    time.sleep(0.50)

    # Set new addresses.
    tof0 = VL53L0X.VL53L0X(address=0x2B)
    tof1 = VL53L0X.VL53L0X(address=0x2D)

    # Start ranging on TOF0
    GPIO.output(TOF0_XSHUT, GPIO.HIGH)
    time.sleep(0.50)
    tof0.start_ranging(VL53L0X.VL53L0X_HIGH_SPEED_MODE)

    # Start ranging on TOF1
    GPIO.output(TOF1_XSHUT, GPIO.HIGH)
    time.sleep(0.50)
    tof1.start_ranging(VL53L0X.VL53L0X_HIGH_SPEED_MODE)

    return tof0, tof1


def start_adc():
    adc = adslib.ADS1115()
    return adc

def start_oled():
    thread = threading.Thread(target=oled_loop)
    thread.start()

def oled_loop():
    global sig_gen
    while connected:
        if sig_gen is not None:
            with canvas(device_oled) as draw:
                draw_canvas(sig_gen, draw)
            time.sleep(1)


def draw_canvas(sig_gen, draw):

    wave_table = sig_gen.generate_wavetable(128, 64, 3)

    x = 0
    last_y = -1
    for y in wave_table:
        y = int(round(y)) + 32
        if y > 0:
            draw.point((x, y), fill="white")
            if last_y > 0 and abs(y - last_y):
                lower = min(last_y, y)
                upper = max(last_y, y)
                for interpolate in range(lower, upper):
                    draw.point((x, interpolate), fill="white")
            x += 1
        last_y = y


def millis():
    return int(round(time.time() * 1000))

if __name__ == "__main__":
    main()
