#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Simple test of camera functionality
#

from CameraController import SingleCamera
from CameraController import StereoCamera

if __name__ == "__main__":
    print "testing single camera..."
    cam = SingleCamera("/dev/video0",  (320,240))
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    print "click.."
    cam = "done"

    print "testing stereo camera..."
    cam = StereoCamera("/dev/video0", "/dev/video1", (320,240))
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    print "click.."
    cam.capture("/home/pi/fishpi/imgs")
    cam = "done"
