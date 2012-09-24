#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Simple test of GPS sensor
#

from GPSSensor import GPS_NavigatronSensor

if __name__ == "__main__":
    print "Testing GPS sensor..."
    gpsSensor = GPS_NavigatronSensor()

    # heading
    (hstatus, fix2d, fix3d, numSat, gndSpd, altitude, time, location) = gpsSensor.read_sensor()
    print "Status %s, fix2d? %d, fix3d? %d, numSat %d, gndSpd %d, altitude %d, time %d, location %d" % (hstatus, fix2d, fix3d, numSat, gndSpd, altitude, time, location)

    # raw values
    (hstatus, fix2d, fix3d, numSat, gndSpd, altitude, time, location) = gpsSensor.read_sensor_raw()
    print "Status %s, fix2d? %d, fix3d? %d, numSat %d, gndSpd %d, altitude %d, time %d, location %d" % (hstatus, fix2d, fix3d, numSat, gndSpd, altitude, time, location)
