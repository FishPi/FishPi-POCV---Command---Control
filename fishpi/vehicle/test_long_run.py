#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Simple test of PWM motor and servo drive
#

import raspberrypi

from time import sleep
from datetime import datetime
from drive_controller import AdafruitDriveController

if __name__ == "__main__":
    print "testing drive controller..."
    drive = AdafruitDriveController(debug=True, i2c_bus=raspberrypi.i2c_bus())

    print "run full ahead..."
    drive.set_throttle(1.0)

    while True:
        with open('/home/fishpi/logs/long_test.txt', 'w') as f:
            f.write(datetime.now().isoformat())
            f.write('\r\n')
        sleep(5)
   
