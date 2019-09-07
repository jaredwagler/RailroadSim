#Purpose is to read all sensor data and make into a sigle format that other scripts can use
#Created by: Daniel Keats
#Updated on: 09/07/2019

import RPi.GPIO as GPIO
import time

#We are going to declare all of our items and their GPIO pins
directionF = 12
directionB = 16
encoder1CLK = 18
encoder1DT = 23
encoder2CLK = 24
encoder2DT = 25
horn = 20
bell = 21
t0 = 4
t1 = 17
t2 = 27
t3 = 22
t4 = 5
t5 = 6
t6 = 13
t7 = 19
t8 = 26

GPIO.setmode(GPIO.BCM) #really don't know what this does but it's here

#Just gonna set everything to be inputs
GPIO.setup(directionF, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(directionF, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoder1CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoder1DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoder2CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoder2DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(horn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(bell, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(t0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(t1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(t2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(t3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(t4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(t5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(t6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(t7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(t8, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lastThrottlePosition = 0

while True: #main shit
    currentThrottlePosition = getThrottlePosition()
    if currentThrottlePosition == 9: #maintains throttle value when inbetween positions
        throttle = lastThrottlePosition
    else:
        lastThrottlePosition = currentThrottlePosition

def getThrottlePosition():
    if GPIO.input(t0) == False:
        state = 0
    if GPIO.input(t1) == False:
        state = 1
    if GPIO.input(t2) == False:
        state = 2
    if GPIO.input(t3) == False:
        state = 3
    if GPIO.input(t4) == False:
        state = 4
    if GPIO.input(t5) == False:
        state = 5
    if GPIO.input(t6) == False:
        state = 6
    if GPIO.input(t7) == False:
        state = 7
    if GPIO.input(t8) == False:
        state = 8
    else:
        state = 9
    return state