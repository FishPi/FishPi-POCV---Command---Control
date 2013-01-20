
#
# FishPi - An autonomous drop in the ocean
#
# Main View classes for POCV UI.
#

import logging
import socket

import wx
from camera_view import CameraPanel

class MainWindow(wx.Frame):

    def __init__(self, parent, title, server, rpc_port, camera_port):
        self._server = server
        self._rpc_port = rpc_port
        self._camera_port = camera_port
        self.rpc_client = None
        
        wx.Frame.__init__(self, parent, title=title, size=(1024, 800))
        
        #build ui
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer_view = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_control = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.sizer_view, 0, wx.EXPAND)
        self.sizer.Add(self.sizer_control, 0, wx.EXPAND)
            
        # map frame
        self.map_frame = MapPanel(self.panel)
        self.sizer_view.Add(self.map_frame, 3, wx.EXPAND)
        
        # camera frame
        self.camera_frame = CameraPanel(self.panel, server, camera_port, True)
        self.sizer_view.Add(self.camera_frame, 1, wx.EXPAND)
        
        # waypoint frame
        self.waypoint_frame = WayPointPanel(self.panel)
        self.sizer_control.Add(self.waypoint_frame, 1, wx.EXPAND)
            
        # display frame
        self.display_frame = DisplayPanel(self.panel, self)
        self.sizer_control.Add(self.display_frame, 1, wx.EXPAND)
            
        # auto pilot frame
        self.autopilot_frame = AutoPilotPanel(self.panel, self)
        self.sizer_control.Add(self.autopilot_frame, 1, wx.EXPAND)
            
        # manual pilot frame
        self.manualpilot_frame = ManualPilotPanel(self.panel)
        self.sizer_control.Add(self.manualpilot_frame, 1, wx.EXPAND)
            
        self.CreateStatusBar()

        self.panel.SetSizerAndFit(self.sizer)
        #self.Fit()
    
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
        if self.rpc_client:
            self.rpc_client.close_connection()

    def update(self):
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

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.header = wx.StaticText(self, label="Navigation Map")
        self.SetBackgroundColour('#3333FF')        

class WayPointPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.header = wx.StaticText(self, label="Waypoints")
        self.SetBackgroundColour('#FFCC33')

class DisplayPanel(wx.Panel):
    
    def __init__(self, parent, host):
        wx.Panel.__init__(self, parent)
        self.host = host
        self.header = wx.StaticText(self, label="Current Status")
        self.SetBackgroundColour('#CC9966')

        self.btnUpdate = wx.Button(self, -1, "Update")
        self.btnUpdate.Bind(wx.EVT_BUTTON, self.update)

    def update(self):
        if self.host.rpc_client:
            self.host.rpc_client.update()

class AutoPilotPanel(wx.Panel):
    
    def __init__(self, parent, host):
        wx.Panel.__init__(self, parent)
        self.host = host
        self.header = wx.StaticText(self, label="Auto Pilot")
        self.SetBackgroundColour('#CC0000')
        self.speed = wx.Slider(self, value=0, minValue=-100, maxValue=100, style=wx.SL_VERTICAL)
        self.heading = wx.Slider(self, value=0, minValue=-45, maxValue=45, style=wx.SL_HORIZONTAL)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.txtA = wx.TextCtrl(self, -1)
        self.sizer.Add(self.txtA)
        
        self.txtB = wx.TextCtrl(self, -1)
        self.sizer.Add(self.txtB)
    
        self.btnAuto = wx.Button(self, -1, "Engage Autopilot")
        self.btnAuto.Bind(wx.EVT_BUTTON, self.engage)
        self.sizer.Add(self.btnAuto)

        self.SetSizerAndFit(self.sizer)

    
    def engage(self, event):
        if self.host.rpc_client:
            self.host.rpc_client.sum(self.txtA.GetValue(), self.txtB.GetValue())

class ManualPilotPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.header = wx.StaticText(self, label="Manual Pilot")
        self.SetBackgroundColour('#00CC33')

        self.throttle = wx.Slider(self, value=0, minValue=-100, maxValue=100, style=wx.SL_VERTICAL)
        self.throttle.Bind(wx.EVT_SCROLL, self.OnThrottleChange)
        self.steering = wx.Slider(self, value=0, minValue=-45, maxValue=45, style=wx.SL_HORIZONTAL)
        self.steering.Bind(wx.EVT_SCROLL, self.OnSteeringChange)

    def OnThrottleChange(self, e):
        value = e.GetEventObject().GetValue()

    def OnSteeringChange(self, e):
        value = e.GetEventObject().GetValue()



