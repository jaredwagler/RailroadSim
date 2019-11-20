#Purpose is to read all sensor data and make into a single format that other scripts can use
#Created by: Daniel Keats
#Updated on: 11/1/2019

import RPi.GPIO as GPIO
import time
import spidev
import board
import busio
import digitalio
import threading
import pygame.mixer as sound
import adafruit_mcp3xxx.mcp3008 as MCP
import gui
import withrottle
from pyky040 import pyky040
from adafruit_mcp3xxx.analog_in import AnalogIn

GPIO.setmode(GPIO.BCM) #now we can use easy numbers

#We are going to declare all of our items and their GPIO pins
directionF = 12
directionB = 16
encoder1CLK = 18
encoder1DT = 23
horn = 20
bell = 21
throttle_0 = 4
throttle_1 = 17
throttle_2 = 27
throttle_3 = 22
throttle_4 = 5
throttle_5 = 6
throttle_6 = 13
throttle_7 = 0 #UPDATE: PIN NUMBER
throttle_8 = 26
eBrake = None #get value for emergency brake
mute = None #get value for sound mute

# Get sound
sound.init()
mfSound = sound.Sound("mf.wav")
hornSound = sound.Sound("horn.wav")
bellSound = sound.Sound("bell.wav")
channel1 = sound.Channel(0)
channel2 = sound.Channel(1)
channel3 = sound.Channel(3)
channel1.play(mfSound)

# Declaration of commands and their corresponding function number
cmdBell = 1
cmdHorn = 2
cmdMute = 8
cmdEmergency = 15
cmdDirection = 29

#Inital values because Java is better
lastThrottlePosition = 0
lastDirection = None
speedVal = 0
brake = 0

#Handy dandy lists to make life easier
sensors = (directionF, directionB, encoder1CLK, encoder1DT, encoder2CLK, encoder2DT, horn, bell, throttle_0, throttle_1, throttle_2, throttle_3, throttle_4, throttle_5, throttle_6, throttle_7, throttle_8)
throttle = (throttle_0, throttle_1, throttle_2, throttle_3, throttle_4, throttle_5, throttle_6, throttle_7, throttle_8)
direction = (directionF, directionB)#Ya this one is kind of pointless
speedLst = (0,15,30,40,50,70,85,100,127)

#Declaration of values pulled from the gui
serverIP = ""
locAddr = ""
guiInput = gui.userGui()

#Gui prompt
while ((serverIP == "") and (locAddr == "")):
    serverIP, locAddr = guiInput.returnValues()

#Music stop
channel1.stop()

#Connection Code
conPoint = None
serverPort = 12090
conPoint = withrottle.WiThrottleConnection()
conPoint.connect(serverIP, serverPort)
throttleAddr = 13
locAddrLong = True #idk it's a fucking boolean check on MRBusThrottle
locObjID = conPoint.locomotiveObjectGet(int(locAddr), throttleAddr, locAddrLong)
#Just gonna set everything to be inputs
for pin in sensors:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def getThrottlePosition(): #returns the position of the throtle else None
    for position, pin in enumerate(throttle):
        if GPIO.input(pin):
            return position
    return None #inbetween throttle positions

def getDirection():
    direction = round(chan.voltage * 100 / 3.3)
    if direction < someNumber: #Figure out the numbers 
        direction = 1
    elif direction > someDifferentNumber:
        direction = 0
    else:
        conPoint.locomotiveSpeedSet(locObjID,0, 0)
    return 0

def getLights(scale_position):
    if scale_position >= 0 and scale_position < 25:
        conPoint.locomotiveFunctionSet(locObjID, 0, 0)
        conPoint.locomotiveFunctionSet(locObjID, 7, 0)
        conPoint.locomotiveFunctionSet(locObjID, 9, 0)
    elif scale_position >= 25 and scale_position < 50:
        conPoint.locomotiveFunctionSet(locObjID, 0, 1)
        conPoint.locomotiveFunctionSet(locObjID, 7, 1)
        conPoint.locomotiveFunctionSet(locObjID, 9, 0)
    elif scale_position >= 50 and scale_position < 75:
        conPoint.locomotiveFunctionSet(locObjID, 0, 1)
        conPoint.locomotiveFunctionSet(locObjID, 7, 0)
        conPoint.locomotiveFunctionSet(locObjID, 9, 0)
    elif scale_position >= 75 and scale_position < 100:
        conPoint.locomotiveFunctionSet(locObjID, 0, 1)
        conPoint.locomotiveFunctionSet(locObjID, 7, 0)
        conPoint.locomotiveFunctionSet(locObjID, 9, 1)

#Encoder Code
encoder1 = pyky040.Encoder(encoder1CLK, encoder1DT)
encoder1.setup(scale_min=0, scale_max=100, step=10, chg_callback=getHeadLights)
thread1 = threading.Thread(target=encoder1.watch)
thread1.start()

#Potentiometer Code
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.CE0)
mcp = MCP.MCP3008(spi, cs)
chan = AnalogIn(mcp, MCP.P0)
cs2 = digitalio.DigitalInOut(board.CE1) #UPDATE: CHECK PIN
mcp2 = MCP.MCP3008(spi, cs2) #UPDATE: CHECK PIN
chan2 = AnalogIn(mcp2, MCP.P1) #UPDATE: CHECK PIN
#Horn and bell variables
hornState = False
bellState = False
lastHornState = False
bellOn = False
bellIdle = False

while True:
    hornState = not GPIO.input(horn)
    if hornState and not lastHornState: #plays horn sound when button is pushed
        channel2.play(hornSound)
        conPoint.locomotiveFunctionSet(locObjID, 2, 1)
        lastHornState = True
    elif not hornState and lastHornState: #stops horn sound
        channel2.stop()
        conPoint.locomotiveFunctionSet(locObjID, 2, 0)
        lastHornState = False

    bellState = not GPIO.input(bell)
    if bellState and not bellOn and bellIdle: #toggles bell sound on
        channel3.play(bellSound)
        conPoint.locomotiveFunctionSet(locObjID, 1, 1)
        bellOn = True
        bellIdle = False
    elif not bellState: #sets idle value
        bellIdle = True
    elif bellState and bellOn and bellIdle: #toggles bell sound off
        channel3.stop()
        conPoint.locomotiveFunctionSet(locObjID, 1, 0)
        bellOn = False
        bellIdle = False

    currentThrottlePosition = getThrottlePosition()#get position from buttons
    if currentThrottlePosition == None: #Check to see if we are inbetween positions, if so keep last val
        throttleVal = lastThrottlePosition
    else:
        lastThrottlePosition = currentThrottlePosition
        throttleVal = currentThrottlePosition #if diff update new value
    brake = round(chan.voltage * 127 / 3.3)
    if speedLst[throttleVal] < brake:
        speedVal = 0
    else:
        speedVal = speedLst[throttleVal] - brake
    currentDirection = getDirection() #gets direction else none, 0 = forward, 1 = backwards, None = neutral
    if currentDirection == None:
        directionVal = lastDirection
    else:
        lastDirection = currentDirection
        directionVal = currentDirection
    conPoint.locomotiveSpeedSet(locObjID,speedVal, currentDirection)
    conPoint.update()
    time.sleep(0.2)
