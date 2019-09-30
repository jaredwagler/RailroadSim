#Purpose is to read all sensor data and make into a single format that other scripts can use
#Created by: Daniel Keats
#Updated on: 09/24/2019

import RPi.GPIO as GPIO
import time
import busio
import digitalio
import board
import sendData
import threading
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from pyky040 import pyky040

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
throttle_4 = 0 #5 -Fix this Button
throttle_5 = 6
throttle_6 = 13
throttle_7 = 0 #19 - Fix this Button
throttle_8 = 26
eBrake = None #get value for emergency brake
mute = None #get value for sound mute

# Declaration of commands and their corresponding function number
cmdBell = 1
cmdHorn = 2
cmdMute = 8
cmdEmergency = 15
cmdDirection = 29

#Handy dandy lists to make life easier
sensors = (directionF, directionB, encoder1CLK, encoder1DT, encoder2CLK, encoder2DT, horn, bell, throttle_0, throttle_1, throttle_2, throttle_3, throttle_4, throttle_5, throttle_6, throttle_7, throttle_8)
throttle = (throttle_0, throttle_1, throttle_2, throttle_3, throttle_4, throttle_5, throttle_6, throttle_7, throttle_8)
direction = (directionF, directionB)#Ya this one is kind of pointless
speedLst = (0,15,30,40,50,70,85,100,127)

#Just gonna set everything to be inputs
for pin in sensors:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def getThrottlePosition(): #returns the position of the throtle else None
    for position, pin in enumerate(throttle):
        if GPIO.input(pin):
            return position
    return None #inbetween throttle positions
def getDirection():
    for position, pin in enumerate(direction):
        if GPIO.input(pin):
            return position
    return None #train is in netural
def getBrake(voltIn):
    return int((int(voltIn)/ int(65535)) * 127)
def getHeadLights(scale_position):
    return(scale_position)
def getBackLights(scale_position):
    return(scale_position)

#Inital values because Java is better
lastThrottlePosition = 0
lastDirection = None
speedVal = 0
brake = 0

#Enconder initalization
encoder1 = pyky040.Encoder(encoder1CLK, encoder1DT)
encoder1.setup(scale_min=0, scale_max=100, step=1, chg_callback=getHeadLights)
encoder2 = pyky040.Encoder(encoder2CLK, encoder2DT)
encoder2.setup(scale_min=0, scale_max=100, step=1, chg_callback=getBackLights)
thread1 = threading.Thread(target=encoder1.watch)
thread2 = threading.Thread(target=encoder2.watch)
thread1.start()
thread2.start()

#Analog to digital
spi = busio.SPI(clock=board.SCK, MISO = board.MISO, MOSI = board.MOSI)
cs = digitalio.DigitalInOut(board.D5) #Change pin number
mcp = MCP.MCP3008(spi, cs)
chan = AnalogIn(mcp, MCP.P0) #Change pin
last_read = 0
tolerance = 250 #Change to make the jitter or not jitter

while True: #main shit, should make it callable at a later point
    pot_value = chan.value
    pot_adjust = abs(pot_value - last_read)
    if pot_adjust > tolerance:
        brake = getbrake(pot_value)

    hornState = GPIO.input(horn)
    #esu_send(cmdHorn,hornState)#send command

    bellState = GPIO.input(bell)
	#esu_send(cmdBell,bellState) #send command

	#esu_send(cmdEmergency,eBrake) #send command

	#esu_send(cmdMute,mute) #send command

    currentThrottlePosition = getThrottlePosition()#get position from buttons
    if currentThrottlePosition == None: #Check to see if we are inbetween positions, if so keep last val
        throttleVal = lastThrottlePosition
    else:
        lastThrottlePosition = currentThrottlePosition
        throttleVal = currentThrottlePosition #if diff update new value
    speedVal = speedLst[throttleVal]
    #throttle_send(speedVal) #sends throttle speed

    currentDirection = getDirection() #gets direction else none, 0 = forward, 1 = backwards, None = neutral
    if currentDirection == None:
        directionVal = lastDirection
    else:
        lastDirection = currentDirection
        directionVal = currentDirection
    #esu_send(cmdDirection,directionVal) #sends direction to function
    time.sleep(0.2)
