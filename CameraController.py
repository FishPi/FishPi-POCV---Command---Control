
#
# FishPi - An autonomous drop in the ocean
#
#
# CameraController
#  - provides interface for image capture
#

import os
import pygame
import pygame.camera
from pygame.locals import *

class CameraController(object):
    """ Provides access to camera devices. """

    default_res = (320,240)    
    default_colorspace = "RGB"

    def __init__(self, configuration):
        self.configuration = configuration
        # set capture path
        self.imgs_path = configuration.imgs_path
        # get and initialise devices
        #self._video_devices = configuration.video_devices
        pygame.init()
        pygame.camera.init()
        camlist = pygame.camera.list_cameras()
        if camlist and len(camlist) == 1:
            self._camera = SingleCamera(camlist[0], self.default_res, self.default_colorspace)
        elif camlist and len(camlist) >= 2:
            self._camera = StereoCamera(camlist[0], camlist[1], self.default_res, self.colorspace)
    
    def capture_now(self):
        """ Captures an image now. """
        self._camera.capture(self.imgs_path)

    @property
    def last_img(self):
        """ Last image captured. """
        return self._camera.last_img

    def set_capture_mode(self, mode): 
        pass

    def enable_capture(self):
        pass

    def disable_capture(self):
        pass

class SingleCamera(object):
    """ Provides access to a single camera """
    
    def __init__(self, camera_addr, res, colorspace="RBG"):
        pygame.init()
        pygame.camera.init()
        self._camera = pygame.camera.Camera(camera_addr, res, colorspace)
        self._camera.start()

    def __del__(self):
        self._camera.stop()

    def capture(self, path):
        """ Captures image to given path """
        self._last_img = self._camera.get_image()
        file_stem = self.next_img_file(path)
        pygame.image.save(self._last_img, os.path.join(path, file_stem+'.png'))

    @property
    def last_img(self):
        """ Last image captured. """
        return self._last_img

    def next_img_file(self, path):
        """ Checks for most recent image file and increments file index count. """
        files = os.listdir(path)
        if not files:
            return 'img0000'
        else:
            # plenty of other (better ways to do this, feel free to change and filter)
            files.sort(key=(lambda k:os.path.getmtime(os.path.join(path,k))), reverse=True)
            last_name = files[0]
            #idx = str(int(last_name.replace('img', '').replace('.png','')) + 1).zfill(4)
            idx = str(int(last_name.replace('img', '').replace('.png','').replace('_L','').replace('_R','')) + 1).zfill(4)
            next_name = 'img' + idx
            return next_name

class StereoCamera(object):
    """ Provides acces to pair of cameras. Convention is (left, right). """

    def __init__(self, camera_addr_left, camera_addr_right, res, colorspace="RGB"):
        pygame.init()
        pygame.camera.init()
        self._camera_left = pygame.camera.Camera(camera_addr_left, res, colorspace)
        self._camera_left.start()
        self._camera_right = pygame.camera.Camera(camera_addr_right, res, colorspace)
        self._camera_right.start()

    def __del__(self):
        self._camera_left.stop()
        self._camera_right.stop()

    def capture(self, path):
        """ Captures image to given path """
        self._last_img_left = self._camera_left.get_image()
        self._last_img_right = self._camera_right.get_image()
        file_stem = self.next_img_file(path)
        pygame.image.save(self._last_img_left, os.path.join(path, file_stem + '_L.png'))
        pygame.image.save(self._last_img_right, os.path.join(path, file_stem + '_R.png'))

    @property
    def last_img(self):
        """ Last image captured. """
        return self._last_img_left
    
    @property
    def last_img_pair(self):
        """ Last image pair captured. """
        return self._last_img_left, self._last_img_right
    
    def next_img_file(self, path):
        """ Checks for most recent image file and increments file index count. """
        files = os.listdir(path)
        if not files:
            return 'img0000'
        else:
            # plenty of other (better ways to do this, feel free to change and filter)
            files.sort(key=(lambda k:os.path.getmtime(os.path.join(path,k))), reverse=True)
            last_name = files[0]
            idx = str(int(last_name.replace('img', '').replace('.png','').replace('_L','').replace('_R','')) + 1).zfill(4)
            next_name = "img" + idx
            return next_name


