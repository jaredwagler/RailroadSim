# ProtoThrottle Bridge for ESU & JMRI

## Overview

This project is a protocol bridge, designed to connect the Iowa Scaled Engineering [ProtoThrottle](http://www.protothrottle.com) to [ESU CabControl DCC command stations](http://www.esu.eu/en/products/digital-control/cabcontrol/) or to JMRI WiFi Throttle (aka WiThrottle or Engine Driver) servers.  Written in python, the code is intended to execute on a Raspberry Pi or similar with an XBee attached to the USB port via an FTDI serial adapter.  The network side - wired or wireless - should be configured to connect to either the ESU CabControl (either via the ESU's built-in wifi access point, or both plugged into the same wired network) or whatever local network the JMRI WiThrottle server is running on.  However, this code was largely written and tested running on a desktop Linux machine, and should run similarly well on any modern Linux distro with the appropriate python packages installed.

Configuration is done via protothrottle.ini, as described below.

## Dependencies

There aren't a lot of dependencies, but the two you may not have will be serial and pySerial, both installable through pip.

## Configuration

### Command Line Options

All configuration options are optional.

`-s or --serial` - Specify the serial port (eg. "/dev/ttyUSB1") that the XBee/FTDI adapter can be found on.  If not specified, the code will auto-detect FTDI-based adapters and choose the first one.

`-i or --server_ip` - Specify the IP address of the ESU command station or the WiThrottle server.  Overrides configuration file and autodetect if specified.

`-p or --server_port` - Specify the listening port of the ESU command station or the WiThrottle server.  Overrides configuration file and autodetect if specified.

`-c or --config` - Specify the full location (eg. "/home/myuser/somedir/someotherdir/myconfig.ini") of the configuration ini file.  By default, it looks for a file called protothrottle.ini in the directory it's executed from.

`-g or --gitver` - Specify up to six characters of the git revision.  This allows an identifying portion of the hash to be transmitted in the status packets back to the ProtoThrottles, so that they can display it to the user.  This is used to help the user identify what version of the esu-bridge code is being run.

### Configuration INI Options

A default protothrottle.ini is included in the projects.  I'd start by having a look at that - it's pretty self-explanatory.  It should have a single section - "configuration".

`mode` - Set to 'esu' for ESU CabControl command stations, or 'withrottle' for JMRI WiThrottle servers

`baseAddress` - A number between 0-15 corresponding to the base address that is configured in the ProtoThrottles talking to this base unit.  Only PTs configured to the same base address will communicate with the base.  (In reality, this is added to a base MRBus address of 0xD0.)

`searchDelay` - When searching the connected network for ESU or Withrottle servers, how long to wait (in seconds) for each to respond.  This defaults to 0.03 seconds, which is typically adequate without incurring undue slowness.

`packetTimeout` - Time (in seconds) before a ProtoThrottle is considered dead and any locomotives being controlled by it are brought to a halt.  (Doesn't actually work yet.)

`serverIP` - Specify the server address for the ESU command station or WiThrottle server (depending on how mode is set).  Will override autodetect, but will be overriden by command line parameters.

`serverPort` - Specify the server port on which the ESU command station or WiThrottle server is listening.  If not specified, ESU defaults to port 15471, and WiThrottle defaults to 12090.  Will override autodetect, but will be overriden by command line parameters.

## Running

`pi-start-esubridge.sh` - This is the script that runs on the RasPi for our actual protocol bridge sold for the ProtoThrottles.  It's hard-coded to certain paths in our particular Raspbian image.

`test-start-esubridge.sh` - This is probably the one you actually want to run.  This is how I invoke it on my desktop to test changes, and is set up to invoke everything from the current directory.  It does, however, assume that the current directory is a git repo.

## License

Copyright (C) 2018 Nathan Holmes & Michael Petersen, with mrbus.py by Nathan Holmes and Mark Finn
    
This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

