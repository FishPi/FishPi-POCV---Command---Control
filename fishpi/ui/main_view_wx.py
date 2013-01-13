#
# FishPi - An autonomous drop in the ocean
#
# Main View classes for POCV UI.
#

import wx
from camera_view import CameraPanel

class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1024, 800))
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer_view = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_control = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.sizer_view, 0, wx.EXPAND)
        self.sizer.Add(self.sizer_control, 0, wx.EXPAND)
            
        # map frame
        self.map_frame = MapPanel(self.panel)
        self.sizer_view.Add(self.map_frame, 3, wx.EXPAND)
        
        server = "raspberrypi.local"
        port = "8080"
        
        # camera frame
        self.camera_frame = CameraPanel(self.panel, server, port)
        self.sizer_view.Add(self.camera_frame, 1, wx.EXPAND)
        
        # waypoint frame
        self.waypoint_frame = WayPointPanel(self.panel)
        self.sizer_control.Add(self.waypoint_frame, 1, wx.EXPAND)
            
        # display frame
        self.display_frame = DisplayPanel(self.panel)
        self.sizer_control.Add(self.display_frame, 1, wx.EXPAND)
            
        # auto pilot frame
        self.autopilot_frame = AutoPilotPanel(self.panel)
        self.sizer_control.Add(self.autopilot_frame, 1, wx.EXPAND)
            
        # manual pilot frame
        self.manualpilot_frame = ManualPilotPanel(self.panel)
        self.sizer_control.Add(self.manualpilot_frame, 1, wx.EXPAND)
            
        self.CreateStatusBar()

        self.panel.SetSizerAndFit(self.sizer)
        #self.Fit()

        self.Show(True)

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
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.header = wx.StaticText(self, label="Current Status")
        self.SetBackgroundColour('#CC9966')

class AutoPilotPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.header = wx.StaticText(self, label="Auto Pilot")
        self.SetBackgroundColour('#CC0000')
        self.speed = wx.Slider(self, value=0, minValue=-100, maxValue=100, style=wx.SL_VERTICAL)
        self.heading = wx.Slider(self, value=0, minValue=-45, maxValue=45, style=wx.SL_HORIZONTAL)

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



