#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Simple test of GPS sensor
#

from time import sleep
from GPS_I2C import GPS_NavigatronSensor

if __name__ == "__main__":
    print "Testing GPS sensor (running 5x with 5s pause)..."

    print "Initialising..."
    gpsSensor = GPS_NavigatronSensor(debug=True)

    # heading
    print "Reading 1..."
    (status, lat, lon, nav_lat, nav_lon, gnd_spd, altitude, gnd_course, time) = gpsSensor.read_sensor()
    print "(status, lat,lon) = (%s, %f, %f)" % (hex(status), lat, lon)
    sleep(5)
    
    print "Reading 2..."
    (status, lat, lon, nav_lat, nav_lon, gnd_spd, altitude, gnd_course, time) = gpsSensor.read_sensor()
    print "(status, lat,lon) = (%s, %f, %f)" % (hex(status), lat, lon)
    sleep(5)

    print "Reading 3..."
    (status, lat, lon, nav_lat, nav_lon, gnd_spd, altitude, gnd_course, time) = gpsSensor.read_sensor()
    print "(status, lat,lon) = (%s, %f, %f)" % (hex(status), lat, lon)
    sleep(5)
    
    print "Reading 4..."
    (status, lat, lon, nav_lat, nav_lon, gnd_spd, altitude, gnd_course, time) = gpsSensor.read_sensor()
    print "(status, lat,lon) = (%s, %f, %f)" % (hex(status), lat, lon)
    sleep(5)
    
    print "Reading 5..."
    (status, lat, lon, nav_lat, nav_lon, gnd_spd, altitude, gnd_course, time) = gpsSensor.read_sensor()
    print "(status, lat,lon) = (%s, %f, %f)" % (hex(status), lat, lon)
    sleep(5)
    
    print "Done."

    # raw values - not currently implemented any differently
    # will move more fields over when correctly reading sensor
    # gpsSensor.read_sensor_raw()
