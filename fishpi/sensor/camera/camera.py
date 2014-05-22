
#
# FishPi - An autonomous drop in the ocean
#
#
# PiCameraController - Provides access to the
# RaspberryPi cam via the PiCamera lib.
#
# Current State:
# - Can continously take pictures and send them over a network
#
# Future Features:
# - Is configured like any other sensor
# - Can take pictures on demand (capture())
# - Can take continously take pictures (with adjustable interval)
# - Can capture video and stream it via MJPEG (with adjustable quality)
# - Both images and video can be send somewhere and/or saved to memory


from __future__ import with_statement
import io
import logging
import picamera
import socket
import struct
import time
import threading


class CameraConfigError(Exception):
    pass


class CameraController(object):
    _cam_thread = None


    def __init__(self, interface="", hw_interface=None, debug=False, server='0.0.0.0', port='8000', initial_mode=None):
        self.server = server
        self.port = int(port)
        self.debug = debug
        self.configure(initial_mode)

    def set_mode(self, camera_cmd):
        """ External command interface. More commands to be added later """
        logging.info("CAM:\tReceived command %s" % camera_cmd)
        if camera_cmd == "start_image_capture":
            self.start_image_capture()
        elif camera_cmd == "stop_image_capture":
            self.stop_image_capture()

    def configure(self, initial_mode):
        logging.info("CAM:\tConfiguring PiCamera")

        # self.lock = threading.Lock()
        self._cam_thread = CameraThread(self.server, self.port)
        self._cam_thread.daemon = True
        self._cam_thread.start()
        if initial_mode is not None:
            self.set_mode(initial_mode)

    def clean_up(self):
        logging.info("CAM:\tCleaning up")
        if self._cam_thread is None:
            logging.error("CAM:\tNot configured correctly")
            return
        self._cam_thread.stop = True
        self._cam_thread.join()

    def capture_now(self):
        """ Captures a picture with the current configuration
            and sends it out """

    def start_video_capture(self):
        """ Starts the video capture with the current configuration """
        pass

    def stop_video_capture(self):
        """ Stops a running video capture """
        pass

    def start_image_capture(self):
        """ Starts continous image capture with the current configuration """
        logging.info("CAM:\tStarting image capture")
        if self._cam_thread is None:
            logging.error("CAM:\tNot configured correctly")
            return
        if not self._cam_thread.is_alive():
            self._cam_thread.start()
        self._cam_thread.stop = False

    def stop_image_capture(self):
        """ Stops a running continous image captureing """
        logging.info("CAM:\tStopping image capture")
        if self._cam_thread is None:
            logging.error("CAM:\tNot configured correctly")
            return
        self._cam_thread.stop = True


class CameraThread(threading.Thread):

    def __init__(self, server_address, server_port):
        threading.Thread.__init__(self)
        self.ip = server_address
        self.port = server_port
        self.stop = True

    def run(self):
        logging.info("CAM:\tCamera thread running")
        server_socket = socket.socket()
        server_socket.bind((self.ip, self.port))
        server_socket.listen(0)
        # Accept a single connection and make a file-like object out of it
        connection = server_socket.accept()[0].makefile('rb')

        while self.stop:
            time.sleep(1)

        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (640, 480)
                # Start a preview and let the camera warm up for 2 seconds
                camera.start_preview()
                time.sleep(2)
                stream = io.BytesIO()
                for foo in camera.capture_continuous(stream, 'jpeg'):
                    # Write the length of the capture to the stream and flush to
                    # ensure it actually gets sent
                    connection.write(struct.pack('<L', stream.tell()))
                    connection.flush()
                    # Rewind the stream and send the image data over the wire
                    stream.seek(0)
                    connection.write(stream.read())
                    # When stop is set, get out.
                    if self.stop:
                        break
                    # Reset the stream for the next capture
                    stream.seek(0)
                    stream.truncate()
            # Write a length of zero to the stream to signal we're done
            connection.write(struct.pack('<L', 0))
        finally:
            connection.close()
            server_socket.close()
