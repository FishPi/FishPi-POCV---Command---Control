#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Simple test of compass sensor
#

import smbus
import raspberrypi
from compass_CMPS10 import Cmps10_Sensor

if __name__ == "__main__":
    print "Testing compass sensor..."
    compassSensor = Cmps10_Sensor(i2c_bus=smbus.SMBus(raspberrypi.i2c_bus()), debug=True)

    # heading
    (heading, pitch, roll) = compassSensor.read_sensor()
    print "Heading %f, pitch %f, roll %f" % (heading, pitch, roll)

    # raw values
    (m_x, m_y, m_z, a_x, a_y, a_z) = compassSensor.read_sensor_raw()
    print "Raw values: M(x,y,z)=(%f,%f,%f) A(x,y,z)=(%f,%f,%f)" % (m_x, m_y, m_z, a_x, a_y, a_z)
