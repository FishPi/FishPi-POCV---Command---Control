
#
# FishPi - An autonomous drop in the ocean
#
# View Controller for POCV MainView
#  - control logic split out from UI
#

import logging

from Tkinter import Tk
from PIL import Image

from ui.main_view import MainView

def run_main_view(kernel):
    """ Runs main UI view. """
    
    # create view controller
    controller = MainViewController(kernel)
    
    # initialise and launch view
    root = Tk()
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
    
    # Control Systems
    # temporary direct access to DriveController to test hardware.
    
    def set_drive(self, throttle_level):
        self._kernel.drive_controller.set_drive(throttle_level)
    
    def set_heading(self, heading):
        self._kernel.drive_controller.set_heading(heading)
    
    def halt(self):
        self._kernel.drive_controller.halt()
    
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
    
    def halt(self):
        """ Commands the NavigationUnit to Halt! """
        self._kernel.navigation_unit.Halt()

    def get_current_map(self):
        return Image.open("fishpi/resources/bournville.tif")
