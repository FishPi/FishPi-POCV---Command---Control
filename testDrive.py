#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Simple test of PWM motor and servo drive
#

from time import sleep
from DriveController import DriveController

if __name__ == "__main__":
    print "testing drive controller..."
    drive = DriveController(debug=True)

    print "run full ahead for 10 sec..."
    drive.set_drive(1.0)
    sleep(10)
    
    print "run 50% ahead for 5 sec..."
    drive.set_drive(0.5)
    sleep(5)

    print "run 0% for 5 sec..."
    drive.set_drive(0.0)
    sleep(5)

    print "run 50% reverse for 5 sec"
    drive.set_drive(-0.5)
    sleep(5)
    
    print "run full reverse for 10 sec"
    drive.set_drive(-1.0)
    sleep(10)
    
    print "check out of bounds errors"
    try:
        drive.set_drive(15.0)
    except ValueError:
        print "caught 15"
    
    try:
        drive.set_drive(-10.0)
    except ValueError:
        print "caught -10"

    print "steer to port for 10 sec"
    drive.set_heading(-100)
    sleep(10)

    print "steer to starboard for 10 sec"
    drive.set_heading(100)
    sleep(10)

