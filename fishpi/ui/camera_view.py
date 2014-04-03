#!/usr/bin/python
#
# FishPi - An autonomous drop in the ocean
#
# Simple viewer for onboard camera
#

import argparse
import sys

import httplib
import socket
from StringIO import StringIO

import wx

class CameraPanel(wx.Panel):
    
    def __init__(self, parent, server, port, enabled=True):
        wx.Panel.__init__(self, parent, size=(320,240), style=wx.SUNKEN_BORDER)
        # self.enabled = enabled
        self.enabled = False  # debug. Remove this!!!
        if self.enabled:
            ipaddr = socket.gethostbyname(server)
            self._conn = httplib.HTTPConnection(ipaddr, port)
            self.update()
    
    def update(self):
        """ Update panel with new image. """
        if self.enabled:
            self._conn.request("GET", "/?action=snapshot")
            r1 = self._conn.getresponse()
            data = r1.read()
            img = wx.ImageFromStream(StringIO(data))
            bmp = wx.BitmapFromImage(img)
            ctrl = wx.StaticBitmap(self, -1, bmp)

class CameraViewer(wx.Frame):
    """ Simple Frame containing CameraPanel and timer callback. """
    
    def __init__(self, parent, title, server, port):
        # initialise frame
        wx.Frame.__init__(self, parent, title=title, size=(320, 240))
        # add camera frame
        print "using camera at %s:%s" % (server, port)
        self.camera_frame = CameraPanel(self, server, port)
        # setup callback timer
        interval_time = 250
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(interval_time, False)
        # and go
        self.Show()

    def on_timer(self, event):
        self.camera_frame.update()

def main():
    """ Main entry point for application. Parses command line args for server and launches wx. """
    # parse cmd line args
    parser = argparse.ArgumentParser(description="raspberry pi - onboard view")
    parser.add_argument("-server", help="server for camera stream", default="raspberrypi.local", type=str, action='store')
    parser.add_argument("-port", help="port for camera stream", default=8080, type=int, action='store')
    selected_args = parser.parse_args()
    server = selected_args.server
    port = selected_args.port
    
    # run UI loop
    app = wx.App(False)
    frame = CameraViewer(None, "raspberry pi - onboard view", server, port)
    app.MainLoop()
    return 0

if __name__ == "__main__":
    status = main()
    sys.exit(status)
