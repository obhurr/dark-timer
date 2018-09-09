#!/usr/bin/python
# -*- coding: utf-8 -*-
from Adafruit_LED_Backpack import SevenSegment
from time import time, sleep, strftime, gmtime

global segment

segment = SevenSegment.SevenSegment(address=0x70)
segment.begin()
segment.set_brightness(0)

def Slot_disp():
    ## Continually update the time on a 4 char, 7-segment display
    global segment

    x = 0

    while True:
        segment.clear()
        segment.set_digit(0, x)     # Tens
        segment.set_digit(1, x)       # Ones
        segment.set_digit(2, x)   # Tens
        segment.set_digit(3, x)    # Ones
        segment.set_colon(False)
        segment.write_display()

        if x == 9:
            x = 0
        else:
            x = x + 1
        sleep(0.05)

Slot_disp()
