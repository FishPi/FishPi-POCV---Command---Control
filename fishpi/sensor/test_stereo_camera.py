#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Simple test of camera functionality
#

from camera import StereoCamera

if __name__ == "__main__":
    print "testing stereo camera..."
    cam = StereoCamera("/dev/video0", "/dev/video1", (320,240))
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    cam = "done"

    print "and in YUV..."
    cam = StereoCamera("/dev/video0", "/dev/video1", (320,240), "YUV")
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    cam = "done"
    
    print "and in HSV..."
    cam = StereoCamera("/dev/video0", "/dev/video1", (320,240), "HSV")
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    cam = "done"
