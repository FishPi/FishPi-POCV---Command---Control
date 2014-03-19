# Wrapper module for the L3GD20 library
#
# This sensor interface uses the I2C2 bus on the BeagleBone Black. Internally this is mapped to i2c-1 (hence the busnum=-1).
# In order for this to work the device overlay for the I2C2 bus has to be exported. Because the internal mapping to i2c-1
# the overlay is called BB-I2C1 (not confusing at all, right?). So to export it type (as root):
# echo BB-I2C1 > /sys/devices/bone_capemgr.9/slots
# if this does not work, the 9 after the bone_capemgr. might be an 8 or some other digit.

from L3GD20 import L3GD20
from L3GD20 import L3GD20_range
import logging

class ConnectionError(Exception):
    '''Exception class indicating that an occured while connection to the remote device'''
    pass

class Gyroscope(object):
    
    def __init__(self, busnum=-1, debug=False, rng=L3GD20_range.R250DPS):
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        self.gyro_handler = L3GD20(busnum=busnum, debug=debug, rng=rng)
    
    def tear_down(self):
        logging.info("Gyroscope Interface:\tTear-down complete, nothing to be done.")
    
    def read_sensor(self):
        data = self.gyro_handler.read()
        return data
    


if __name__ == "__main__":
    from time import sleep
    print("This is the gyroscope data handler.")
    gyro_handler = Gyroscope()
    while True:
        print gyro_handler.read_sensor()
        sleep(0.5)
