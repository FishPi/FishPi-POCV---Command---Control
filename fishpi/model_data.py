
#
# FishPi - An autonomous drop in the ocean
#
# POCVModelData
#  - Internal model containing FishPi POCV state
#    - 

class POCVModelData:
    """ Internal model containing FishPi POCV state. """

    def __init__(self):
        # GPS
        self.has_GPS = False
        self.fix = 0
        self.lat = 0.0
        self.lon = 0.0
        self.gps_heading = 0.0
        self.speed = 0.0
        self.altitude = 0.0
        self.num_sat = 0
        
        # time
        self.has_time = False
        self.timestamp = ''
        self.datestamp = ''

        # compass
        self.has_compass = False
        self.compass_heading = 0.0

        # gyro
        self.has_gyro = False
        
        # accelerometer
        self.has_accelerometer = False
        
        # temperature
        self.has_temperature = False
        self.temperature = 0.0


        
