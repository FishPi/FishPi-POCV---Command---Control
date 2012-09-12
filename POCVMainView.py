
from Tkinter import *
from PIL import Image, ImageTk

from POCVMainViewController import *

root = 0
controller = 0

class Main:

	def __init__(self,master,view_controller):
                root = master
                controller = view_controller

                self.frm_geo = MapFrame(master)
	        self.frm_geo.pack(fill=X)
	
	      	self.frm_controls = Frame(master,bd=1,relief=GROOVE)
	       	self.frm_controls.pack(fill=X)

		self.frm_info = InfoFrame(self.frm_controls)
	        self.frm_info.pack(side=LEFT,fill=X,expand=True)
	
	        self.frm_btn = ButtonFrame(self.frm_controls)
	        self.frm_btn.pack( side=LEFT,fill=X,expand=True)

	        self.frm_cam = CameraFrame(self.frm_controls)
	        self.frm_cam.pack(side=LEFT,fill=X,expand=True)


class MapFrame(Frame,object):
	
	def __init__(self,master):
		super(MapFrame,self).__init__(master,bd=1,relief=GROOVE)

		image = Image.open("bournville_model_yachting_club_satellite.tif")
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

class InfoFrame(Frame,object):

	def __init__(self,master):
		super(InfoFrame,self).__init__(master, bd=1,relief=SUNKEN)

		self.lbl_latitude = Label(self, text = "Lat: \t",pady=6,bd=1,relief=GROOVE,anchor=W,justify=LEFT)
		self.lbl_latitude.pack(fill=X,expand=True)

		self.lbl_longitude = Label(self, text = "Long: \t",pady=6,bd=1,relief=GROOVE,anchor=W,justify=LEFT)
		self.lbl_longitude.pack(fill=X,expand=True)

		self.scl_rudder = Scale(self,orient=HORIZONTAL)
		self.scl_rudder.pack(fill=X, expand =True)

		self.scl_speed_controller = Scale(self)
		self.scl_speed_controller.pack(fill=Y,side=LEFT)

		self.lbl_signals = Label(self, text = "Satellite Signals",bd=1,relief=GROOVE,anchor=W,justify=LEFT)
		self.lbl_signals.pack(fill=X,expand=True)

		self.lstbx_signals = Listbox(self,height=4)
		self.lstbx_signals.pack(fill=X)

		self.lbl_time = Label(self, text = "Time : HH:MM:SS", pady=6, bd=1, relief=GROOVE, anchor=W,justify=LEFT)
		self.lbl_time.pack(fill=X,expand=True)

		self.lbl_date = Label(self, text = "Date : DD:MM:YY", pady=6, bd=1, relief=GROOVE, anchor=W,justify=LEFT)
		self.lbl_date.pack(fill=X,expand=True)

		self.rdbtn_sat_lock = Radiobutton(self, text = "Satellite lock")
		self.rdbtn_sat_lock.pack(fill=X,expand=True,side=RIGHT)
		
		self.btn_config = Button(self, text = "Configuration")
		self.btn_config.pack(fill=X,expand=True,side=RIGHT)

class ButtonFrame(Frame,object):

	def __init__(self,master):
		super(ButtonFrame,self).__init__(master, bd=1,relief=SUNKEN)

		self.btn_route = Button(self,pady=4,text="Open Route Planning")
        	self.btn_route.pack(fill=X)

        	self.btn_save = Button(self,pady=4,text="Save GPX Track")
        	self.btn_save.pack(fill=X)

        	self.chkbtn_capture_img = Checkbutton(self, text = "Capture Images")
        	self.chkbtn_capture_img.pack(fill=X,expand=True)

       		self.chkbtn_record_vid = Checkbutton(self, text = "Record Video")
       		self.chkbtn_record_vid.pack(fill=X,expand=True)

        	self.chkbtn_enable_camera = Checkbutton(self, text = "Enable Camera")
        	self.chkbtn_enable_camera.pack(fill=X,expand=True)

		## Variable bound to selection box selection
        	self.time_delay= StringVar(root)
        	self.time_delay.set("10 Seconds")
        
        	self.optmnu_delay = OptionMenu(self,self.time_delay,"10 Seconds")
        	self.optmnu_delay.pack(fill=X,expand=True)

        	self.rdbtn_sat_lock = Radiobutton(self, text = "Navigation Paused",fg="red")
        	self.rdbtn_sat_lock.pack(fill=X,expand=True)

class CameraFrame(Frame,object):

	def __init__(self,master):
		super(CameraFrame,self).__init__(master, bd=1,relief=SUNKEN)

		self.bottom = Label(self, text = "Destination \t Lat\\Long \t Remove")
        	self.bottom.pack(fill=X)

        	self.lstbx_waypoints = Listbox(self,height=5)
        	self.lstbx_waypoints.pack(fill=X)

		image = Image.open("cam.jpg")
		photo = ImageTk.PhotoImage(image)
        	self.cnvs_camera = Canvas(self)
		self.cnvs_camera.create_image((0,0),image=photo,anchor=NW)
		self.image=photo
        	self.cnvs_camera.pack(fill=BOTH)

