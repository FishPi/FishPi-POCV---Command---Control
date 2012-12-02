
#
# FishPi - An autonomous drop in the ocean
#
# GPS Navigatron V2 - I2C GPS using GTPA010
#  - Details at http://www.flytron.com/sensors/180-i2c-gps-for-multiwii-and-others.html
#  - Register definitions at http://www.flytron.com/pdf/Navigatron_Master.pde
#
#  - Standard sense gives:
#    - fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp
#
#  - Detailed raw sense gives:
#    - fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp
#

#
# Adafruit i2c library (and others) at https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git

import logging
from datetime import datetime

from Adafruit_I2C import Adafruit_I2C

class GPS_NavigatronSensor:
    """ GPS Navigatron over I2C. """

    # I2C 'registers' implemented on ATMega328
    I2C_GPS_STATUS = 0
    # values from status register
    I2C_GPS_NEW_DATA = 0x1
    I2C_GPS_2D_FIX = 0x2
    I2C_GPS_3D_FIX = 0x4
    I2C_GPS_NUM_SATS = 0xF0
    # writable command register
    I2C_GPS_COMMAND = 1
    # writable wp register
    I2C_GPS_WP_REG = 2
    # firmware version (uint8_t)
    I2C_GPS_REG_VERSION = 3
    # Current position (8 bytes, int32_t)
    # lat and lon, 1 degree = 10 000 000 (read only)
    I2C_GPS_LOCATION = 7
    # banking towards north/south (int16_t)
    I2C_GPS_NAV_LAT = 15
    # banking towards east/west (int16_t)
    I2C_GPS_NAV_LON = 17
    # GPS ground speed in m/s*100 (uint16_t)      (Read Only)
    I2C_GPS_GROUND_SPEED = 31
    # GPS altitude in meters (uint16_t)           (Read Only)
    I2C_GPS_ALTITUDE = 33
    # GPS ground course (uint16_t)
    I2C_GPS_GROUND_COURSE = 35
    # UTC Time from GPS in hhmmss.sss * 100 (uint32_t)(unneccesary precision) (Read Only)
    I2C_GPS_TIME = 39

    def __init__(self, address=0x20, i2c_bus=None, debug=False):
        if i2c_bus is None:
            self.i2c = Adafruit_I2C(address, debug=debug)
        else:
            self.i2c = Adafruit_I2C(address, bus=i2c_bus, debug=debug)
        self.address = address
        self.debug = debug
        if self.debug:
            logging.debug("SENSOR:\tGPS_I2C:\tChecking firmware version...")
        self.version = self.i2c.readU8(self.I2C_GPS_REG_VERSION)
        if self.debug:
            logging.debug("SENSOR:\tGPS_I2C:\tFirmware v:%d", self.version)

    def read_sensor(self):
        """ Read sensor values. """
        # read status
        if self.debug:
            logging.debug("SENSOR:\tGPS_I2C:\tReading status...")
        status = self.i2c.readU8(self.I2C_GPS_STATUS)
        if self.debug:
            logging.debug("SENSOR:\tGPS_I2C:\tStatus %s", hex(status))
        
        fix = 1
        num_sat = 1
    
        # read data
        if self.debug:
            logging.debug("SENSOR:\tGPS_I2C:\tReading location...")
        loc_buffer = self.i2c.readList(self.I2C_GPS_LOCATION, 8)
        (lat, lon) = self.convert_buffer(loc_buffer)
        if self.debug:
            logging.debug("SENSOR:\tGPS_I2C:\t(lat,lon) = (%f, %f)", lat, lon)
    
        # read remaining data
        if self.debug:
            logging.debug("SENSOR:\tGPS_I2C:\tReading nav heading...")
        nav_lat = self.i2c.readS16(self.I2C_GPS_NAV_LAT)
        nav_lon = self.i2c.readS16(self.I2C_GPS_NAV_LON)
        if self.debug:
            logging.debug("SENSOR:\tGPS_I2C:\tBearing to (N/S, E/W) = (%f, %f)", nav_lat, nav_lon)
        if self.debug:
            logging.debug("SENSOR:\tGPS_I2C:\tReading ground speed and altitude...")
        speed = self.i2c.readU16(self.I2C_GPS_GROUND_SPEED)/100.0
        altitude = self.i2c.readU16(self.I2C_GPS_ALTITUDE)
        heading = self.i2c.readU16(self.I2C_GPS_GROUND_COURSE)
        if self.debug:
            logging.debug("SENSOR:\tGPS_I2C:\t(ground speed, altitude, ground course) = (%f, %f, %f)", speed, altitude, heading)

        # read time
        if self.debug:
            logging.debug("SENSOR:\tGPS_I2C:\tReading time...")
        time_buffer = self.i2c.readList(self.I2C_GPS_TIME, 4)
        time = float((time_buffer[3]<<24)|(time_buffer[2]<<16)|(time_buffer[1]<<8)|(time_buffer[0]))/10000.0
        if self.debug:
            logging.debug("SENSOR:\tGPS_I2C:\ttime = %f", time)
        dt = datetime.today()
        timestamp = dt.time()
        datestamp = dt.date()
        #timestamp = datetime.strptime(int(time), "%H%M%S").time()
        #datestamp = x
                
        # and return
        return fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp
    
    def convert_buffer(self, loc_buffer):
        ulat = int((loc_buffer[3]<<24)|(loc_buffer[2]<<16)|(loc_buffer[1]<<8)|(loc_buffer[0]))
        ulon = int((loc_buffer[7]<<24)|(loc_buffer[6]<<16)|(loc_buffer[5]<<8)|(loc_buffer[4]))
        lat = self.convert_u_l(ulat)/10000000.0
        lon = self.convert_u_l(ulon)/10000000.0
        return lat, lon

    def convert_u_l(self, value_in):
        if value_in >> 31:
            return float(int('0b'+''.join('1' if c == '0' else '0' for c in bin(value_in-1).lstrip('-0b')),2)) * -1.0
        else:
            return float(value_in)

    def read_sensor_raw(self):
        """ Read raw sensor values. """
        return self.read_sensor()
