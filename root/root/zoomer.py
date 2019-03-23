#!/usr/bin/env python

from RPi import GPIO
import time
import os
import subprocess
import sys

os.environ['DISPLAY'] = ':0.0'

colorSwitch = 22
clk = 17
dt = 18
sw = 27

tmpFileName = '/tmp/grayscale'
mpvID = 0

def getMpvID():
    while True:
        result = subprocess.run(['xdotool', 'search', '--name', 'mpv'], stdout=subprocess.PIPE)
        if result.returncode == 0:
            mpvID = result.stdout.decode().splitlines()[0]
            return
        time.sleep(0.5)

def initMpv():
    getMpvID()
    time.sleep(10)
    subprocess.run(['xdotool', 'key', '--clearmodifiers', '--window', str(mpvID), 'Up'])
    time.sleep(1)
    subprocess.run(['xdotool', 'key', '--clearmodifiers', '--window', str(mpvID), 'Up'])
    time.sleep(1)
    subprocess.run(['xdotool', 'key', '--clearmodifiers', '--window', str(mpvID), 'Up'])

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(colorSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

counter = 0
pressed = False
clkLastState = GPIO.input(clk)

lastProbe = GPIO.input(colorSwitch) == 0
with open(tmpFileName, 'w') as tmpFile:
    tmpFile.write(str(lastProbe))

initMpv()

try:
    while True:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
                if counter % 2 == 0:
                    subprocess.run(['xdotool', 'key', '--clearmodifiers', '--window', str(mpvID), 'Alt+minus'])
            else:
                counter -= 1
                if counter % 2 == 0:
                    subprocess.run(['xdotool', 'key', '--clearmodifiers', '--window', str(mpvID), 'Alt+plus'])

            if counter == 4000 or counter == -4000:
                counter = 0
            clkLastState = clkState


        if GPIO.input(sw):
            pressed = False
        elif not pressed:
            pressed=True
            subprocess.run(['xdotool', 'key', '--clearmodifiers', '--window', str(mpvID), 'Alt+BackSpace'])
            counter=0


        probe = GPIO.input(colorSwitch) == 0
        if probe != lastProbe:
            with open(tmpFileName, 'w') as tmpFile:
                tmpFile.write(str(probe))
            # wait for an instance to be started up
            getMpvID()
            subprocess.run(['killall', 'xinit'])
            lastProbe = probe
            initMpv()

        time.sleep(0.001)
finally:
        GPIO.cleanup()

