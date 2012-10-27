#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Adafruit GPS module:
#  - http://www.adafruit.com/products/746
#  - http://learn.adafruit.com/adafruit-ultimate-gps/overview
#  - based on Arduino library at https://github.com/adafruit/Adafruit-GPS-Library
#
#  - nmea sentence details at http://aprs.gids.nl/nmea/
#
#  - Standard sense gives:
#    - fix, lat, lon, heading, speed, altitude, num_sat, time, date
#
#  - Detailed raw sense gives:
#    - fix, lat, lon, heading, speed, altitude, num_sat, time, date

import serial
import pynmea.nmea

class GPS_AdafruitSensor:
    """ GPS Navigatron over serial port. """

    # different commands to set the update rate from once a second (1 Hz) to 10 times a second (10Hz)
    PMTK_SET_NMEA_UPDATE_1HZ = '$PMTK220,1000*1F'
    PMTK_SET_NMEA_UPDATE_5HZ = '$PMTK220,200*2C'
    PMTK_SET_NMEA_UPDATE_10HZ = '$PMTK220,100*2F'

    # baud rates
    PMTK_SET_BAUD_57600 = '$PMTK250,1,0,57600*2C'
    PMTK_SET_BAUD_9600 = '$PMTK250,1,0,9600*17'

    # turn on only the second sentence (GPRMC)
    PMTK_SET_NMEA_OUTPUT_RMCONLY = '$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29'
    # turn on GPRMC and GGA
    PMTK_SET_NMEA_OUTPUT_RMCGGA = '$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28'
    # turn on GPRMC, GPVTG and GGA
    PMTK_SET_NMEA_OUTPUT_RMCVTGGGA = '$PMTK314,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29'
    #turn on ALL THE DATA
    PMTK_SET_NMEA_OUTPUT_ALLDATA = '$PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0*28'
    #turn off output
    PMTK_SET_NMEA_OUTPUT_OFF = '$PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28'

    # ask for the release and version
    PMTK_Q_RELEASE = '$PMTK605*31'

    #  how long to wait when we're looking for a response
    MAXWAITSENTENCE = 5

    def __init__(self, serial_bus="/dev/ttyAMA0", baud=9600, debug=False):
	self._GPS = serial.Serial(serial_bus, baud)
	#self._GPS.write(self.PMTK_Q_RELEASE)
	#self._version = self._GPS.readline(20)
	self._GPS.write(self.PMTK_SET_NMEA_UPDATE_1HZ)
	self._GPS.write(self.PMTK_SET_BAUD_9600)
	self._GPS.write(self.PMTK_SET_NMEA_OUTPUT_RMCVTGGGA)
	self._GPS.flush()

    def read_sensor(self):
	""" Reads GPS and returns (fix, lat, lon, heading, speed, altitude, num_sat, time, date). """
	if not(self._GPS.inWaiting()):
	    return self.zero_response()

	# read gps gga (fix data) packet
	hasRead, gps_gga = self.wait_for_sentence('$GPGGA')
	if not(has_read):
	    return self.zero_response()
	if not(gps_gga.gps_qual > 0):
	    return self.zero_response()
	
	fix = gps_gga.gps_qual
	lat = gps_gga.latitude * (1.0 if gps_gga.lat_direction == 'N' else -1.0)
	lon = gps_gga.longitude * (1.0 if gps_gga.lon_direction == 'E' else -1.0)
	altitude = gps_gga.antenna_altitude
	num_sat = gps_gga.num_sats
	time = gps_gga.timestamp
        
	# read gps rmc (recommended minimum) packet
	has_read, gps_rmc = wait_for_sentence('$GPRMC')
	if not(has_read):
	    return self.zero_response()    
	if not(gps_rmc.data_validity == 'A'):
	    return self.zero_response()

	lat = gps_rmc.lat * (1.0 if gps_rmc.lat_dir == 'N' else -1.0)
	lon = gps_rmc.lon * (1.0 if gps_rmc.lon_dir == 'E' else -1.0)
	altitude = gps_rmc.antenna_altitude
	num_sat = gps_rmc.num_sats
	time = gps_rmc.timestamp
	date = gps_rmc.datestamp
	heading = gps_rmc.true_course
	speed = gps_rmc.spd_over_grnd

	# and done
	return fix, lat, lon, heading, speed, altitude, num_sat, time, date

    def read_sensor_raw(self):
        """ Read raw sensor values. """
        return self.read_sensor()

    def zero_response(self):
        return 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0

    def wait_for_sentence(self, wait4me):
        i = 0;
	while (i < self.MAXWAITSENTENCE):
	    if self._GPS.inWaiting():
	        line = self._GPS.readline()
                if line.startswith(wait4me):
                    if line.startswith('$GPGGA'):
                        p = pynmea.nmea.GPRMC()
                        p.parse(line)
                        return True, p
                if line.startswith('$GPGGA'):
                        p = pynmea.nmea.GPGGA()
                        p.parse(line)
                        return True, p
		i += 1

        return False, None

