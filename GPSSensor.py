
#
# FishPi - An autonomous drop in the ocean
#
# GPS Navigatron V2 - I2C GPS using GTPA010
#  - Details at http://www.flytron.com/sensors/180-i2c-gps-for-multiwii-and-others.html
#  - Register definitions at http://www.flytron.com/pdf/Navigatron_Master.pde
#
#  - Standard sense gives:
#    - status, fix2d, fix3d, numSat, gndSpd, altitude, time, location
#
#  - Detailed raw sense gives:
#    - status, fix2d, fix3d, numSat, gndSpd, altitude, time, location
#

#
# Adafruit i2c library (and others) at https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git

from Adafruit_I2C import Adafruit_I2C

class GPS_NavigatronSensor:
    """ GPS Navigatron over I2C. """

    # I2C 'registers' implemented on ATMega328
    I2C_GPS_STATUS= 0x00
    I2C_GPS_NEW_DATA = 0x1
    I2C_GPS_2D_FIX = 0X2
    I2C_GPS_3D_FIX = 0X4
    I2C_GPS_NUM_SATS = 0XF0
    # GPS ground speed in m/s*100 (uint16_t)      (Read Only)
    I2C_GPS_GROUND_SPEED = 0X07
    # GPS altitude in meters (uint16_t)           (Read Only)
    I2C_GPS_ALTITUDE = 0X09
    # UTC Time from GPS in hhmmss.sss * 100 (uint32_t)(unneccesary precision) (Read Only)
    I2C_GPS_TIME = 0X0B
    # Current position (8 bytes, lat and lon, 1 degree = 10 000 000 (read only)
    I2C_GPS_LOCATION =  0x13

    def __init__(self, address=0x20, i2c_bus=None, debug=False):
        if i2c_bus is None:
            self.i2c = Adafruit_I2C(address, debug=debug)
        else:
            self.i2c = Adafruit_I2C(address, bus=i2c_bus, debug=debug)
        self.address = address
        self.debug = debug
        #self.version = self.i2c.readU8(0x3)
        #if self.debug:
        #    print "GPS software v:%d" % self.version

    def read_sensor(self):
        """ Read sensor values. """
        # read status
        status = hex(self.i2c.readU8(self.I2C_GPS_STATUS))
        # read data
        fix2d = self.i2c.readU8(self.I2C_GPS_2D_FIX)
        fix3d = self.i2c.readU8(self.I2C_GPS_3D_FIX)
        numSat = self.i2c.readU8(self.I2C_GPS_NUM_SATS)
        gndSpd = self.i2c.readU16(self.I2C_GPS_GROUND_SPEED)
        altitude = self.i2c.readU16(self.I2C_GPS_ALTITUDE)
        time = self.i2c.readU16(self.I2C_GPS_TIME)
        location = self.i2c.readU16(self.I2C_GPS_LOCATION)
        if self.debug:
            print "Status %s, fix2d? %d, fix3d? %d, numSat %d, gndSpd %d, altitude %d, time %d, location %d" % (status, fix2d, fix3d, numSat, gndSpd, altitude, time, location)
        return status, fix2d, fix3d, numSat, gndSpd, altitude, time, location

    def read_sensor_raw(self):
        """ Read raw sensor values. """
        return self.read_sensor()
