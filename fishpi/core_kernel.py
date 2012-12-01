
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
    
    def __init__(self, config, debug=False):
        self.config = config
        self.debug = debug
        
        # pull over all hw devices (or proxies) from config
        
        # sensors
        self._gps_sensor = config.gps_sensor
        self._compass_sensor = config.compass_sensor
        self._temperature_sensor = config.temperature_sensor
        
        # vehicle
        self._drive_controller = config.drive_controller
        
        # camera
        self._camera_controller = config.camera_controller

        # data class
        self.data = POCVModelData()

        # supporting classes
        self._perception_unit = PerceptionUnit(self.data)
        self._navigation_unit = NavigationUnit(self._perception_unit, self._drive_controller)
        
    def update(self):
        """ Update loop for sensors->perception->control(->vehicle). """
        try:
            self.read_time()
        except Exception as ex:
            self.data.has_time = False
            logging.exception("CORE:\tError in update loop (TIME) - %s" % ex)
                
        try:
            self.read_GPS()
        except Exception as ex:
            self.data.has_GPS = False
            logging.exception("CORE:\tError in update loop (GPS) - %s" % ex)

        try:
            self.read_compass()
        except Exception as ex:
            self.data.has_compass = False
            logging.exception("CORE:\tError in update loop (COMPASS) - %s" % ex)

        try:
            self.read_temperature()
        except Exception as ex:
            self.data.has_temperature = False
            logging.exception("CORE:\tError in update loop (TEMPERATURE) - %s" % ex)
        
        try:
            self.capture_img()
        except Exception as ex:
            logging.exception("CORE:\tError in update loop (CAMERA) - %s" % ex)

        try:
            self._perception_unit.update(self.data)
        except Exception as ex:
            logging.exception("CORE:\tError in update loop (PERCEPTION) - %s" % ex)
        
        try:
            self._navigation_unit.update()
        except Exception as ex:
            logging.exception("CORE:\tError in update loop (NAVIGATION) - %s" % ex)
        
            
    # Devices
    
    def list_devices(self):
        logging.info("CORE:\tListing devices...")
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
        self.data.has_time = True
    
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
            self.data.has_GPS = True
        else:
            self.data.has_GPS = False

    def read_compass(self):
        if self._compass_sensor:
            (heading, pitch, roll) = self._compass_sensor.read_sensor()
            self.data.compass_heading = heading
	    self.data.compass_pitch = pitch
	    self.data.compass_roll = roll
            self.data.has_compass = True
        else:
            self.data.has_compass = False

    def read_temperature(self):
        if self._temperature_sensor:
            temperature = self._temperature_sensor.read_sensor()
            self.data.temperature = temperature
            self.data.has_temperature = True
        else:
            self.data.has_temperature = False
    
    # Control Systems
    # temporary direct access to DriveController to test hardware.

    def set_throttle(self, throttle_level):
        self._drive_controller.set_throttle(throttle_level)

    def set_steering(self, angle):
        self._drive_controller.set_steering(angle)
    
    # Control modes (Manual, AutoPilot)
    def set_manual_mode(self):
        """ Stops navigation unit and current auto-pilot drive. """
        self._navigation_unit.stop()
        self.halt()

    def set_auto_pilot_mode(self):
        """ Stops current manual drive and starts navigation unit. """
        self.halt()
        self._navigation_unit.start()
    
    @property
    def auto_mode_enabled(self):
        return self._navigation_unit.auto_mode_enabled
                
    # Route Planning and Navigation
    def set_speed(self, speed):
        """ Commands the NavigationUnit to set and hold a given speed. """
        self._navigation_unit.set_speed(speed)
    
    def set_heading(self, heading):
        """ Commands the NavigationUnit to set and hold a given heading. """
        self._navigation_unit.set_heading(heading)
    
    def navigate_to(self):
        """ Commands the NavigationUnit to commence navigation of a route. """
        #self.navigation_unit.NavigateTo(route)
        pass
    
    def halt(self):
        """ Commands the NavigationUnit and Drive Control to Halt! """
        self._navigation_unit.stop()
        self._drive_controller.halt()

    def load_gpx(self, filename):
        gpx = self._perception_unit.load_gpx(filename)
        return gpx
