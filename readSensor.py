#Purpose is to read all sensor data and make into a sigle format that other scripts can use
#Created by: Daniel Keats
#Updated on: 09/07/2019

import RPi.GPIO as GPIO
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from ky040.KY040 import KY040

GPIO.setmode(GPIO.BCM) #now we can use easy numbers

#We are going to declare all of our items and their GPIO pins
directionF = 12
directionB = 16
encoder1CLK = 18
encoder1DT = 23
encoder2CLK = 24
encoder2DT = 25
horn = 20
bell = 21
throttle_0 = 4
throttle_1 = 17
throttle_2 = 27
throttle_3 = 22
throttle_4 = 5
throttle_5 = 6
throttle_6 = 13
throttle_7 = 19
throttle_8 = 26

sensors = (directionF, directionB, encoder1CLK, encoder1DT, encoder2CLK, encoder2DT, horn, bell, throttle_0, throttle_1, throttle_2, throttle_3, throttle_4, throttle_5, throttle_6, throttle_7, throttle_8)
throttle = (throttle_0, throttle_1, throttle_2, throttle_3, throttle_4, throttle_5, throttle_6, throttle_7, throttle_8)
direction = (directionF, directionB)
speedLst = (0,15,30,40,50,70,85,100,127)

#Just gonna set everything to be inputs
for pin in sensors:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lastThrottlePosition = 0
lastDirection = None
speedVal = 0

#Analog to Digital initalization
spi = busio.SPI(clock = board.SCK, MISO = board.MSIO, MOSI = board.MOSI)
cs = digitalio.DigitalInOut(board.SPI01) #Might need to change this. You can use dir(board) on th Pi to figure out the pins.
chan0 = AnalogIn(mcp, MCP.P0)
last_read = 0
tolerance = 250

#Enconder initalization
encoder1 = KY040(encoder1CLK, encoder1DT, rotaryCallback=rotaryChange)
encoder2 = KY040(encoder2CLK, encoder2DT, rotaryCallback=rotaryChange)
encoder1.start()
encoder2.start()

while True: #main shit, should make it callable at a later point
    hornState = GPIO.input(horn)
    bellState = GPIO.input(bell)

    currentThrottlePosition = getThrottlePosition()#sets throttle speed
    if currentThrottlePosition == None: #maintains throttle value when inbetween positions
        throttleVal = lastThrottlePosition
    else:
        lastThrottlePosition = currentThrottlePosition
        throttleVal = currentThrottlePosition

    currentDirection = getDirection() #gets direction else none, 0 = forward, 1 = backwards, None = neutral
    if currentDirection == None:
        directionVal = lastDirection
    else:
        lastDirection = currentDirection
        directionVal = currentDirection

    speedVal = speedLst[throttleVal]

    trim_pot_changed = False
    trim_pot = chan0.values
    pot_adujust = abs(trim_pot - last_read)
    if pot_adjust > tolerance:
        trim_pot_changed = True
    if trim_pot_changed:
        set_potentiometer = remap_range(trim_pot, 0,65535, 0, 100) #Change 100 to max range that we want
        last_read = trim_pot

def getThrottlePosition(): #returns the position of the throtle else None
    for position, pin in enumerate(throttle):
        if not GPIO.input(pin):
            return position
    return None #inbetween throttle positions

def getDirection():
    for position, pin in enumerate(direction):
        if not GPIO.input(pin):
            return position
    return None #train is in netural
def rotaryChange(direction): #Input info here for encoders
    print direction

def remap_range(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min
    valueScaled = int(value - left_min) / int(left_span)
    return int(right_min + (valueScaled * right_span))
