#!/usr/bin/python
#
# FishPi - An autonomous drop in the ocean
#
# Simple viewer for onboard camera
#

import argparse
import io
import sys
import socket
import struct
# from StringIO import StringIO

import wx


class CameraPanel(wx.Panel):

    def __init__(self, parent, server, port=8001, enabled=True):
        wx.Panel.__init__(self, parent,
            size=(320, 240), style=wx.SUNKEN_BORDER)
        self.enabled = enabled
        if self.enabled:
            self.client_socket = socket.socket()
            self.client_socket.connect((server, port))
            # Make a file-like object out of the connection
            self.connection = self.client_socket.makefile('wb')
            self.update()

    def update(self):
        """ Update panel with new image. """
        if self.enabled:
            try:
                # Read the length of the image as a 32-bit unsigned int. If the
                # length is zero, quit
                image_len = struct.unpack('<L', self.connection.read(4))[0]
                if not image_len:
                    print "Could not read image length. Skipping.."
                    self.enabled = False
                    return
                print("Image length: %s" % image_len)
                # Construct a stream to hold the image data and read the image
                # data from the connection
                image_stream = io.BytesIO()
                image_stream.write(self.connection.read(image_len))
                # Rewind the stream, open it as an image with PIL and do some
                # processing on it
                image_stream.seek(0)
                # this part is from the previous version of this.
                # let's see how it integrates with the new code
                # img = wx.ImageFromStream(StringIO(image_stream))
                img = wx.ImageFromStream(image_stream)
                bmp = wx.BitmapFromImage(img)
                ctrl = wx.StaticBitmap(self, -1, bmp)
                # image = Image.open(image_stream)
                # print('Image is %dx%d' % image.size)
                # image.verify()
                # print('Image is verified')
            except Exception, e:
                print("Exception: %s, closing client" % e)
                self.shut_down()

    def shut_down(self):
        self.connection.close()
        self.client_socket.close()


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
    """ Main entry point for application.
        Parses command line args for server and launches wx. """
    # parse cmd line args
    parser = argparse.ArgumentParser(description="raspberry pi - onboard view")
    parser.add_argument("-server", help="server for camera stream",
        default="raspberrypi.local", type=str, action='store')
    parser.add_argument("-port", help="port for camera stream",
        default=8000, type=int, action='store')
    selected_args = parser.parse_args()
    server = selected_args.server
    port = selected_args.port

    # run UI loop
    app = wx.App(False)
    frame = CameraViewer(None, "raspberry pi - onboard view", server, port)
    app.MainLoop()
    frame.shut_down()
    return 0

if __name__ == "__main__":
    status = main()
    sys.exit(status)
