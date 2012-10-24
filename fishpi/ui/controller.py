
#
# FishPi - An autonomous drop in the ocean
#
# View Controller for POCV MainView
#  - control logic split out from UI
#

import logging
import math

from Tkinter import Tk
from PIL import Image

from ui.main_view import MainView

def run_main_view(kernel):
    """ Runs main UI view. """
    
    # create view controller
    controller = MainViewController(kernel)
    
    # initialise and launch view
    root = Tk()
    root.title("fishpi - Proof Of Concept Vehicle UI")
    root.minsize(800,600)
    root.maxsize(800,600)
    
    app = MainView(root, controller)
    
    # run ui loop
    root.mainloop()


class MainViewController:
    """ Coordinator between UI and main control layers. """
    
    def __init__(self, kernel):
        self._kernel = kernel
    
    def capture_img(self):
        pass
    
    @property
    def last_img(self):
        self.camera_controller.last_img
    
    # Control modes (Manual, AutoPilot)
    def set_manual_mode(self):
        """ Stops navigation unit and current auto-pilot drive. """
        self._kernel.navigation_unit.halt()
        self._kernel.drive_controller.halt()
    
    def set_auto_pilot_mode(self):
        """ Stops current manual drive and starts navigation unit. """
        self._kernel.drive_controller.halt()
        self._kernel.navigation_unit.start()
    
    def halt(self):
        """ Commands the NavigationUnit and Drive Control to Halt! """
        self._kernel.halt()

    # Drive control
    # temporary direct access to DriveController to test hardware.
    
    def set_throttle(self, throttle_level):
        self._kernel.set_throttle(float(throttle_level)/100.0)
    
    def set_heading(self, heading):
        heading_in_rad = (float(heading)/180.0)*math.pi
        self._kernel.set_heading(heading_in_rad)
    
    # Sensors
    
    def read_time(self):
        return localtime()
    
    def read_GPS(self):
        pass
    
    def read_compass(self):
        pass
    
    def get_current_photo(self):
        return Image.open("fishpi/resources/camera.jpg")
    
    # Route Planning and Navigation
    
    def navigate_to(self):
        """ Commands the NavigationUnit to commence navigation of a route. """
        #self.navigation_unit.NavigateTo(route)
        pass
    
    def get_current_map(self):
        return Image.open("fishpi/resources/bournville.tif")
