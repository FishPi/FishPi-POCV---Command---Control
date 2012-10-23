
#
# FishPi - An autonomous drop in the ocean
#
# POCVModelData
#  - Internal model containing FishPi POCV state
#    - 

class POCVModelData:
    """ Internal model containing FishPi POCV state. """

    def __init__(self):
        pass

    def getHeading(self):
        pass

    def getSpeed(self):
        pass

    def getDriveSetting(self):
        pass

    def getSteeringSetting(self):
        pass

    def getLatLong(self):
        pass

    def getDateTime(self):
        pass

    def getRouteData(self):
        pass

class RouteData:
    """ Internal model containing Route Data. """

    def __init__(self):
        pass

class SensorData:
    """ Internal model containing Sensor Data. """

    def __init__(self):
        pass

    def getGPSData(self):
        pass

    def getCompassData(self):
        pass

    def getTemperatureData(self):
        pass

    def getGyroData(self):
        pass

    def getAccelerometerData(self):
        pass

class CameraData:
    """ Internal model containing Camera Data. """

    def __init__(self):
        pass

    def getCaptureMode(self):
        pass

    def getIsEnabled(self):
        pass

    def getLastImageLocation(self):
        pass
