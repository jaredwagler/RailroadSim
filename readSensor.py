#Purpose is to read all sensor data and make into a single format that other scripts can use
#Created by: Daniel Keats
#Updated on: 09/17/2019

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
eBrake = None #get value for emergency brake
mute = None #get value for sound mute

# Declaration of commands and their corresponding number
cmdBell = 1
cmdHorn = 2
cmdMute = 8
cmdEmergency = 15
cmdDirection = 29

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


#Enconder initalization
encoder1 = KY040(encoder1CLK, encoder1DT, rotaryCallback=rotaryChange)
encoder2 = KY040(encoder2CLK, encoder2DT, rotaryCallback=rotaryChange)
encoder1.start()
encoder2.start()

while True: #main shit, should make it callable at a later point
    hornState = GPIO.input(horn)-
	if hornState:
		esu_send(cmdHorn,1) #send command
    else:
        esu_send(cmdHorn,0) #send command

    bellState = GPIO.input(bell)
	if bellState:
		esu_send(cmdBell,1) #send command
    else:
        esu_send(cmdBell,0) #send command

	if eBrake:
		esu_send(cmdEmergency,1) #send command
    else:
        esu_send(cmdEmergency,0) #send command

	if mute:
		esu_send(cmdMute,1) #send command
    else:
        esu_send(cmdMute,0) #send command
    currentThrottlePosition = getThrottlePosition()#sets throttle speed
    throttle_send(currentThrottlePosition) #sends throttle speed
    if currentThrottlePosition == None: #maintains throttle value when inbetween positions
        throttleVal = lastThrottlePosition
    else:
        lastThrottlePosition = currentThrottlePosition
        throttleVal = currentThrottlePosition

    currentDirection = getDirection() #gets direction else none, 0 = forward, 1 = backwards, None = neutral
    esu_send(cmdDirection,currentDirection) #sends direction to function

    if currentDirection == None:
        directionVal = lastDirection
    else:
        lastDirection = currentDirection
        directionVal = currentDirection

    speedVal = speedLst[throttleVal]

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
