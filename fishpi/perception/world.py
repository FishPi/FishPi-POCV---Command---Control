
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

    def __init__(self):
        pass

    def load_gpx(self, filename):
        gpx_file = open(filename)
        gpx = gpxpy.parse(gpx_file)
        return gpx
