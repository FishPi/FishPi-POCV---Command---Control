
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
from datetime import datetime

from localconfig import FishPiConfig
from model_data import POCVModelData
from control.navigation import NavigationUnit
from perception.world import PerceptionUnit

class FishPiKernel:
    """ Coordinator between different layers. """
    
    def __init__(self, config):
        self.config = config
        
        # pull over all hw devices (or proxies) from config
        
        # sensors
        self._gps_sensor = config.gps_sensor
        self._compass_sensor = config.compass_sensor
        self._temperature_sensor = config.temperature_sensor
        
        # vehicle
        self._drive_controller = config.drive_controller
        
        # camera
        self._camera_controller = config.camera_controller

        # supporting classes
        self.perception_unit = PerceptionUnit()
        self.navigation_unit = NavigationUnit(self._drive_controller, self.perception_unit)
        
        # data class
        self.data = POCVModelData()

    def update(self):
        """ Update loop for sensors. """
        self.read_time()
        self.read_GPS()
        self.read_compass()
        self.capture_img()
        
    # Devices
    
    def list_devices(self):
        logging.info("Listing devices...")
        for device in self.config.devices:
            logging.info(device)
    
    def capture_img(self):
        self._camera_controller.capture_now()
    
    def get_capture_img_enabled(self):
        return self._camera_controller.enabled
    
    def set_capture_img_enabled(self, capture_img_enabled):
        self._camera_controller.enabled = capture_img_enabled
    
    @property
    def last_img(self):
        return self._camera_controller.last_img
        
    # Sensors
    
    def read_time(self):
        dt = datetime.today()
        self.data.timestamp = dt.time()
        self.data.datestamp = dt.date()
    
    def read_GPS(self):
        if self._gps_sensor:
            (fix, lat, lon, heading, speed, altitude, num_sat, timestamp, datestamp) = self._gps_sensor.read_sensor()
            self.data.fix = fix
            self.data.lat = lat
            self.data.lon = lon
            self.data.gps_heading = heading
            self.data.speed = speed
            self.data.altitude = altitude
            self.data.num_sat = num_sat
            self.data.timestamp = timestamp
            self.data.datestamp = datestamp
    
    def read_compass(self):
        if self._compass_sensor:
            heading = self._compass_sensor.read_sensor()
            self.data.compass_heading = heading

    def read_temperature(self):
        if self._temperature_sensor:
            temperature = self._temperature_sensor.read_sensor()
            self.data.temperature = temperature
    
    # Control Systems
    # temporary direct access to DriveController to test hardware.

    def set_throttle(self, throttle_level):
        self._drive_controller.set_throttle(throttle_level)

    def set_heading(self, heading):
        self._drive_controller.set_heading(heading)
    
    # Route Planning and Navigation
    
    def navigate_to(self):
        """ Commands the NavigationUnit to commence navigation of a route. """
        #self.navigation_unit.NavigateTo(route)
        pass
    
    def halt(self):
        """ Commands the NavigationUnit and Drive Control to Halt! """
        self.navigation_unit.halt()
        self._drive_controller.halt()

    def load_gpx(self, filename):
        gpx = self.perception_unit.load_gpx(filename)
        return gpx
