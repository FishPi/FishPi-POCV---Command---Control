
#
# FishPi - An autonomous drop in the ocean
#
# Core Kernel for coordinating FishPi components
#  - control logic split out, providing:
#    - access to device configuration and drivers
#    - basic control systems eg power and steering
#    - sensory systems eg GPS and Compass
#    - route planning and navigation
#

import logging
import os
import platform
from time import localtime

from PIL import Image

from localconfig import FishPiConfig
from control.navigation import NavigationUnit
from perception.world import PerceptionUnit

class FishPiKernel:
    """ Coordinator between different layers. """
    
    def __init__(self, config):
        self.config = config
        
        # setup controllers and coordinating services
        
        # CameraController
        if platform.system() == "Linux":
            try:
                from sensor.camera import CameraController
                self.camera_controller = CameraController(self.config)
            except ImportError as ex:
                logging.info(ex)
                logging.info("Camera support unavailable.")
                self.camera_controller = DummyCameraController(self.resources_folder())
        else:
            logging.info("Camera support unavailable.")
            self.camera_controller = DummyCameraController(self.resources_folder())
            
        # DriveController
        if os.getuid() == 0:
            try:
                from vehicle.DriveController import DriveController
                # TODO pull out address from self.config.drive (and possibly pwm addresses)
                self.drive_controller = DriveController()
            except ImportError:
                logging.info("Drive controller not loaded, drive support unavailable.")
                self.drive_controller = DummyDriveController()
        else:
            logging.info("Not running as root, drive support unavailable.")
            self.drive_controller = DummyDriveController()
        
        self.perception_unit = PerceptionUnit()
        self.navigation_unit = NavigationUnit(self.drive_controller, self.perception_unit)

    def update(self):
        #(fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp) = self.gps_sensor.read_sensor()
        self.camera_controller.capture_now()
        pass
    
    def resources_folder(self):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')
    
    # Devices
    
    def list_devices(self):
        logging.info("Listing devices...")
        for device in self.config.devices:
            logging.info(device)
    
    def capture_img(self):
        self.camera_controller.capture_now()
    
    @property
    def last_img(self):
        return self.camera_controller.last_img
    
    # Control Systems
    # temporary direct access to DriveController to test hardware.
    
    def set_throttle(self, throttle_level):
        self.drive_controller.set_throttle(throttle_level)
    
    def set_heading(self, heading):
        self.drive_controller.set_heading(heading)
        
    # Sensors
    
    def read_time(self):
        return localtime()
    
    def read_GPS(self):
        pass
    
    def read_compass(self):
        pass
    
    
    # Route Planning and Navigation
    
    def navigate_to(self):
        """ Commands the NavigationUnit to commence navigation of a route. """
        #self.navigation_unit.NavigateTo(route)
        pass
    
    def halt(self):
        """ Commands the NavigationUnit and Drive Control to Halt! """
        self.navigation_unit.halt()
        self.drive_controller.halt()

    def load_gpx(self, filename):
        gpx = self.perception_unit.load_gpx(filename)
        return gpx

class DummyCameraController(object):
    
    def __init__(self, resources_folder):
        temp_image_path = os.path.join(resources_folder, 'camera.jpg')
        self._last_img = Image.open(temp_image_path)
    
    def capture_now(self):
        pass
    
    @property
    def last_img(self):
        return self._last_img

class DummyDriveController(object):
    def __init__(self):
        pass
    
    def set_throttle(self, throttle_level):
        logging.debug("Throttle set to: %s" % throttle_level)
        pass
    
    def set_heading(self, heading):
        logging.debug("Heading set to: %s" % heading)
        pass
    
    def halt(self):
        logging.debug("Drive halting.")
        pass
