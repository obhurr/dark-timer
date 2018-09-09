#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from subprocess import call
from gpiozero import *
from time import time, sleep, strftime, gmtime
from datetime import datetime, timedelta
from multiprocessing import Pool
import Queue
import threading
from Adafruit_LED_Backpack import SevenSegment


global segment
segment = SevenSegment.SevenSegment(address=0x70)
segment.begin()
brightness = 0
segment.set_brightness(brightness)


eventq = Queue.Queue()

Enc_A = Button(16) # Rotary encoder pin A
Enc_B = Button(20) # Rotary encoder pin B
Opp = Button(13)
Ned = Button(19)
Hoyre = Button(6, hold_time=2)
Vensre = Button(5)
Rele = LED(21)
Tute = LED(26)

set_time = 15
hold_time = 2

global timeOfStart
timeOfStart = datetime.now() # bare for å sette type

def PwrOff():
    diff = 0
    Single = True
    start_time = time()
    while Vensre.is_active and Single :
        if Enc_B.is_pressed or Enc_A.is_pressed:
            Single = False
        else:
            now_time=time()
            diff=-start_time+now_time

    if diff < 10 and Single:
        Face_disp()
        while True:
            if Ned.is_pressed:
                Update_disp(set_time)
            elif Opp.is_pressed:
                call("sudo nohup shutdown -h now", shell=True)


def Enc_A_rising():
    if Enc_B.is_pressed:
        if Ned.is_pressed:
            eventq.put(-0.1)
        elif Opp.is_pressed:
            eventq.put(-10)
        elif Vensre.is_pressed:
            eventq.put(-1000)
        else:
            eventq.put(-1)

def Enc_B_rising():
    if Enc_A.is_pressed:
        if Ned.is_pressed:
            eventq.put(0.1)
        elif Opp.is_pressed:
            eventq.put(10)
        elif Vensre.is_pressed:
            eventq.put(1000)
        else:
            eventq.put(1)

def utgang():
    diff = 0
    start_time = time()
    while Hoyre.is_active and (diff < hold_time) :
        now_time=time()
        diff=-start_time+now_time

    if diff < hold_time :
        belys()
    else:
        focus()


def Time_Done_Trigger(): #Utfort tid paa nedtelling
    global timeOfStart

    currentTime = datetime.now()
    stopTime = timeOfStart + timedelta(seconds=set_time) #sekunder
    stopTime = stopTime + timedelta(microseconds=(set_time % 1) * 1E6) #microsekunder
    TimeLeft = stopTime-currentTime

    if (TimeLeft.total_seconds()) > 0:
        threading.Timer(0.05, Time_Done_Trigger).start()
        Update_disp(TimeLeft.total_seconds())

    else:
        print "Deaktiverer utgang, {} sekunder ferdig".format(set_time)
        Rele.off()
        Blink_On()
        Update_disp(0)
        sleep(1)
        Update_disp(set_time)
        Blink_Off()

def reset_disp():
    Blink_On()
    sleep(1)
    Update_disp(set_time)
    Blink_Off()

def belys():
    global timeOfStart
    if Rele.is_lit:
        print "Avbryter - Deaktiverer utgang"
        timeOfStart = timeOfStart - timedelta(days=1)
        threading.Timer(0.05, Time_Done_Trigger).start()
    else:
        timeOfStart = datetime.now()
        Rele.on()
        threading.Timer(0.05, Time_Done_Trigger).start() #for display
        print timeOfStart

def focus():
    if Rele.is_lit:
        timeOfStart = timeOfStart - timedelta(days=1)
        threading.Timer(0.05, Time_Done_Trigger).start()
        print "Deaktiverer utgang"
    else:
        Rele.on()
        Lines_disp()
        print "Aktiverer utgang"

def beep(x):
    print "Aktiverer Tute"
    Tute.on()
    sleep(0.3)
    print "Deaktiverer Tute"
    Tute.off()

def beepStarter():
    pool = Pool(processes=1)              # Start a worker processes.
    result = pool.apply_async(beep, [300]) # pool.apply_async(beep, [300], callback)


def to_sek_time():
    print set_time
    n = set_time
    print n
    n = n - 2
    print n
    eventq.put(n)

def Update_disp(time):
    ## Continually update the time on a 4 char, 7-segment display
    global segment
    print(time)
    total_secs = time
    hours = total_secs // 3600

    secs_still_remaining = total_secs % 3600
    minutes =  secs_still_remaining // 60

    secs = secs_still_remaining  % 60
    secs = secs // 1

    print("Time: %s | hours = %s | minutes = %s | secs = %s" % (time, hours, minutes, secs))

    segment.clear()

    if time >= 60:
        segment.set_digit(0, int(minutes) // 10)     # Tens
        segment.set_digit(1, int(minutes) % 10)       # Ones
        segment.set_digit(2, int(secs) // 10)   # Tens
        segment.set_digit(3, int(secs) % 10)    # Ones
        segment.set_colon(True)
    else:
        segment.print_float(time, decimal_digits=2)
        segment.set_colon(False)


    segment.write_display()

def Lines_disp():
    ## Continually update the time on a 4 char, 7-segment display
    global segment

    segment.clear()

    segment.set_digit(0, "-")     # Tens
    segment.set_digit(1, "-")       # Ones
    segment.set_digit(2, "-")   # Tens
    segment.set_digit(3, "-")    # Ones
    segment.set_colon(False)

    segment.write_display()

def Face_disp():
    ## Continually update the time on a 4 char, 7-segment display
    global segment

    segment.clear()

    segment.set_digit(0, "F")     # Tens
    segment.set_digit(1, "A")       # Ones
    segment.set_digit(2, "C")   # Tens
    segment.set_digit(3, "E")    # Ones
    segment.set_colon(False)

    segment.write_display()

def Blink_On():
    global segment
    segment.set_blink(0x02)

def Blink_Off():
    global segment
    segment.set_blink(0x00)

def Slot_disp():
    ## Continually update the time on a 4 char, 7-segment display
    global segment
    x = 9
    y = 0.15
    while x >= 0:
        segment.clear()
        segment.set_digit(0, x)     # Tens
        segment.set_digit(1, x)       # Ones
        segment.set_digit(2, x)   # Tens
        segment.set_digit(3, x)    # Ones
        segment.set_colon(False)
        segment.write_display()

        x = x - 1
        y = y + 0.035
        sleep(y)

def Brigh(bright):
    segment.set_brightness(bright)

Enc_A.when_pressed = Enc_A_rising      # Register the event handler for pin A
Enc_B.when_pressed = Enc_B_rising      # Register the event handler for pin B
Hoyre.when_pressed = utgang
Vensre.when_pressed = PwrOff
#Opp.when_pressed = reset_time
#Ned.when_pressed = to_sek_time


print "Klar..."
Slot_disp()
Update_disp(set_time)


while True:
    value = eventq.get()
    if abs(value) >= 1000:
        print(value)
        brightness = brightness - (value // 1000)
        if brightness < 0:
            brightness = 0
        elif brightness > 15:
            brightness = 15
        Brigh(int(brightness))
    else:
        if not Rele.is_lit:

            set_time = set_time - value
            if set_time < 0:
                set_time = 0
            Update_disp(set_time)
            print(set_time)
