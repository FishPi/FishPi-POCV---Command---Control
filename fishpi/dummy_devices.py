#
# FishPi - An autonomous drop in the ocean
#

import os
import logging


class DummyCameraController(object):
    """ 'Dummy' camera controller that just logs. """

    def __init__(self, resources_folder):
        self.enabled = False
        from PIL import Image
        temp_image_path = os.path.join(resources_folder, 'camera.jpg')
        self._last_img = Image.open(temp_image_path)

    def capture_now(self):
        if self.enabled:
            logging.debug("CAM:\tCapture image.")
        pass

    @property
    def last_img(self):
        return self._last_img


class DummyDriveController(object):
    """ 'Dummy' drive controller that just logs. """

    # current state
    throttle_level = 0.0
    steering_angle = 0.0

    def __init__(self):
        pass

    def set_throttle(self, throttle_level):
        logging.debug("DRIVE:\tThrottle set to: %s" % throttle_level)
        self.throttle_level = throttle_level
        pass

    def set_steering(self, angle):
        logging.debug("DRIVE:\tSteering set to: %s" % angle)
        self.steering_angle = angle
        pass

    def halt(self):
        logging.debug("DRIVE:\tDrive halting.")
        self.throttle_level = 0.0
        self.steering_angle = 0.0
        pass


class DummyCompassSensor(object):
    """ 'Dummy' compass sensor that outputs a static heading value. """

    def __init__(self, interface="", hw_interface="-1", debug=False,
            heading=0.0, pitch=0.0, roll=0.0):
        self.debug = debug
        self.heading = heading
        self.pitch = pitch
        self.roll = roll

    def read_sensor(self):
        logging.debug("SENSOR:\tDUMMY_CMP:\tHeading %f, pitch %f, roll %f",
            self.heading, self.pitch, self.roll)
        return self.heading, self.pitch, self.roll


class DummyTemperatureSensor(object):
    """ 'Dummy' temperature sensor that outputs a static temperature value. """

    def __init__(self, interface="", hw_interface="-1", debug=False,
            temperature=0.0):
        self.debug = debug
        self.temperature = temperature

    def read_sensor(self):
        logging.debug("SENSOR:\tDUMMY_TEMP:\tTemperature: %f",
            self.temperature)
        return self.temperature
