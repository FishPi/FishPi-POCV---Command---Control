#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Simple test of PWM motor and servo drive
#

import raspberrypi

from time import sleep
from drive_controller import AdafruitDriveController

if __name__ == "__main__":
    print "stopping drive controller..."
    drive = AdafruitDriveController(debug=True, i2c_bus=raspberrypi.i2c_bus())

    drive.set_throttle(0.0)
    drive.set_steering(0.0)

