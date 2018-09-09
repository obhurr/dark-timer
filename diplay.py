#!/usr/bin/python
# -*- coding: utf-8 -*-
from Adafruit_LED_Backpack import SevenSegment
from time import time, sleep, strftime, gmtime
import threading

global segment

segment = SevenSegment.SevenSegment(address=0x70)
segment.begin()
segment.set_brightness(0)



def Slot_disp():
    ## Continually update the time on a 4 char, 7-segment display
    global segment
    x = 9
    y = 0
    while x >= 0:
        segment.clear()
        segment.set_digit(0, x)     # Tens
        segment.set_digit(1, x)       # Ones
        segment.set_digit(2, x)   # Tens
        segment.set_digit(3, x)    # Ones
        segment.set_colon(False)
        segment.write_display()

        x = x - 1
        y = y + 0.05
        sleep(y)

Slot_disp()
