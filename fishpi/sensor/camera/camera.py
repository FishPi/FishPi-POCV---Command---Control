
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
import os
import socket
import struct
import time
import threading


class CameraController(object):
    _cam_thread = None
    modes = ['stop', 'single', 'continuous', 'video', 'demo']

    def __init__(self, interface="", hw_interface=None, debug=False, server='0.0.0.0', port='8001', initial_mode=None):
        self.server = server
        self.port = int(port)
        self.debug = debug
        self.set_up(initial_mode)
        self.enabled = True  # what's this for? The Kernel wants it, but why?

    def set_up(self, initial_mode):
        """ Create and start the camera thread """
        logging.info("CAM:\tSetting up PiCamera")

        self._cam_thread = CameraThread(self.server, self.port)
        self._cam_thread.daemon = True
        self._cam_thread.start()
        if initial_mode is not None:
            self.set_mode(initial_mode)

    def tear_down(self):
        """ Stop and destroy the camera thread """
        logging.info("CAM:\tCleaning up")
        if self._cam_thread is None:
            logging.error("CAM:\tNot configured correctly")
            return
        self._cam_thread.mode = 'stop'  # deactivate capturing
        self._cam_thread.stop = True    # stop thread
        self._cam_thread.join()

    def set_mode(self, camera_cmd):
        """ External command interface. More commands to be added later """
        logging.info("CAM:\tReceived command %s" % camera_cmd)
        # If the thread is dead, restart it
        if self._cam_thread is None or not self._cam_thread.is_alive():
            logging.error("CAM:\tCamera thread is dead. Restarting..")
            self.tear_down()
            self.set_up('stop')
        if camera_cmd not in self.modes:
            logging.error("CAM:\tIllegal mode %s received. Ignoring." %
                camera_cmd)
            return
        self._cam_thread.mode = camera_cmd

    def capture_now(self):
        """ Captures a picture with the current configuration
            and sends it out """
        pass


class CameraThread(threading.Thread):

    def __init__(self, server_address, server_port):
        threading.Thread.__init__(self)
        self.ip = server_address
        self.port = server_port
        self.stop = False
        self.demo_lock = False  # set to true to lock mode variable
        self.mode = 'stop'

    def run(self):
        """ The thread's run method. There are three possible modes:
            single capture: The thread sleeps and waits for a command to take a
                            single picture.
            continous capture: The thread continously takes pictures.
            video capture: The thread captures a video stream.
            A fourth mode could be sending a test picture. """

        # try to import picamera, if it fails, lock to demo mode
        try:
            import picamera
        except ImportError:
            logging.error("CAM:\tFailed to import picamera module. " +
                "Running demo mode..")
            self.demo_lock = True

        logging.info("CAM:\tCamera thread running")
        server_socket = socket.socket()
        server_socket.bind((self.ip, self.port))
        server_socket.listen(0)
        # Accept a single connection and make a file-like object out of it
        connection = server_socket.accept()[0].makefile('rb')

        try:
            while not self.stop:
                # Make sure mode if 'demo' if lock is set
                if self.demo_lock is True:
                    self.mode = 'demo'

                if self.mode == 'stop':
                    time.sleep(1)
                elif self.mode == 'demo':
                    logging.debug("CAM:\tRunning demo mode...")
                    self._demo_mode(connection)
                elif self.mode == 'continous':
                    self._capture_continuous(connection)
                elif self.mode == 'video':
                    self._capture_video(connection)
                elif self.mode == 'single':
                    self._capture_single(connection)
                else:
                    pass
                    # Here be dragons
        finally:
            connection.close()
            server_socket.close()

    def _capture_continuous(self, connection):
        """ Continously capture pictures and send them """
        logging.info("CAM:\tStarting image capture")
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            # Start a preview and let the camera warm up for 2 seconds
            camera.start_preview()
            time.sleep(2)
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg'):
                # When mode is not continuous, get out.
                if self.mode != 'continuous':
                    break
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                connection.write(stream.read())
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
            # Write a length of zero to the stream to signal we're done
            connection.write(struct.pack('<L', 0))
        logging.info("CAM:\tStopping image capture")

    def _capture_single(self, connection):
        """ Take a single picture and send it.
            Can take up to a second to respond """
        pass

    def _capture_video(self, connection):
        """ Capture a video stream and send it """
        pass

    def _demo_mode(self, connection):
        """ Continuously broadcast a demo image """
        os.abspath(__name__)
        stream = io.open(os.path.dirname(os.path.abspath(__file__)) +
            'test.bmp', 'rb')
        stream.seek(0, 2)

        while self.mode == 'demo':
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            stream.seek(0, 2)
        # Write a length of zero to the stream to signal that we're done
        connection.write(struct.pack('<L', 0))
