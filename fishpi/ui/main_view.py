
#
# FishPi - An autonomous drop in the ocean
#
# Main View classes for POCV UI.
#

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
        
        # get latest image
        image = self._view_controller.get_current_photo()
        photo = ImageTk.PhotoImage(image)
        
        # display it
        self.cnvs_camera = Canvas(self, width=320, height=240)
        self.cnvs_camera.create_image((0,0), image=photo, anchor=NW)
        self.image = photo
        self.cnvs_camera.pack(fill=BOTH)

class InfoFrame(Frame, object):
    """ UI Frame displaying information and status. """
    
    def __init__(self, master, view_controller):
        super(InfoFrame, self).__init__(master, bd=1, relief=SUNKEN)
        self._view_controller = view_controller

        self.lbl_latitude = Label(self, text = "Lat: \t", pady=6, bd=1, relief=GROOVE, anchor=W, justify=LEFT)
        self.lbl_latitude.pack(fill=X, expand=True)

        self.lbl_longitude = Label(self, text = "Long: \t", pady=6, bd=1, relief=GROOVE, anchor=W, justify=LEFT)
        self.lbl_longitude.pack(fill=X, expand=True)

        self.lbl_signals = Label(self, text = "Satellite Signals", bd=1, relief=GROOVE, anchor=W, justify=LEFT)
        self.lbl_signals.pack(fill=X, expand=True)

        self.lstbx_signals = Listbox(self, height=4)
        self.lstbx_signals.pack(fill=X)

        self.lbl_time = Label(self, text = "Time : HH:MM:SS", pady=6, bd=1, relief=GROOVE, anchor=W,justify=LEFT)
        self.lbl_time.pack(fill=X, expand=True)

        self.lbl_date = Label(self, text = "Date : DD:MM:YY", pady=6, bd=1, relief=GROOVE, anchor=W,justify=LEFT)
        self.lbl_date.pack(fill=X, expand=True)

        self.rdbtn_sat_lock = Radiobutton(self, text = "Satellite fix")
        self.rdbtn_sat_lock.pack(fill=X, expand=True, side=RIGHT)

        self.btn_config = Button(self, text = "Configuration")
        self.btn_config.pack(fill=X, expand=True, side=RIGHT)

class ControlsFrame(Frame, object):
    """ UI Frame displaying controls for heading and throttle. """
    
    def __init__(self, master, view_controller):
        super(ControlsFrame, self).__init__(master, bd=1, relief=SUNKEN)
        self._view_controller = view_controller
        
        self.lbl_mode = Label(self, text = "Control Mode:", pady=6, bd=1, anchor=W, justify=LEFT)
        self.lbl_mode.pack(fill=X, padx=2, expand=True)
        
        # top frame
        self.top_frame = Frame(self)
        self.top_frame.pack(fill=X)
        
        # mode buttons
        self.btn_manual = Button(self.top_frame, text="Manual", command=self.on_set_manual_mode)
        self.btn_manual.config(relief=SUNKEN)
        self.btn_manual.pack(side=LEFT, padx=3)        
        
        self.btn_pause = Button(self.top_frame, text="Pause", command=self.on_pause)
        self.btn_pause.pack(side=LEFT)
        
        self.btn_auto = Button(self.top_frame, text="Auto Pilot", command=self.on_set_auto_pilot_mode)
        self.btn_auto.pack(side=LEFT, padx=3)
        
        # centre frame
        self.lbl_heading = Label(self, text = "Heading:", pady=6, bd=1, anchor=W, justify=LEFT)
        self.lbl_heading.pack(fill=X, padx=2, expand=True)
        
        # rudder heading
        self.scl_rudder = Scale(self, orient=HORIZONTAL, from_=-45, to=45, command=self.on_rudder)
        self.scl_rudder.set(0)
        self.scl_rudder.pack(fill=X, expand=True, padx=5)
        
        # throttle level
        self.lbl_throttle = Label(self, text = "Throttle:", pady=6, bd=1, anchor=W, justify=LEFT)
        self.lbl_throttle.pack(fill=X, padx=2, expand=True)
        
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
        self._view_controller.set_heading(value)
    
    def on_zero_throttle(self):        
        """ event handler for throttle change """
        # only apply in manual mode
        self._view_controller.set_throttle(0)
        self.scl_speed_controller.set(0)

    def on_throttle(self, value):        
        """ event handler for throttle change """
        # only apply in manual mode
        self._view_controller.set_throttle(value)

class RouteFrame(Frame, object):
    """ UI Frame with buttons for user interactions. """
    
    def __init__(self, master, view_controller):
        super(RouteFrame, self).__init__(master, bd=1, relief=SUNKEN)
        self._view_controller = view_controller
        
        self.bottom = Label(self, text = "Destination \t Lat\\Long \t Remove")
        self.bottom.pack(fill=X)

        self.lstbx_waypoints = Listbox(self,height=5)
        self.lstbx_waypoints.pack(fill=X)

        self.btn_save = Button(self, pady=4, text="Save GPX Track")
        self.btn_save.pack()
        self.btn_route = Button(self, pady=4, text="Open Route Planning")
        self.btn_route.pack()

        self.chkbtn_capture_img = Checkbutton(self, text = "Capture Images")
        self.chkbtn_capture_img.pack(fill=X, expand=True)
