
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
        self.create_widgets(master, view_controller)

    def create_widgets(self, master, view_controller):
        """ Create widgets for view. """
        
        # map frame (in main frame)
        self.frm_geo = MapFrame(master, view_controller)
        self.frm_geo.pack(fill=X)
        
        # controls sub-frame (in main frame)
        self.frm_controls = Frame(master, bd=1, relief=GROOVE)
        self.frm_controls.pack(fill=X)
        
        # info frame (in controls sub-frame)
        self.frm_info = InfoFrame(self.frm_controls, view_controller)
        self.frm_info.pack(side=LEFT, fill=X, expand=True)
        
        # buttons frame (in controls sub-frame)
        self.frm_btn = ButtonFrame(self.frm_controls, view_controller)
        self.frm_btn.pack(side=LEFT, fill=X, expand=True)
        
        # camera frame (in controls sub-frame)
        self.frm_cam = CameraFrame(self.frm_controls, view_controller)
        self.frm_cam.pack(side=LEFT, fill=X, expand=True)


class MapFrame(Frame, object):
    """ UI Frame displaying map. """
    
    def __init__(self, master, view_controller):
        super(MapFrame, self).__init__(master, bd=1, relief=GROOVE)
        self._view_controller = view_controller
        
        # get map image
        image = view_controller.get_current_map()
        
        # scale and display
        width, height = image.size
        scale = .2
        image_resized = image.resize((int(width*scale), int(height*scale)), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image_resized)
        self.top = Canvas(self,width=780, height=300)
        self.top.create_image((40,-50),image=photo,anchor=NW)
        self.top.create_oval((50,230,90,270),width=3,fill="white")
        self.top.create_text((70,250),text="H",font=14)
        self.image=photo
        self.top.pack(fill=X)

class InfoFrame(Frame, object):
    """ UI Frame displaying information and status. """
    
    def __init__(self, master, view_controller):
        super(InfoFrame, self).__init__(master, bd=1,relief=SUNKEN)
        self._view_controller = view_controller

        self.lbl_latitude = Label(self, text = "Lat: \t", pady=6, bd=1, relief=GROOVE, anchor=W, justify=LEFT)
        self.lbl_latitude.pack(fill=X, expand=True)

        self.lbl_longitude = Label(self, text = "Long: \t", pady=6, bd=1, relief=GROOVE, anchor=W, justify=LEFT)
        self.lbl_longitude.pack(fill=X, expand=True)

        self.scl_rudder = Scale(self, orient=HORIZONTAL)
        self.scl_rudder.pack(fill=X, expand =True)

        self.scl_speed_controller = Scale(self, from_=100, to=0)
        self.scl_speed_controller.pack(fill=Y, side=LEFT)

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

class ButtonFrame(Frame, object):
    """ UI Frame with buttons for user interactions. """
    
    def __init__(self, master, view_controller):
        super(ButtonFrame, self).__init__(master, bd=1, relief=SUNKEN)
        self._view_controller = view_controller

        self.btn_route = Button(self, pady=4, text="Open Route Planning")
        self.btn_route.pack(fill=X)

        self.btn_save = Button(self, pady=4, text="Save GPX Track")
        self.btn_save.pack(fill=X)

        self.chkbtn_capture_img = Checkbutton(self, text = "Capture Images")
        self.chkbtn_capture_img.pack(fill=X, expand=True)

        self.chkbtn_record_vid = Checkbutton(self, text = "Record Video")
        self.chkbtn_record_vid.pack(fill=X, expand=True)

        self.chkbtn_enable_camera = Checkbutton(self, text = "Enable Camera")
        self.chkbtn_enable_camera.pack(fill=X, expand=True)

        ## Variable bound to selection box selection
        self.time_delay= StringVar()
        self.time_delay.set("10 Seconds")
        
        self.optmnu_delay = OptionMenu(self, self.time_delay, "10 Seconds")
        self.optmnu_delay.pack(fill=X, expand=True)
        
        self.rdbtn_sat_lock = Radiobutton(self, text = "Navigation Paused", fg="red")
        self.rdbtn_sat_lock.pack(fill=X, expand=True)

class CameraFrame(Frame, object):
    """ UI Frame displaying camera image. """
    
    def __init__(self, master, view_controller):
        super(CameraFrame, self).__init__(master, bd=1, relief=SUNKEN)
        self._view_controller = view_controller

        self.bottom = Label(self, text = "Destination \t Lat\\Long \t Remove")
        self.bottom.pack(fill=X)

        self.lstbx_waypoints = Listbox(self,height=5)
        self.lstbx_waypoints.pack(fill=X)

        # get latest image
        image = self._view_controller.get_current_photo()
        
        # display it
        photo = ImageTk.PhotoImage(image)
        self.cnvs_camera = Canvas(self)
        self.cnvs_camera.create_image((0,0),image=photo,anchor=NW)
        self.image=photo
        self.cnvs_camera.pack(fill=BOTH)

