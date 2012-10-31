#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Simple test of GPS sensor
#

import raspberrypi

from time import sleep
from GPS_I2C import GPS_NavigatronSensor

def test_buffer_conversion(gps_sensor):
    buffer_1 = [0, 0, 0, 0, 0, 0, 0, 0]
    lat_1, lon_1 = gps_sensor.convert_buffer(buffer_1)
    print "%s maps to (%s, %s)" % (buffer_1, lat_1, lon_1)
    
    buffer_2 = [18, 8, 64, 31, 99, 150, 87, 254]
    lat_2, lon_2 = gps_sensor.convert_buffer(buffer_2)
    print "%s maps to (%s, %s)" % (buffer_2, lat_2, lon_2)

if __name__ == "__main__":
    print "Testing GPS sensor (running 5x with 5s pause)..."

    print "Initialising..."
    gps_sensor = GPS_NavigatronSensor(debug=True, i2c_bus=raspberrypi.i2c_bus())

    # test raw conversion logic
    #test_buffer_conversion(gps_sensor)

    # heading
    print "Reading 1..."
    (fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp) = gps_sensor.read_sensor()
    print fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp
    sleep(5)
    
    print "Reading 2..."
    (fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp) = gps_sensor.read_sensor()
    print fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp
    sleep(5)
    
    print "Reading 3..."
    (fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp) = gps_sensor.read_sensor()
    print fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp
    sleep(5)
    
    print "Reading 4..."
    (fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp) = gps_sensor.read_sensor()
    print fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp
    sleep(5)
    
    print "Reading 5..."
    (fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp) = gps_sensor.read_sensor()
    print fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp
    sleep(5)
    
    print "Done."

    # raw values - not currently implemented any differently
    # will move more fields over when correctly reading sensor
    # gpsSensor.read_sensor_raw()
