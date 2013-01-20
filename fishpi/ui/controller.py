
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

# callback interval in milli seconds
callback_interval = 50

#def run_main_view(kernel):
#   """ Runs the main UI view. """
#   run_main_view_wx(kernel)

def run_main_view_wx(server, rpc_port, camera_port):
    """ Runs main UI view based on wx framework. """
    # imports
    import wx
    import socket
    # might be some cross platform (windows) issues reported with wxReactor
    from twisted.internet import wxreactor
    # add twisted / wx interaction support
    wxreactor.install()
    # add logging observer
    from twisted.python.log import PythonLoggingObserver
    observer = PythonLoggingObserver()
    observer.start()
    # add some extra logging (temp - merge later)
    #from sys import stdout
    #from twisted.python.log import startLogging, err
    #startLogging(stdout)

    # then can do normal reactor imports
    from twisted.internet import reactor
    from ui.main_view_wx import MainWindow

    # ip address *much* faster than by device name
    ipaddr = socket.gethostbyname(server)

    # create rpc client
    from web.webclient import RPCClient, RPCClientFactory
    rpc_client = RPCClient()
    
    # create wxApp and main window
    wxApp = wx.App(False)
    frame = MainWindow(None, "fishpi - Proof Of Concept Vehicle control", ipaddr, rpc_port, camera_port)
    frame.Show()
    
    # run reactor rather than usual 'wxApp.MainLoop()'
    reactor.registerWxApp(wxApp)
    logging.debug("RPC:\tconnecting to %s (%s) on port %s" % (server, ipaddr, rpc_port))
    reactor.connectTCP(ipaddr, rpc_port, RPCClientFactory(frame))
    #reactor.callLater(5, update_callback)
    reactor.run()

def run_main_view_tk(kernel):
    """ Runs main UI view based on tk framework. """
    # move imports here
    from ui.view_model_tk import MainViewModel
    from ui.main_view_tk import MainView
    
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
    # longer delay on first callback to give UI time for initialisation
    root.after(5000, update_callback, root, controller, view)

    # run ui loop
    root.mainloop()

def update_callback(root, controller, view):
    """ Callback to perform updates etc. Needs to reregister callback at end. """
    # update kernel - note this will need revisiting for non-interactive modes...
    logging.debug("UI:\tIn update...")
    controller._kernel.set_capture_img_enabled(controller.model.capture_img_enabled.get())
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
        self.model.time.set(self._kernel.data.timestamp.isoformat())
        self.model.date.set(self._kernel.data.datestamp.isoformat())
        
        # other data
        self.model.temperature.set(self._kernel.data.temperature)
    
    @property
    def last_img(self):
        return self._kernel.last_img
    
    # Control modes (Manual, AutoPilot)
    def set_manual_mode(self):
        """ Stops navigation unit and current auto-pilot drive. """
        self._kernel.set_manual_mode()
    
    def set_auto_pilot_mode(self):
        """ Stops current manual drive and starts navigation unit. """
        self._kernel.set_auto_pilot_mode()
    
    def halt(self):
        """ Commands the NavigationUnit and Drive Control to Halt! """
        self._kernel.halt()

    @property
    def auto_mode_enabled(self):
        return self._kernel.auto_mode_enabled
    
    # Drive control
    # temporary direct access to DriveController to test hardware.
    
    def set_throttle(self, throttle_level):
        throttle_act = float(throttle_level)/100.0
        # adjustment for slider so min +/- .3 so if in .05 to .3 range, jump to .3
        if throttle_act > 0.05 and throttle_act < 0.3:
            throttle_act = 0.3
        elif throttle_act < -0.05 and throttle_act > -0.3:
            throttle_act = -0.3
        self._kernel.set_throttle(throttle_act)
    
    def set_steering(self, angle):
        angle_in_rad = (float(angle)/180.0)*math.pi
        # adjustment for slider in opposite direction - TODO - move to drive controller
        angle_in_rad = angle_in_rad * -1.0
        self._kernel.set_steering(angle_in_rad)
    
    # Route Planning and Navigation
    def set_speed(self, speed):
        """ Commands the NavigationUnit to set and hold a given speed. """
        self._kernel.set_speed(float(speed))
    
    def set_heading(self, heading):
        """ Commands the NavigationUnit to set and hold a given heading. """
        self._kernel.set_heading(float(heading))
    
    def navigate_to(self):
        """ Commands the NavigationUnit to commence navigation of a route. """
        #self._kernel.navigate_to(route)
        pass
    
    def get_current_map(self):
        return Image.open(os.path.join(self._kernel.config.resources_folder(), 'bournville.tif'))

    def load_gpx(self):
        default_path = os.path.join(self._kernel.config.resources_folder(), 'sample_routes')
        filename = tkFileDialog.askopenfilename(initialdir=default_path, title="Select GPX file to load", filetypes=[("GPX", "*.GPX; *.gpx")])
        if os.path.exists(filename):
            logging.info("UI:\tloading %s" % filename)
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

