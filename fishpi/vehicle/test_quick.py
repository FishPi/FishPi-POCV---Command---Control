#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Simple test of PWM motor and servo drive
#
import logging
import raspberrypi

from time import sleep
from drive_controller import AdafruitDriveController

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    logger.addHandler(console)

    print "testing drive controller..."
    drive = AdafruitDriveController(debug=True, i2c_bus=raspberrypi.i2c_bus())

    print "run ahead..."
    drive.set_throttle(0.5)
    sleep(0.5)
    drive.set_throttle(1.0)
    sleep(0.5)
    drive.set_throttle(0.5)
    sleep(2)

    print "run 0%..."
    drive.set_throttle(-1.0)
    sleep(2)
    drive.set_throttle(0.0)
    sleep(2)

    print "run reverse for 2 sec"
    drive.set_throttle(-0.5)
    sleep(0.5)
    drive.set_throttle(-1.0)
    sleep(2)
    
    print "and back to neutral..."
    drive.set_throttle(0.0)
    sleep(5)

