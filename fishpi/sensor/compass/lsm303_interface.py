# Wrapper module for the LSM303 library by Adafruit
#
# This sensor interface uses the I2C2 bus on the BeagleBone Black.
# Internally this is mapped to i2c-1 (hence the busnum=-1).
# In order for this to work the device overlay for the I2C2 bus has to be
# exported. Because the internal mapping to i2c-1 the overlay is called BB-I2C1
# (not confusing at all, right?). So to export it type (as root):
# echo BB-I2C1 > /sys/devices/bone_capemgr.9/slots
# if this does not work, the 9 after the bone_capemgr. might be an 8 or
# some other digit.


from Adafruit_LSM303 import Adafruit_LSM303
import logging


class LSM303(object):
    def __init__(self):
        self._setup_complete = False
        self.device_handler = None

    def setup(self, busnum=-1, debug=False, hires=False):
        if self._setup_complete:
            return
        self.device_handler = Adafruit_LSM303(debug=debug)
        self._setup_complete = True

    def read_sensor(self):
        return self.device_handler.read()

# Global instance of sensor class:
sensor = LSM303()


class Magnetometer(object):

    def __init__(self, busnum=-1, debug=False, hires=False):
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        sensor.setup(busnum=busnum, debug=debug, hires=hires)

    def tear_down(self):
        logging.info("Magnetometer Interface:\tTear-down complete, " +
                "nothing to be done.")

    def read_sensor(self):
        # Split and return only compass data
        return sensor.read()[3:]


class Accelerometer(object):

    def __init__(self, busnum=-1, debug=False, hires=False):
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        sensor.setup(busnum=busnum, debug=debug, hires=hires)

    def tear_down(self):
        logging.info("Accelerometer Interface:\tTear-down complete, " +
                "nothing to be done.")

    def read_sensor(self):
        return sensor.read()[:3]

if __name__ == "__main__":
    from time import sleep
    print("This is the magnetometer and accelerometer data handler.")
    magn_handler = Magnetometer()
    while True:
        print magn_handler.read_sensor()
        sleep(0.5)
