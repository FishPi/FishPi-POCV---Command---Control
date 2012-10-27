#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Adafruit GPS module:
#  - http://www.adafruit.com/products/746
#  - http://learn.adafruit.com/adafruit-ultimate-gps/overview
#  - based on Arduino library at https://github.com/adafruit/Adafruit-GPS-Library
#
#  - Standard sense gives:
#    - status, fix2d, fix3d, numSat, gndSpd, altitude, time, location
#
#  - Detailed raw sense gives:
#    - status, fix2d, fix3d, numSat, gndSpd, altitude, time, location

import serial

class GPS_AdafruitSensor:
    """ GPS Navigatron over serial port. """

    # different commands to set the update rate from once a second (1 Hz) to 10 times a second (10Hz)
    PMTK_SET_NMEA_UPDATE_1HZ = "$PMTK220,1000*1F"
    PMTK_SET_NMEA_UPDATE_5HZ = "$PMTK220,200*2C"
    PMTK_SET_NMEA_UPDATE_10HZ = "$PMTK220,100*2F"

    # baud rates
    PMTK_SET_BAUD_57600 = "$PMTK250,1,0,57600*2C"
    PMTK_SET_BAUD_9600 = "$PMTK250,1,0,9600*17"

    # turn on only the second sentence (GPRMC)
    PMTK_SET_NMEA_OUTPUT_RMCONLY = "$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29"
    # turn on GPRMC and GGA
    PMTK_SET_NMEA_OUTPUT_RMCGGA = "$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28"
    #turn on ALL THE DATA
    PMTK_SET_NMEA_OUTPUT_ALLDATA = "$PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0*28"
    #turn off output
    PMTK_SET_NMEA_OUTPUT_OFF = "$PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28"

    # ask for the release and version
    PMTK_Q_RELEASE = "$PMTK605*31"

    #  how long to wait when we're looking for a response
    MAXWAITSENTENCE = 5


    def __init__(self, serial_bus="/dev/ttyAMA0", baud=9600, debug=False):
	self._GPS = serial.Serial(serial_bus, baud)
	self._GPS.write(self.PMTK_Q_RELEASE)
	self._version = self._GPS.readline(20)

    def read_sensor(self):
	line = self._GPS.readline()
	status = 'x'
	lat = 'x'
	lon = 'x'
	nav_lat = 'x'
	nav_lon = 'x'
	gnd_spd = 'x'
	altitude = 'x'
	gnd_course = 'x'
	time = 'x'
        return status, lat, lon, nav_lat, nav_lon, gnd_spd, altitude, gnd_course, time

    def read_sensor_raw(self):
        """ Read raw sensor values. """
        return self.read_sensor()

    def parse(self, nmea):
        """ Parses NMEA message. """
	
	chars = list(nmea)
	# do checksum check
	if chars[len(chars)-4] == '*':
	    pass

    	if '$GPGGA':
		pass

	if '$GPRMC':
		pass

