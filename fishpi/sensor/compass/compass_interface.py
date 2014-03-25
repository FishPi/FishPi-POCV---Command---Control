#
# FishPi - An autonomous drop in the ocean
#
# Tilt-compensated Compass driver for the LSM303

import logging
from math import atan2, sqrt, sin, cos, pi
from math import pow as fpow

from Adafruit_LSM303 import Adafruit_LSM303


class Compass(object):

    def __init__(self, busnum=-1, debug=False, hires=False):
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        self.device_handler = Adafruit_LSM303(debug=debug)

    def tear_down(self):
        logging.info("Compass Interface:\tTear-down complete, " +
                "nothing to be done.")

    def read_sensor(self):
        # Split and return only compass data
        data = self.device_handler.read()



        ((x_a, y_a, z_a), (x_m, y_m, z_m, or_)) = data

        # Calculate roll and pitch in radians
        pitch_r = atan2(x_a, sqrt(fpow(y_a, 2) + fpow(z_a, 2)))
        roll_r = atan2(y_a, z_a)

        x_h = x_a * cos(pitch_r) + z_m * sin(pitch_r)
        y_h = ((x_m * sin(roll_r) * sin(pitch_r)) + (y_m * cos(roll_r)) -
            (z_m * sin(roll_r) * cos(pitch_r)))
        heading = atan2(y_h, x_h)

        pitch = pitch_r * 180 / pi
        roll = roll_r * 180 / pi

        return heading, pitch, roll


if __name__ == "__main__":
    print("This is the tilt-compensated compass data handler.")
    from time import sleep
    compass = Compass()
    while True:
        heading, pitch, roll = compass.read_sensor()
        print("Heading: %f, Pitch: %f, Roll: %f" % heading, pitch, roll)
        sleep(0.5)


