
#
# FishPi - An autonomous drop in the ocean
#
# Main View classes for POCV UI.
#

import logging
import socket
import datetime

import wx
from camera_view import CameraPanel

class MainWindow(wx.Frame):

    def __init__(self, parent, title, controller, server_name, rpc_port, camera_port):
        self.controller = controller
        self._server_name = server_name
        self._rpc_port = rpc_port
        self._camera_port = camera_port
        
        wx.Frame.__init__(self, parent, title=title, size=(1024, 800))
        
        #build ui
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer_view = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_control = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.sizer_view, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 4)
        self.sizer.Add(self.sizer_control, 1, wx.EXPAND | wx.ALL, 4)
            
        # map frame
        self.map_frame = MapPanel(self.panel, controller)
        self.sizer_view.Add(self.map_frame, 3, wx.EXPAND | wx.RIGHT, 4)
        
        # camera frame
        cam_enabled = self.controller.model.capture_img_enabled
        self.camera_frame = CameraPanel(self.panel, server_name, camera_port, cam_enabled)
        self.sizer_view.Add(self.camera_frame, 1, wx.EXPAND)
        
        # waypoint frame
        self.waypoint_frame = WayPointPanel(self.panel)
        self.sizer_control.Add(self.waypoint_frame, 1, wx.EXPAND | wx.RIGHT, 4)
            
        # display frame
        self.display_frame = DisplayPanel(self.panel, controller)
        self.sizer_control.Add(self.display_frame, 1, wx.EXPAND | wx.RIGHT, 4)
            
        # auto pilot frame
        self.autopilot_frame = AutoPilotPanel(self.panel, controller)
        self.sizer_control.Add(self.autopilot_frame, 1, wx.EXPAND | wx.RIGHT, 4)
            
        # manual pilot frame
        self.manualpilot_frame = ManualPilotPanel(self.panel, controller)
        self.sizer_control.Add(self.manualpilot_frame, 1, wx.EXPAND)
            
        self.CreateStatusBar()

        self.panel.SetSizerAndFit(self.sizer)
    
        # bind events
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # setup callback timer
        interval_time = 250
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(interval_time, False)

    def on_timer(self, event):
        self.update()
    
    def OnClose(self, event):
        logging.debug("UI:\tMain window closing.")
        if self.controller:
            self.controller.close_connection()
        #self.Close(True)

    def update(self):
        """ Callback to perform updates etc. """
        logging.debug("UI:\tIn update...")
        # update controller
        self.controller.update()
        # update screens
        self.display_frame.update()
        self.camera_frame.update()

    @property
    def server(self):
        """ Server address for remote device. """
        return self._server
    
    @property
    def rpc_port(self):
        """ Port for RPC. """
        return self._rpc_port
    
    @property
    def camera_port(self):
        """ Port for camera stream. """
        return self._camera_port

class MapPanel(wx.Panel):

    def __init__(self, parent, view_controller):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        #self.header = wx.StaticText(self, label="Navigation Map")

        self._view_controller = view_controller
        # get map image
        #image = view_controller.get_current_map()
        #wx.StaticBitmap(self, -1, image, (10, 5), (image.GetWidth(), image.GetHeight()))
        #wx.StaticBitmap(self, -1, image, (10, 5), (640, 320))

class WayPointPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.sizer = wx.GridBagSizer(vgap=2, hgap=2)
        
        self.header = wx.StaticText(self, label="Waypoints")
        self.sizer.Add(self.header, (0,0), (1,2), wx.EXPAND | wx.ALL, 4)
        
        self.sizer.Add(wx.StaticLine(self), (1,0), (1,2), wx.EXPAND | wx.ALL, 4)

        self.SetSizerAndFit(self.sizer)


class DisplayPanel(wx.Panel):
    
    def __init__(self, parent, controller):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.controller = controller
        
        self.sizer = wx.GridBagSizer(vgap=2, hgap=2)

        self.header = wx.StaticText(self, label="Current Status")
        self.sizer.Add(self.header, (0,0), (1,2), wx.EXPAND | wx.ALL, 4)        

        self.sizer.Add(wx.StaticLine(self), (1,0), (1,2), wx.EXPAND | wx.ALL, 4)
        
        self.l1 = wx.StaticText(self, label="Location Info:")
        self.sizer.Add(self.l1, (2,0), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        #self.t1 = wx.TextCtrl(self, value="----", style=wx.TE_READONLY)
        #self.sizer.Add(self.t1, (2,1), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.l2 = wx.StaticText(self, label="Latitude:")
        self.sizer.Add(self.l2, (3,0), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.t2 = wx.TextCtrl(self, value="----", style=wx.TE_READONLY)
        self.sizer.Add(self.t2, (3,1), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.l3 = wx.StaticText(self, label="Longitude:")
        self.sizer.Add(self.l3, (4,0), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.t3 = wx.TextCtrl(self, value="----", style=wx.TE_READONLY)
        self.sizer.Add(self.t3, (4,1), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.l4 = wx.StaticText(self, label="Compass Heading:")
        self.sizer.Add(self.l4, (5,0), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.t4 = wx.TextCtrl(self, value="----", style=wx.TE_READONLY)
        self.sizer.Add(self.t4, (5,1), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.l5 = wx.StaticText(self, label="GPS Heading:")
        self.sizer.Add(self.l5, (6,0), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.t5 = wx.TextCtrl(self, value="----", style=wx.TE_READONLY)
        self.sizer.Add(self.t5, (6,1), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.l6 = wx.StaticText(self, label="GPS Speed (knots):")
        self.sizer.Add(self.l6, (7,0), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.t6 = wx.TextCtrl(self, value="----", style=wx.TE_READONLY)
        self.sizer.Add(self.t6, (7,1), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.l7 = wx.StaticText(self, label="GPS Altitude:")
        self.sizer.Add(self.l7, (8,0), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.t7 = wx.TextCtrl(self, value="----", style=wx.TE_READONLY)
        self.sizer.Add(self.t7, (8,1), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
    
        self.cb_fix = wx.CheckBox(self, label="GPS fix?")
        self.cb_fix.SetValue(False)
        self.sizer.Add(self.cb_fix, (9,0), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        
        self.l8 = wx.StaticText(self, label="# satellites:")
        self.sizer.Add(self.l8, (10,0), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.t8 = wx.TextCtrl(self, value="----", style=wx.TE_READONLY)
        self.sizer.Add(self.t8, (10,1), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)

        self.sizer.Add(wx.StaticLine(self), (11,0), (1,2), wx.EXPAND | wx.ALL, 4)

        self.l9 = wx.StaticText(self, label="Other Info:")
        self.sizer.Add(self.l9, (12,0), (1,1), wx.EXPAND | wx.ALL, 4)
        self.l10 = wx.StaticText(self, label="Time:")
        self.sizer.Add(self.l10, (13,0), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.t10 = wx.TextCtrl(self, value="----", style=wx.TE_READONLY)
        self.sizer.Add(self.t10, (13,1), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.l11 = wx.StaticText(self, label="Date:")
        self.sizer.Add(self.l11, (14,0), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.t11 = wx.TextCtrl(self, value="----", style=wx.TE_READONLY)
        self.sizer.Add(self.t11, (14,1), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.l12 = wx.StaticText(self, label="Temperature:")
        self.sizer.Add(self.l12, (15,0), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        self.t12 = wx.TextCtrl(self, value="----", style=wx.TE_READONLY)
        self.sizer.Add(self.t12, (15,1), (1,1), wx.EXPAND | wx.LEFT | wx.RIGHT, 2)
        
        #self.btnUpdate = wx.Button(self, -1, "Update")
        #self.btnUpdate.Bind(wx.EVT_BUTTON, self.update)
        self.sizer.AddGrowableCol(0)
        self.SetSizerAndFit(self.sizer)

    def update(self):
        self.t2.SetValue(str(self.controller.model.GPS_latitude))
        self.t3.SetValue(str(self.controller.model.GPS_longitude))
            
        self.t5.SetValue(str(self.controller.model.GPS_heading))
        self.t6.SetValue(str(self.controller.model.GPS_speed))
        self.t7.SetValue(str(self.controller.model.GPS_altitude))
        
        self.cb_fix.SetValue(self.controller.model.GPS_fix)
        self.t8.SetValue(str(self.controller.model.GPS_satellite_count))
            
        # compass data
        self.t4.SetValue(str(self.controller.model.compass_heading))
            
        # time data
        self.t10.SetValue(str(self.controller.model.time))
        self.t11.SetValue(str(self.controller.model.date))
    
        # other data
        self.t12.SetValue(str(self.controller.model.temperature))

class AutoPilotPanel(wx.Panel):
    
    def __init__(self, parent, controller):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.controller = controller
        self.sizer = wx.GridBagSizer(vgap=4, hgap=4)
        self.SetSizerAndFit(self.sizer)
        
        self.header = wx.StaticText(self, label="Auto Pilot")
        self.sizer.Add(self.header, (0,0),  (1,3), wx.EXPAND | wx.ALL, 4)

        self.sizer.Add(wx.StaticLine(self), (1,0), (1,3), wx.EXPAND | wx.ALL, 4)
        
        self.lblHeading = wx.StaticText(self, label="--")
        self.sizer.Add(self.lblHeading, (3,0), (1,3), wx.CENTER | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)

        self.heading = wx.Slider(self, value=0, minValue=-45, maxValue=45, style=wx.SL_HORIZONTAL)
        self.heading.Bind(wx.EVT_SCROLL, self.on_heading_scroll)
        self.sizer.Add(self.heading, (4, 0), (1,3), wx.EXPAND | wx.ALL, 2)

        self.btnCentreRudder = wx.Button(self, -1, "Zero Heading")
        self.btnCentreRudder.Bind(wx.EVT_BUTTON, self.zero_heading)
        self.sizer.Add(self.btnCentreRudder, (5,0), (1,3), wx.ALIGN_CENTER | wx.ALL, 2)
        
        self.lblThrottle = wx.StaticText(self, label="--")
        self.sizer.Add(self.lblThrottle, (7,0), (3,1), wx.CENTER | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 2)

        self.speed = wx.Slider(self, value=0, minValue=-100, maxValue=100, style=wx.SL_VERTICAL)
        self.speed.Bind(wx.EVT_SCROLL, self.on_speed_scroll)
        self.sizer.Add(self.speed, (7, 1), (3,1), wx.EXPAND | wx.ALL, 2)
        
        self.btnZeroThrottle = wx.Button(self, -1, "Zero Speed")
        self.btnZeroThrottle.Bind(wx.EVT_BUTTON, self.zero_speed)
        self.sizer.Add(self.btnZeroThrottle, (7,2), (3,1), wx.ALIGN_CENTER | wx.ALL, 2)
            
        self.btnAuto = wx.Button(self, -1, "Engage Autopilot")
        self.btnAuto.Bind(wx.EVT_BUTTON, self.engage)
        self.sizer.Add(self.btnAuto, (2,0), (1,1), wx.ALL, 2)

        self.btnHalt = wx.Button(self, -1, "Halt!")
        self.btnHalt.Bind(wx.EVT_BUTTON, self.halt)
        self.sizer.Add(self.btnHalt, (10,2), (1,1), wx.ALL, 2)
        
        self.SetSizerAndFit(self.sizer)
    
    
    def engage(self, event):
        # tell controller to engage autopilot
        self.controller.set_auto_pilot_mode()
        self.send_update()

    def halt(self, event):
        # tell controller to halt
        self.speed.SetValue(0.0)
        self.heading.SetValue(0.0)
        self.controller.halt()

    def zero_speed(self, event):
        self.speed.SetValue(0.0)
        self.send_update()
    
    def zero_heading(self, event):
        self.heading.SetValue(0.0)
        self.send_update()
    
    def on_speed_scroll(self, event):
        #value = event.GetEventObject().GetValue()
        #print value
        self.send_update()
    
    def on_heading_scroll(self, event):
        #value = event.GetEventObject().GetValue()
        #print value
        self.send_update()

    def send_update(self):
        sp = self.speed.GetValue()
        he = self.heading.GetValue()
        self.controller.set_navigation(sp, he)

class ManualPilotPanel(wx.Panel):
    
    def __init__(self, parent, controller):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.controller = controller
        
        self.sizer = wx.GridBagSizer(vgap=4, hgap=4)
        
        self.header = wx.StaticText(self, label="Manual Pilot")
        self.sizer.Add(self.header, (0,0),  (1,3), wx.EXPAND | wx.ALL, 4)
       
        self.sizer.Add(wx.StaticLine(self), (1,0), (1,3), wx.EXPAND | wx.ALL, 4)
        
        self.lblHeading = wx.StaticText(self, label="--")
        self.sizer.Add(self.lblHeading, (3,0), (1,3), wx.CENTER | wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 2)
        
        self.steering = wx.Slider(self, value=0, minValue=-45, maxValue=45, style=wx.SL_HORIZONTAL)
        self.steering.Bind(wx.EVT_SCROLL, self.on_steering_scroll)
        self.sizer.Add(self.steering, (4, 0), (1,3), wx.EXPAND | wx.ALL, 2)

        self.btnCentreRudder = wx.Button(self, -1, "Centre Rudder")
        self.btnCentreRudder.Bind(wx.EVT_BUTTON, self.centre_rudder)
        self.sizer.Add(self.btnCentreRudder, (5,0), (1,3), wx.ALIGN_CENTER | wx.ALL, 2)

        self.lblThrottle = wx.StaticText(self, label="--")
        self.sizer.Add(self.lblThrottle, (7,0), (3,1), wx.CENTER | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 2)
        
        self.throttle = wx.Slider(self, value=0, minValue=-100, maxValue=100, style=wx.SL_VERTICAL)
        self.throttle.Bind(wx.EVT_SCROLL, self.on_throttle_scroll)
        self.sizer.Add(self.throttle, (7, 1), (3,1), wx.EXPAND | wx.ALL, 2)
    
        self.btnZeroThrottle = wx.Button(self, -1, "Zero Throttle")
        self.btnZeroThrottle.Bind(wx.EVT_BUTTON, self.zero_throttle)
        self.sizer.Add(self.btnZeroThrottle, (7,2), (3,1), wx.ALIGN_CENTER | wx.ALL, 2)
        
        self.btnManual = wx.Button(self, -1, "Engage Manual")
        self.btnManual.Bind(wx.EVT_BUTTON, self.engage)
        self.sizer.Add(self.btnManual, (2,0), (1,1), wx.ALL, 2)

        self.btnHalt = wx.Button(self, -1, "Halt!")
        self.btnHalt.Bind(wx.EVT_BUTTON, self.halt)
        self.sizer.Add(self.btnHalt, (10,2), (1,1), wx.ALL, 2)
        
        self.SetSizerAndFit(self.sizer)

    def engage(self, event):
        # tell controller to engage manual
        self.controller.set_manual_mode()
        self.send_update()

    def halt(self, event):
        # tell controller to halt
        self.throttle.SetValue(0.0)
        self.steering.SetValue(0.0)
        self.controller.halt()

    def zero_throttle(self, event):
        self.throttle.SetValue(0.0)
        self.send_update()
    
    def centre_rudder(self, event):
        self.steering.SetValue(0.0)
        self.send_update()
    
    def on_throttle_scroll(self, event):        
        #value = event.GetEventObject().GetValue()
        #print value
        self.send_update()
            
    def on_steering_scroll(self, event):
        #value = event.GetEventObject().GetValue()
        #print value
        self.send_update()
    
    def send_update(self):
        th = self.throttle.GetValue()
        st = self.steering.GetValue()
        self.controller.set_drive(th, st)
