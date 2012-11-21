
#
# FishPi - An autonomous drop in the ocean
#
# Main View classes for POCV UI.
#

import tkFont

from Tkinter import *
from PIL import Image, ImageTk

class MainView(Frame, object):
    """ MainView class for POCV UI. """
    
    def __init__(self, master, view_controller):
        super(MainView, self).__init__(master, bd=1, relief=GROOVE)
        self.pack()
        self.create_widgets(master, view_controller)

    def create_widgets(self, master, view_controller):
        """ Create widgets for view. """
        
        # top frame
        self.top_frame = Frame(master, bd=1, relief=GROOVE)
        self.top_frame.pack(fill=X)
        
        # map frame (in top sub-frame)
        self.map_frame = MapFrame(self.top_frame, view_controller)
        self.map_frame.pack(side=LEFT, fill=X)
        
        # camera frame (in top sub-frame)
        self.camera_frame = CameraFrame(self.top_frame, view_controller)
        self.camera_frame.pack(side=LEFT, fill=X, expand=True)
        
        # bottom sub-frame (in main frame)
        self.bottom_frame = Frame(master, bd=1, relief=GROOVE)
        self.bottom_frame.pack(fill=BOTH, expand=True)
        
        # route frame (in bottom sub-frame)
        self.route_frame = RouteFrame(self.bottom_frame, view_controller)
        self.route_frame.pack(side=LEFT, fill=BOTH, padx=5, pady=5, expand=True)

        # info frame (in bottom sub-frame)
        self.info_frame = InfoFrame(self.bottom_frame, view_controller)
        self.info_frame.pack(side=LEFT, fill=BOTH, pady=5, expand=True)

        # controls frame (in bottom sub-frame)
        self.controls_frame = ControlsFrame(self.bottom_frame, view_controller)
        self.controls_frame.pack(side=LEFT, fill=BOTH, padx=5, pady=5, expand=True)
    
    def update_callback(self):
        """ Callback for any view objects that need to requery (rather than observe a model. """
        self.camera_frame.update_callback()

class MapFrame(Frame, object):
    """ UI Frame displaying map. """
    
    def __init__(self, master, view_controller):
        super(MapFrame, self).__init__(master, bd=1, relief=GROOVE)
        self._view_controller = view_controller
        
        # get map image
        image = view_controller.get_current_map()
        
        # scale and display image
        width, height = image.size
        scale = .12
        image_resized = image.resize((int(width*scale), int(height*scale)), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image_resized)
        
        # add overlay
        self.top = Canvas(self, width=480, height=240)
        self.top.create_image((25,0), image=photo, anchor=NW)
        self.top.create_oval((35,190,75,230), width=2, fill="white")
        self.top.create_text((55,210), text="H", font=14)
        self.image=photo
        self.top.bind("<Button-1>", self.click_callback)
        self.top.bind("<B1-Motion>", self.move_callback)
        self.top.pack(fill=X)

    def click_callback(self, event):
        print "clicked at", event.x, event.y

    def move_callback(self, event):
        print event.x, event.y

class CameraFrame(Frame, object):
    """ UI Frame displaying camera image. """
    
    def __init__(self, master, view_controller):
        super(CameraFrame, self).__init__(master, bd=1, relief=SUNKEN)
        self._view_controller = view_controller
        # display image
        self.cnvs_camera = Canvas(self, width=320, height=240)
        self.update_image()
        self.cnvs_camera.pack(fill=BOTH)
    
    def update_image(self):
        # get latest image
        image = self._view_controller.last_img
        photo = ImageTk.PhotoImage(image)
        
        # display it
        self.cnvs_camera.create_image((0,0), image=photo, anchor=NW)
        #self.cnvs_camera.configure(image = photo)
        self.image = photo
    
    def update_callback(self):
        self.update_image()

class InfoFrame(Frame, object):
    """ UI Frame displaying information and status. """
    
    def __init__(self, master, view_controller):
        super(InfoFrame, self).__init__(master, bd=1, relief=SUNKEN)
        self._view_controller = view_controller

        Label(self, text = "Location Info:", pady=6, anchor=W, justify=LEFT).grid(row=0, columnspan=2, sticky=W)
        
        # latitude
        Label(self, text = "Latitude:", padx=3, anchor=W, justify=LEFT).grid(row=1, sticky=W)
        Label(self, textvariable=view_controller.model.GPS_latitude).grid(row=1, column=1)

        # longitude
        Label(self, text = "Longitude:", padx=3, anchor=W, justify=LEFT).grid(row=2, sticky=W)
        Label(self, textvariable=view_controller.model.GPS_longitude).grid(row=2, column=1)

        # compass heading info
        Label(self, text = "Compass Heading:", padx=3, anchor=W, justify=LEFT).grid(row=3, sticky=W)
        Label(self, textvariable=view_controller.model.compass_heading).grid(row=3, column=1)
        
        # GPS heading info
        Label(self, text = "GPS Heading:", padx=3, anchor=W, justify=LEFT).grid(row=4, sticky=W)
        Label(self, textvariable=view_controller.model.GPS_heading).grid(row=4, column=1)
        Label(self, text = "GPS Speed (knots):", padx=3, anchor=W, justify=LEFT).grid(row=5, sticky=W)
        Label(self, textvariable=view_controller.model.GPS_speed).grid(row=5, column=1)
        Label(self, text = "GPS Altitude:", padx=3, anchor=W, justify=LEFT).grid(row=6, sticky=W)
        Label(self, textvariable=view_controller.model.GPS_altitude).grid(row=6, column=1)
        
        # GPS status
        Checkbutton(self, text="GPX fix?", font=tkFont.Font(weight="bold"), state=DISABLED, variable=view_controller.model.GPS_fix).grid(row=7, column=0, columnspan=2, sticky=E)
        
        Label(self, text = "# satellites:", padx=3, anchor=W, justify=LEFT).grid(row=8, sticky=W)
        Label(self, textvariable=view_controller.model.GPS_satellite_count).grid(row=8, column=1)

        Label(self, text = "Other Info:", pady=6, anchor=W, justify=LEFT).grid(row=9, columnspan=2, sticky=W)

        # date and time
        Label(self, text = "Time:", padx=3, anchor=W, justify=LEFT).grid(row=10, sticky=W)
        Label(self, textvariable=view_controller.model.time).grid(row=10, column=1)
        Label(self, text = "Date:", padx=3, anchor=W, justify=LEFT).grid(row=11, sticky=W)
        Label(self, textvariable=view_controller.model.date).grid(row=11, column=1)
        
        Label(self, text = "Temperature:", padx=3, anchor=W, justify=LEFT).grid(row=12, sticky=W)
        Label(self, textvariable=view_controller.model.temperature).grid(row=12, column=1)

class ControlsFrame(Frame, object):
    """ UI Frame displaying controls for heading and throttle. """
    
    def __init__(self, master, view_controller):
        super(ControlsFrame, self).__init__(master, bd=1, relief=SUNKEN)
        self._view_controller = view_controller
        
        Label(self, text = "Control Mode:", pady=6, bd=1, anchor=W, justify=LEFT).pack(fill=X, padx=2, expand=True)
        
        # top frame
        self.top_frame = Frame(self)
        self.top_frame.pack(fill=X)
        
        # mode buttons
        self.btn_manual = Button(self.top_frame, text="Manual", command=self.on_set_manual_mode)
        self.btn_manual.config(relief=SUNKEN)
        self.btn_manual.pack(side=LEFT, padx=3)        
        
        self.btn_pause = Button(self.top_frame, text="Pause", command=self.on_pause)
        self.btn_pause.pack(side=LEFT)
        
        self.btn_auto = Button(self.top_frame, text="AutoPilot", command=self.on_set_auto_pilot_mode)
        self.btn_auto.pack(side=LEFT, padx=3)
        
        # centre frame
        Label(self, text = "Heading:", pady=6, bd=1, anchor=W, justify=LEFT).pack(fill=X, padx=2, expand=True)
        
        # rudder heading
        self.scl_rudder = Scale(self, orient=HORIZONTAL, from_=-45, to=45, command=self.on_rudder)
        self.scl_rudder.set(0)
        self.scl_rudder.pack(fill=X, expand=True, padx=5)
        
        self.btn_zero_heading = Button(self, text="Centre Rudder", command=self.on_zero_heading)
        self.btn_zero_heading.pack(padx=3)

        # throttle level
        Label(self, text = "Throttle:", pady=6, bd=1, anchor=W, justify=LEFT).pack(fill=X, padx=2, expand=True)
        
        self.btn_zero_throttle = Button(self, text="Zero Throttle", command=self.on_zero_throttle)
        self.btn_zero_throttle.pack(side=RIGHT, padx=3)
        
        self.scl_speed_controller = Scale(self, length=200, from_=100, to=-100, command=self.on_throttle)
        self.scl_speed_controller.set(0)
        self.scl_speed_controller.pack(fill=Y, pady=5)

    def on_set_manual_mode(self):
        """ event handler for mode change """
        self.btn_manual.config(relief=SUNKEN)
        self.btn_auto.config(relief=RAISED)
        self._view_controller.set_manual_mode()
    
    def on_pause(self):
        """ event handler for mode change """
        self.btn_manual.config(relief=RAISED)
        self.btn_auto.config(relief=RAISED)
        self._view_controller.halt()
    
    def on_set_auto_pilot_mode(self):
        """ event handler for mode change """
        self.btn_manual.config(relief=RAISED)
        self.btn_auto.config(relief=SUNKEN)
        self._view_controller.set_auto_pilot_mode()
    
    def on_rudder(self, value):
        """ event handler for heading change """
        # only apply in manual mode
        self._view_controller.set_steering(value)
    
    def on_throttle(self, value):
        """ event handler for throttle change """
        # only apply in manual mode
        self._view_controller.set_throttle(value)
    
    def on_zero_throttle(self):        
        """ event handler for throttle change """
        # only apply in manual mode
        self._view_controller.set_throttle(0)
        self.scl_speed_controller.set(0)

    def on_zero_heading(self):        
        """ event handler for heading change """
        # only apply in manual mode
        self._view_controller.set_steering(0)
        self.scl_rudder.set(0)

class RouteFrame(Frame, object):
    """ UI Frame with buttons for user interactions. """
    
    def __init__(self, master, view_controller):
        super(RouteFrame, self).__init__(master, bd=1, relief=SUNKEN)
        self._view_controller = view_controller
        
        Label(self, text = "Route Planning:", pady=6, anchor=W, justify=LEFT).grid(row=0, columnspan=4, sticky=W)
        
        # waypoints list
        Label(self, text = "Waypoint", pady=3, anchor=W, justify=LEFT).grid(row=1, column=0, sticky=W)
        Label(self, text = "Latitude", pady=3, anchor=W, justify=LEFT).grid(row=1, column=1, sticky=W)
        Label(self, text = "Longitude", pady=3, anchor=W, justify=LEFT).grid(row=1, column=2, sticky=W)
        Label(self, text = "Remove", pady=3, anchor=W, justify=LEFT).grid(row=1, column=3, sticky=W)
        
        self.lstbx_waypoints = Listbox(self, height=10)
        self.lstbx_waypoints.grid(row=2, rowspan=10, columnspan=4, padx=3, sticky=NSEW)

        # load / save route
        self.btn_load = Button(self, text="Load GPX", command=self.on_load_gpx)
        self.btn_load.grid(row=13, column=0)
        self.btn_save = Button(self, text="Save GPX", state=DISABLED, command=self.on_save_gpx)
        self.btn_save.grid(row=13, column=1)
        self.btn_route = Button(self, pady=4, text="Open Plannner", state=DISABLED, command=self.on_open_planner)
        self.btn_route.grid(row=13, column=2, columnspan=2)

        # misc
        Checkbutton(self, text = "Capture Images", variable=view_controller.model.capture_img_enabled).grid(row=15, column=2, columnspan=2, sticky=E)

    def on_load_gpx(self):
        """ event handler for loading gpx file """
        self._view_controller.load_gpx()
        self.lstbx_waypoints.delete(0,END)
        for item in self._view_controller.model.waypoints:
            self.lstbx_waypoints.insert(END, item)

    def on_save_gpx(self):
        """ event handler for save gpx file """
        self._view_controller.save_gpx()

    def on_open_planner(self):
        """ event handler for planner window """
        pass
