
#
# FishPi - An autonomous drop in the ocean
#
# Perception Unit
#  - responsible for mapping sensor to internal model
#

# temporarily put gpx loading code here
# using https://github.com/tkrajina/gpxpy

import logging

import gpxpy
import gpxpy.gpx

class PerceptionUnit:

    def __init__(self, vehicle_constants, data):
        self._vehicle_constants = vehicle_constants
        self._observed_speed = 0.0
        self._observed_heading = 0.0
        self.update(data)
    
    @property
    def observed_speed(self):
        return self._observed_speed
    
    @property
    def observed_heading(self):
        return self._observed_heading
    
    def update(self, data):
        """ Update observed speed, heading, location from model and sensor data. """
        if data.has_time:
            #data.timestamp
            #data.datestamp
            pass

        if data.has_compass:
            compass_heading = data.compass_heading
            compass_pitch = data.compass_pitch
            compass_roll = data.compass_roll
            
        if data.has_GPS and data.fix:
            lat = data.lat
            lon = data.lon
            # heading only vaild above speed x
            gps_heading = data.gps_heading
            gps_speed = data.speed
            altitude = data.altitude
            num_sat = data.num_sat
                
        # temp - use GPS speed
        if data.has_GPS and data.fix:
            self._observed_speed = gps_speed

        # temp - average compass and GPS headings
        if data.has_compass and data.has_GPS and data.fix:
            self._observed_heading = (compass_heading + gps_heading) / 2.0
        elif data.has_compass:
            self._observed_heading = compass_heading
        elif data.has_GPS and data.fix:
            self._observed_heading = gps_heading


    def load_gpx(self, filename):
        gpx_file = open(filename)
        gpx = gpxpy.parse(gpx_file)
        return gpx
