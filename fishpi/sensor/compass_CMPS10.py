
#
# FishPi - An autonomous drop in the ocean
#
# Compass (Magnetometer) using CMPS10 - Tilt Compensated Compass Module
#  - Details at http://www.robot-electronics.co.uk/htm/cmps10i2c.htm
#
#  - Standard sense gives:
#   - Compass bearing between 0-359.9
#   - Pitch angle in degrees from the horizontal plane.
#   - Roll angle in degrees from the horizontal plane.
#
#  - Detailed raw sense gives:
#   - Magnetometer (X,Y,Z)
#   - Accelerometer (X,Y,Z)
#
#  - Support for Calibration, I2C address changing, factory reset, serial or PWM modes not provided.
#

#
# Adafruit i2c library (and others) at https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git

import logging
from Adafruit_I2C import Adafruit_I2C

class Cmps10_Sensor:
    """ Tilt adjusted Compass sensor CMP10 over I2C. """

    def __init__(self, address=0x60, i2c_bus=None, debug=False):
        if i2c_bus is None:
            self.i2c = Adafruit_I2C(address, debug=debug)
        else:
            self.i2c = Adafruit_I2C(address, bus=i2c_bus, debug=debug)
        self.address = address
        self.debug = debug
        self.version = self.i2c.readU8(0)
        if self.debug:
            logging.debug("SENSOR:\tCMPS10:\tSoftware v:%d", self.version)

    def read_sensor(self):
        """ Read sensor values. """
        # read 2 registers for heading
        heading = float(self.i2c.readU16(2))/10.0
        # read 2 registers for pitch and roll
        pitch = self.i2c.readS8(4)
        roll = self.i2c.readS8(5)
        if self.debug:
            logging.debug("SENSOR:\tCMPS10\tHeading %f, pitch %f, roll %f", heading, pitch, roll)
        return heading, pitch, roll

    def read_sensor_raw(self):
        """ Read raw sensor values. """
        # read 2 registers each for raw sensor values
        # Magnetometer
        m_x = float(self.i2c.readS16(10))
        m_y = float(self.i2c.readS16(12))
        m_z = float(self.i2c.readS16(14))
        # Accelerometer
        a_x = float(self.i2c.readS16(16))
        a_y = float(self.i2c.readS16(18))
        a_z = float(self.i2c.readS16(20))
        if self.debug:
            logging.debug("SENSOR:\tCMPS10\tRaw values: M(x,y,z)=(%f,%f,%f) A(x,y,z)=(%f,%f,%f)", m_x, m_y, m_z, a_x, a_y, a_z)
        return (m_x, m_y, m_z, a_x, a_y, a_z)

