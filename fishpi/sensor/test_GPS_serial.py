#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#

import serial

DEVICE = "/dev/ttyAMA0"
BAUD = 9600

def test_GPS():
	ser = serial.Serial(DEVICE, BAUD)
	ser.readline()


