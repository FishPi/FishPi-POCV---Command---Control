
#
# FishPi - An autonomous drop in the ocean
#
# View Controller for POCV MainView
#  - control logic split out from UI
#

import logging
import math
import os

import Tkinter
import tkFileDialog
from PIL import Image

from ui.main_view import MainView

# callback interval in milli seconds
callback_interval = 1000

def run_main_view(kernel):
    """ Runs main UI view. """
    
    # initialise UI system
    root = Tkinter.Tk()
    root.title("fishpi - Proof Of Concept Vehicle control")
    root.minsize(800,600)
    root.maxsize(800,600)
    
    # create view model
    view_model = MainViewModel(root)
    
    # create view controller
    controller = MainViewController(kernel, view_model)
    
    # create view
    view = MainView(root, controller)

    # add callback to kernel for updates
    root.after(callback_interval, update_callback, root, controller, view)

    # run ui loop
    root.mainloop()

def update_callback(root, controller, view):
    """ Callback to perform updates etc. Needs to reregister callback at end. """
    # update kernel - note this will need revisiting for non-interactive modes...
    logging.debug("In update...")
    controller._kernel.update()
    # tell controller to update model (from kernel)
    controller.update()
    # annoyingly, images don't seem to bind so calling back to view to tell it to update image
    view.update_callback()
    # reregister callback
    root.after(callback_interval, update_callback, root, controller, view)

class MainViewController:
    """ Coordinator between UI and main control layers. """
    
    def __init__(self, kernel, view_model):
        self._kernel = kernel
        self.model = view_model
    
    def update(self):
        """ Updates view model from kernel. """
        # GPS data
        self.model.GPS_latitude.set(self._kernel.data.lat)
        self.model.GPS_longitude.set(self._kernel.data.lon)
        
        self.model.GPS_heading.set(self._kernel.data.gps_heading)
        self.model.GPS_speed.set(self._kernel.data.speed)
        self.model.GPS_altitude.set(self._kernel.data.altitude)
        
        self.model.GPS_fix.set(self._kernel.data.fix)
        self.model.GPS_satellite_count.set(self._kernel.data.num_sat)
        
        # compass data
        self.model.compass_heading.set(self._kernel.data.compass_heading)
        
        # time data
        self.model.time.set(self._kernel.data.timestamp)
        self.model.date.set(self._kernel.data.datestamp)
        
        # other data
        self.model.temperature.set(self._kernel.data.temperature)
    
    @property
    def last_img(self):
        return self._kernel.last_img
    
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
    
    # Route Planning and Navigation
    
    def navigate_to(self):
        """ Commands the NavigationUnit to commence navigation of a route. """
        #self.navigation_unit.NavigateTo(route)
        pass
    
    def get_current_map(self):
        return Image.open(os.path.join(self._kernel.resources_folder(), 'bournville.tif'))

    def load_gpx(self):
        default_path = os.path.join(self._kernel.resources_folder(), 'sample_routes')
        filename = tkFileDialog.askopenfilename(initialdir=default_path, title="Select GPX file to load", filetypes=[("GPX", "GPX")])
        if os.path.exists(filename):
            logging.info('loading %s' % filename)
            gpx = self._kernel.load_gpx(filename)
            # update list
            self.model.clear_waypoints()
            for route in gpx.routes:
                for point in route.points:
                    wp_str = '({0}:{1},{2})'.format(point.name, point.latitude, point.longitude)
                    logging.info(wp_str)
                    wp_str2 = '{0}  {1}, {2}    X'.format(point.name, point.latitude, point.longitude)
                    self.model.waypoints.append(wp_str2)
    
    def save_gpx(self):
        pass

class MainViewModel:
    """ UI Model containing bindable variables. """

    def __init__(self, root):
        # GPS data
        self.GPS_latitude = Tkinter.StringVar(master=root, value="##d ##.####' X")
        self.GPS_longitude = Tkinter.StringVar(master=root, value="##d ##.####' X")
        
        self.GPS_heading = Tkinter.DoubleVar(master=root, value=0.0)
        self.GPS_speed = Tkinter.DoubleVar(master=root, value=0.0)
        self.GPS_altitude = Tkinter.DoubleVar(master=root, value=0.0)

        self.GPS_fix = Tkinter.IntVar(master=root, value=0)
        self.GPS_satellite_count = Tkinter.IntVar(master=root, value=0)

        # compass data
        self.compass_heading = Tkinter.DoubleVar(master=root, value=0.0)

        # time data
        self.time = Tkinter.StringVar(master=root, value="hh:mm:ss")
        self.date = Tkinter.StringVar(master=root, value="dd:MM:yyyy")

        # other data
        self.temperature = Tkinter.DoubleVar(master=root, value=0.0)

        # other settings
        self.capture_img_enabled = Tkinter.IntVar(master=root, value=0)

        # route data
        self.waypoints = []

    def clear_waypoints(self):
        del self.waypoints[0:len(self.waypoints)]
