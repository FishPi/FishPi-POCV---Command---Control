
#
# FishPi - An autonomous drop in the ocean
#

#
# View Controller for POCV MainView
#  - control logic split out from UI, providing:
#    - access to device configuration and drivers
#    - basic control systems eg power and steering
#    - sensory systems eg GPS and Compass
#    - route planning and navigation
#

from time import localtime

from FishPiConfig import FishPiConfig
from CameraController import CameraController
from DriveController import DriveController
from NavigationUnit import NavigationUnit
from PerceptionUnit import PerceptionUnit

class POCVMainViewController:

    def __init__(self, configuration):
        self.config = configuration
        
        self.cameraController = CameraController()
        self.driveController = DriveController()
        self.navigationUnit = NavigationUnit()
        self.perceptionUnit = PerceptionUnit()

    # Devices

    def list_devices(self):
        for device in self.config.devices:
            print device

    # Control Systems


    # Sensors

    def read_time(self):
        return localtime()

    def read_GPS(self):
        pass

    def read_compass(self):
        pass


    # Route Planning and Navigation


    # 

