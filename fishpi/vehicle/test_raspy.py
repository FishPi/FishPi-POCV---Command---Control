#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Simple test of Raspy Juice
#

import raspberrypi

from time import sleep

if __name__ == "__main__":
    
    print "init i2c bus"
    i2c_bus=raspberrypi.i2c_bus()
    
    addr = 0x32
    servo_number = 3

    print "full left"
    i2c_bus.write_word_data(addr, servo_number, 1000)
    sleep(5)
    
    print "full right"
    i2c_bus.write_word_data(addr, servo_number, 2000)
    sleep(5)
    
    print "centre"
    i2c_bus.write_word_data(addr, servo_number, 1500)
    
