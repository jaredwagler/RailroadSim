#!/bin/bash
GIT_REV=`git rev-parse --short=6 HEAD`
/usr/bin/python esu-bridge.py --config ./protothrottle.ini --gitver $GIT_REV

