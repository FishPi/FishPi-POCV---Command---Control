#
# FishPi - An autonomous drop in the ocean
#
# View Model for POCV MainView
#

import wx

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