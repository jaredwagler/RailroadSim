# *************************************************************************
# Title:    Client for ESU CabControl DCC System Network Interface
# Authors:  Michael D. Petersen <railfan@drgw.net>
#           Nathan D. Holmes <maverick@drgw.net>
# File:     esu.py
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
#   This class provides a way to interface with an ESU CabControl system
#   in order to provide basic functionality, like acquiring locomotives and
#   then setting speed, direction, and function outputs.
# 
#   Many thanks to ESU for providing the protocol documentation that allowed
#   this to be developed.  Thankfully, while I don't speak German, Google 
#   Translate does rather well.
# 
# *************************************************************************

import socket
import re

class ESUConnection:
   """An interface to talk to an ESU CabControl command station via the network in order to
      control model railway locomotives via DCC or other supported protocols."""
   conn = None

   # Define a few constants - the ESU port is always 15471
   ESU_PORT = 15471
   ESU_RCV_SZ = 1024

   # Some pre-compiled regexs used in response parsing
   REglobalList = re.compile("(?P<objID>\d+)\s+addr\[(?P<locAddr>\d+)\].*")
   RElocAdd = re.compile("10\s+id\[(?P<objID>\d+)\].*")
   
   def __init__(self):
      """Constructor for the object.  Any internal initialization should occur here."""
      pass
     
   def connect(self, ip, port = None):
      """Connect this object to an ESU CabControl command station on the IP address specified."""
      if port is None:
         port = self.ESU_PORT
      print "ESU Trying to connect to %s on port %d" % (ip, port)
      try:
         self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         self.conn.connect((ip, port))
         print "ESU Command station connection succeeded"
      except:
         print "ESU Command station connection failed"
      
   def disconnect(self):
      """Disconnect from the CabControl command station in a clean way."""
      print "ESU Disconnecting"
      try:
         self.conn.close()
         print "ESU Command station connection closed successfully"
      except:
         print "ESU Command station connection closed with exception, ignoring"
      self.conn = None
      
   def esuTXRX(self, cmdStr, parseRE=None, resultKey=''):
      """Internal shared function for transacting with the command station."""
      self.conn.send(cmdStr)
      resp = self.conn.recv(self.ESU_RCV_SZ)
      # Find the response
      lines = resp.splitlines()
      numDataElements = len(lines)
      if (lines[0] != "<REPLY %s>" % (cmdStr)):
         print "ESU: YIKES!  Reply malformed!"
      if (lines[numDataElements-1] != "<END 0 (OK)>"):
         print "ESU: Got an error back, parsing..."
      
      if parseRE is None:
         return {}
      
      results = { }
      for idx in range(1, numDataElements-1):
         try:
            parsed = parseRE.match(lines[idx])

            if resultKey == "":
               results[len(results)] = parsed.groupdict()
            else:
               results[parsed.group(resultKey)] = parsed.groupdict()
         except:
            print "ESU esuRXTX Line %d does not match regex\n  Line %d: '%s'" % (idx, idx, lines[idx])

      return results

   def esuLocomotiveAdd(self, locoNum, locoName=""):
      """Internal function for adding a locomotive to the command station's object table."""
      cmdStr = "create(10, addr[%d], append)" % ( int(locoNum))
      result = self.esuTXRX(cmdStr, self.RElocAdd)
      return int(result[0]['objID'])

   def locomotiveObjectGet(self, locoNum, cabID, isLongAddress):
      """Acquires and returns a handle that will be used to control a locomotive address."""
      print "ESU locomotiveObjectGet(%d, 0x%02X)" % (locoNum, cabID)
      
      cmdStr = "queryObjects(10,addr)"
      locoList = self.esuTXRX(cmdStr, self.REglobalList, 'locAddr')
      
      locAddr = "%d" % (int(locoNum))
      
      if locAddr in locoList.keys():
         objID = int(locoList[locAddr]['objID'])
         print "Found locomotive %s at object %d" % (locAddr, objID)
         return objID
      else:
         print "Need to add this locomotive"
         objID = self.esuLocomotiveAdd(locoNum)
         print "Added locomotive %s at object %d" % (locAddr, objID)
         return objID
         
   def locomotiveEmergencyStop(self, objID):
      """Issues an emergency stop command to a locomotive handle that has been previously acquired with locomotiveObjectGet()."""
      objID = int(objID)
      cmdStr = "set (%d, stop)" % (objID)
      self.esuTXRX(cmdStr)
      

   # For the purposes of this function, direction of 0=forward, 1=reverse
   def locomotiveSpeedSet(self, objID, speed, direction=0):
      """Sets the speed and direction of a locomotive via a handle that has been previously acquired with locomotiveObjectGet().  
         Speed is 0-127, Direction is 0=forward, 1=reverse."""
      objID = int(objID)
      speed = int(speed)
      direction = int(direction)
      
      if direction != 0 and direction != 1:
         speed = 0
         direction = 0
      
      if speed >= 127 or speed < 0:
         speed = 0

      cmdStr = "set(%d, speed[%d], dir[%d])" % (objID, speed, direction)
      self.esuTXRX(cmdStr)
      
      print "ESU locomotiveSpeedSet(%d): set speed %d %s" % (objID, speed, ["FWD","REV"][direction])
   
   def locomotiveFunctionSet(self, objID, funcNum, funcVal):
      """Sets or clears a function on a locomotive via a handle that has been previously acquired with locomotiveObjectGet().  
         funcNum is 0-28 for DCC, funcVal is 0 or 1."""
      objID = int(objID)
      funcNum = int(funcNum)
      funcVal = int(funcVal)
     
      cmdStr = "set(%d, func[%d,%d])" % (objID, funcNum, funcVal)
      self.esuTXRX(cmdStr)   

   def locomotiveFunctionDictSet(self, objID, funcDict):
      """Don't use this!  An effort to set multiple functions at a time that doesn't really work yet."""
      objID = int(objID)
      funcStr = ""
      for funcNum in funcDict:
         funcNum = int(funcNum)
         funcVal = int(funcDict[funcNum])
         
         funcStr = funcStr + ", func[%d,%d]" % (funcNum, funcVal)
     
      cmdStr = "set(%d%s])" % (objID, funcStr)
      self.esuTXRX(cmdStr)
      
      print "ESU locomotiveFunctionSet(%d): set func %d to %d" % (int(objID), funcNum, funcVal)

   def locomotiveDisconnect(self, objID):
      print "ESU locomotiveDisconnect(%d): disconnect" % (int(objID))
 
   def locomotiveFunctionsGet(self, objID):
     print "ESU locomotiveFunctionsGet(%d)" % (int(objID))
     print " ...isn't implemented yet\n"
     return [0] * 29

   def update(self):
      """This should be called frequently within the main program loop.  While it doesn't do anything for ESU,
         other command station interfaces have housekeeping work that needs to be done periodically."""
      return

   
   
   
