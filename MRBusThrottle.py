# *************************************************************************
# Title:    Client driver for MRBus Throttle (mainly the ProtoThrottle)
# Authors:  Michael D. Petersen <railfan@drgw.net>
#           Nathan D. Holmes <maverick@drgw.net>
# File:     MRBusThrottle.py
# License:  GNU General Public License v3
#
# LICENSE:
#   Copyright (C) 2018 Michael Petersen & Nathan Holmes
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
# DESCRIPTION:
#   This class provides a way parse incoming MRBus throttle packets (primarily
#   from the ProtoThrottle ( http://www.protothrottle.com/ ) and send them
#   on to a variety of command stations as a form of protocol translator.
#
# *************************************************************************

import mrbus
import sys
import time

class MRBusThrottle:

   def __init__(self, addr):
      self.locAddr = 0
      self.locAddrLong = True
      self.locSpeed = 0
      self.locDirection = 0
      self.locObjID = 0
      self.locEStop = 0
      self.locFunctions = None
      self.throttleAddr = addr
      self.lastUpdate = 0
      return

   def getLastUpdateTime(self):
      return self.lastUpdate

   def disconnect(self, cmdStn):
      cmdStn.locomotiveSpeedSet(self.locObjID, 0, 0)
      cmdStn.locomotiveDisconnect(self.locObjID)


   def update(self, cmdStn, pkt):
      if pkt.cmd != 0x53 or len(pkt.data) != 10:  # Not a status update, bump out
         return

      # print "MRBusThrottle (0x%02X): UPDATE loco %d" % (self.throttleAddr, self.locAddr)

      addr = pkt.data[0] * 256 + pkt.data[1] #dest*256+src
      if 0 != (addr & 0x8000): #Is this a signed int checker???? Needs further reseach.
         self.locAddrLong = False
         addr = addr & 0x007F
      else:
         self.locAddrLong = True

      speed = pkt.data[2] & 0x7F  #The speed value goes from 0-127 and if it goes above this it loops around so 128 would be 0.
      if 1 == speed: #Also negative values go backwards so -1 is 127
         speed = 0
         estop = 1
      elif speed > 1:
         estop = 0
         speed = speed - 1
      elif speed == 0:
         estop = 0

      if pkt.data[2] & 0x80: #If number is positive direction = 0; if number is negative direction = 1
         direction = 0
      else:
         direction = 1

      if (addr != self.locAddr): #sets the locAddr to the address found above
         self.locAddr = addr
         self.locObjID = cmdStn.locomotiveObjectGet(self.locAddr, self.throttleAddr, self.locAddrLong)
         print "MRBusThrottle (0x%02X): Acquiring new locomotive %d - objID = %s" % (self.throttleAddr, self.locAddr, self.locObjID)

      # Only send ESTOP if we just moved into that state
      if estop != self.locEStop and estop == 1:
         print "MRBusThrottle (0x%02X): Set ESTOP loco %d" % (self.throttleAddr, self.locAddr)
         cmdStn.locomotiveEmergencyStop(self.locObjID)

      self.locEStop = estop

      if self.locEStop != 1 and (speed != self.locSpeed or direction != self.locDirection):
         print "MRBusThrottle (0x%02X): Set loco [%d] speed %d %s" % (self.throttleAddr, self.locAddr, speed, ["FWD","REV"][direction])
         cmdStn.locomotiveSpeedSet(self.locObjID, speed, direction)

      self.locSpeed = speed
      self.locDirection = direction

      # On the first pass, get the function statuses from the command station
      # The LNWI / WiThrottle support this, others may in the future
      if self.locFunctions is None: #Checks if there is an array of functions.
         try: #Tries to acquire the functions from the command station
            self.locFunctions = cmdStn.locomotiveFunctionsGet(self.locObjID)
            print "MRBusThrottle (0x%02X): Got loco [%d] functions from cmd station" % (self.throttleAddr, self.locAddr)
            print self.locFunctions
         except Exception as e: #If it can't get the functions it sets all of them to 0
            print "MRBusThrottle (0x%02X): Exception in locomotiveFunctionsGet() for loco [%d]" % (self.throttleAddr, self.locAddr)
            self.locFunctions = [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ]

      functions = [ 0,0,0,0,0,0,0,0,0,0,
                       0,0,0,0,0,0,0,0,0,0,
                       0,0,0,0,0,0,0,0,0 ]

      for i in range(29):
         if i >= 0 and i < 8: # 0-7
            if pkt.data[6] & (1<<i): #& is a bitwise operator that compares two binary values and returns the similiarities. For example 9 & 1 would be 1 but 8 & 1 would be 0.
               functions[i] = 1
         elif i >= 8 and i < 16: #8-15
            if pkt.data[5] & (1<<(i-8)): # 1<<i is a bitwise operator that shifts a bit to the left i.e. 0100 would become 1000.
               functions[i] = 1
         elif i >= 16 and i < 24: #16-23
            if pkt.data[4] & (1<<(i-16)): #Need to find out what the range of data is coming through and make a table of possible values.
               functions[i] = 1
         elif i >= 24 and i < 29: #23-28
            if pkt.data[3] & (1<<(i-24)):
               functions[i] = 1

      for i in range(29):
         if functions[i] != self.locFunctions[i]: #updates the functions if they changed.
            print "MRBusThrottle (0x%02X): Set loco [%d] function [%d] to [%d]" % (self.throttleAddr, self.locAddr, i, functions[i])
            cmdStn.locomotiveFunctionSet(self.locObjID, i, functions[i]) #Goes to esu.py line 155

      self.locFunctions = functions

      self.lastUpdate = time.time()

      return
