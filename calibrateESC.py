#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Calibrate ESC through PWM controller
#

from time import sleep
from DriveController import DriveController

if __name__ == "__main__":
    print "Calibrating ESC"
    drive = DriveController(debug=True)

    raw_input("Power on ESC and enter calibration mode... Then press <ENTER>...")

    print "run full ahead for 5 sec..."
    drive.set_drive(1.0)
    sleep(5)
    
    print "returning to neutral for 5 sec"
    drive.set_drive(0.0)
    sleep(5)

    print "run full reverse for 5 sec"
    drive.set_drive(-1.0)
    sleep(5)
    
    print "returning to neutral"
    drive.set_drive(0.0)
    sleep(5)

    print "calibration should be complete!"

