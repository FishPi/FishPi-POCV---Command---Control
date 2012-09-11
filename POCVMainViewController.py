
#
# FishPi - An autonomous drop in the ocean
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
    """ Coordinator between UI and main control layers. """
    
    def __init__(self, configuration):
        self.config = configuration
        
        # setup coordinating
        self.cameraController = CameraController()
        self.driveController = DriveController()
        self.perceptionUnit = PerceptionUnit()
        self.navigationUnit = NavigationUnit(self.driveController, self.perceptionUnit)

    # Devices

    def list_devices(self):
        for device in self.config.devices:
            print device

    # Control Systems
    # temporary direct access to DriveController to test hardware.
    # ...

    # Sensors

    def read_time(self):
        return localtime()

    def read_GPS(self):
        pass

    def read_compass(self):
        pass


    # Route Planning and Navigation

    def navigateTo(self):
        """ Commands the NavigationUnit to commence navigation of a route. """
        #self.navigationUnit.NavigateTo(route)
        pass

    def halt(self):
        """ Commands the NavigationUnit to Halt! """
        self.navigationUnit.Halt()

