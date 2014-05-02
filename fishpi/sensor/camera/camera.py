
#
# FishPi - An autonomous drop in the ocean
#
#
# PiCameraController - Provides access to the
# RaspberryPi cam via the PiCamera lib.
#
# Features:
# - Is configured like any other sensor
# - Can take pictures on demand (capture())
# - Can take continously take pictures (with adjustable interval)
# - Can capture video and stream it via MJPEG (with adjustable quality)
# - Both images and video can be send somewhere and/or saved to memory

from __future__ import with_statement
import io
import logging
import picamera
import time
import threading


class CameraController(object):
    _cam_thread = None
    _stream = None

    def __init__(self, interface="", hw_interface=None, debug=False, **kwargs):
        self.configure(**kwargs)
        pass  # configuration?? what is that?

    @property
    def stream(self):
        return self._stream

    def configure(self, **kwargs):
        logging.info("CAM:\tConfiguring PiCamera")
        self._stream = io.BytesIO()
        self.lock = threading.Lock()
        self._cam_thread = CameraThread(self.lock, self._stream)
        # later thread's config could be called here with kwargs
        self._cam_thread.start()

    def clean_up(self):
        logging.info("CAM:\tCleaning up")
        self._cam_thread.join()

    def capture_now(self):
        """ Captures a picture with the current configuration
            and sends it out """
        if self._cam_thread is None:
            logging.error("CAM:\tNot configured correctly")
            return
        self.lock.aquire()
        self._cam_thread.take_single_image = True

    def start_video_capture(self):
        """ Starts the video capture with the current configuration """
        pass

    def stop_video_capture(self):
        """ Stops a running video capture """
        pass

    def start_image_capture(self):
        """ Starts continous image capture with the current configuration """
        pass

    def stop_image_capture(self):
        """ Stops a running continous image captureing """
        pass


class CameraThread(threading.Thread):
    take_single_image = False
    start_cont_image_capture = False
    stop_cont_image_capture = False
    start_video_capture = False
    stop_video_capture = False
    heating_up = False

    def __init__(self, lock, stream):
        threading.Thread.__init__(self)
        self.lock = lock
        self.stream = stream
        self.configure()

    def run(self):
        """ Check the state variables and take the appropriate actions """
        if self.stream is None:
            self.configure()
        self.lock.aquire()
        if self.take_single_image:
            with picamera.PiCamera() as camera:
                camera.start_preview()
                camera.capture(self.stream, 'jpeg')
            self.take_single_image = False
        self.lock.release()
        time.sleep(0.5)

    def configure(self, **kwargs):
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
