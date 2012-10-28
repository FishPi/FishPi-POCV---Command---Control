
#
# FishPi - An autonomous drop in the ocean
#
# POCVModelData
#  - Internal model containing FishPi POCV state
#    - 

class POCVModelData:
    """ Internal model containing FishPi POCV state. """

    def __init__(self):
        self.fix = 0
        self.lat = 0.0
        self.lon = 0.0
        self.gps_heading = 0.0
        self.speed = 0.0
        self.altitude = 0.0
        self.num_sat = 0
        self.timestamp = ''
        self.datestamp = ''

        self.compass_heading = 0.0

        self.temperature = 0.0


        
