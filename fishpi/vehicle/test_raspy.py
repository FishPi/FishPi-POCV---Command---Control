#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Simple test of Raspy Juice
#

import raspberrypi

from time import sleep
from drive_controller import PyJuiceDriveController

def test_servo(i2c_bus, addr, servo_number):
    print "init i2c bus"

    print "full left"
    i2c_bus.write_word_data(addr, servo_number, 1000)
    sleep(5)
    
    print "full right"
    i2c_bus.write_word_data(addr, servo_number, 2000)
    sleep(5)
    
    print "centre"
    i2c_bus.write_word_data(addr, servo_number, 1500)
    sleep(5)

def test_drive(i2c_bus):
    print "testing drive controller..."
    drive = PyJuiceDriveController(debug=True, i2c_bus=i2c_bus)
    
    print "run full ahead for 5 sec..."
    drive.set_throttle(1.0)
    sleep(5)
    
    print "run 50% ahead for 5 sec..."
    drive.set_throttle(0.5)
    sleep(5)
    
    print "run 0% for 5 sec..."
    drive.set_throttle(0.0)
    sleep(5)
    
    print "run 50% reverse for 5 sec"
    drive.set_throttle(-0.5)
    sleep(5)
    
    print "run full reverse for 5 sec"
    drive.set_throttle(-1.0)
    sleep(5)
    
    print "and back to neutral..."
    drive.set_throttle(0.0)
    sleep(5)
    
    # test steering
    print "steer hard to port for 5 sec"
    drive.set_heading(-0.785398)
    sleep(5)
    
    print "steer to port for 5 sec"
    drive.set_heading(-0.3927)
    sleep(5)
    
    print "and back to neutral..."
    drive.set_heading(0.0)
    sleep(5)
    
    print "steer to starboard for 5 sec"
    drive.set_heading(0.3927)
    sleep(5)
    
    print "steer hard to starboard for 5 sec"
    drive.set_heading(0.785398)
    sleep(5)
    
    print "and back to neutral..."
    drive.set_heading(0.0)
    sleep(5)

if __name__ == "__main__":
    # init
    i2c_bus=raspberrypi.i2c_bus()
    
    # test servo
    test_servo(i2c_bus, 0x32, 3)

    # test drive
    test_drive(i2c_bus)

