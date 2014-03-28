#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Simple test of temperature sensor
#

import raspberrypi

from temperature_TMP102 import TemperatureSensor

def test_conversions():
    #test_values(0x7FF, 128.0)
    test_values(0x7FF, 127.9375)
    test_values(0x640, 100)
    test_values(0x500, 80)
    test_values(0x4B0, 75)
    test_values(0x320, 50)
    test_values(0x190, 25)
    test_values(0x004, 0.25)
    test_values(0x000, 0)
    test_values(0xFFC, -0.25)
    test_values(0xE70, -25)
    test_values(0xC90, -55)

def test_values(value_in, value_expected):
    value_out = TemperatureSensor()._convert_12b(value_in)
    if value_out == value_expected:
        print "MATCH: got %f, expected %f for %s" % (value_out, value_expected, bin(value_in))
    else:
        print "FAIL:  got %f, expected %f for %s" % (value_out, value_expected, bin(value_in))

if __name__ == "__main__":
    #print "Testing value conversions..."
    #test_conversions()

    print "Testing temperature sensor..."
    tmpSensor = TemperatureSensor(debug=True, interface=raspberrypi.i2c_bus())
    value = tmpSensor.read_sensor()
    print "Current temperature: %f" % value

