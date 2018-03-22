# README #

## What is this? ##
Syntheremin is a project to build a Theremin-Synthesizer using a Raspberry Pi and some hardware.

You'll need scipy to run this, and I've been using minoconda on the raspberry pi.

## How do I set it up? ##
You'll need the following libraries installed from github:
    VL53L0X from https://github.com/johnbryanmoore/VL53L0X_rasp_python

You'll need the following libraries from pip:

| Package name      | PyPi link                                     |
| ----------------- | --------------------------------------------- |
| Adafruit_ADS1x15  | https://pypi.python.org/pypi/Adafruit-ADS1x15 |
| luma              | https://pypi.python.org/pypi/luma.core        |
| pillow            | https://pypi.python.org/pypi/Pillow           |
| pyayudio          | https://pypi.python.org/pypi/PyAudio          |
| pyserial          | https://pypi.python.org/pypi/pyserial         |


You'll also have to enable i2c communication on your Raspberry Pi.


![Syntheremin Image](https://raw.githubusercontent.com/aaronhourie/syntheremin/master/synth.png)