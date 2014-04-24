#
# FishPi - An autonomous drop in the ocean
#
# Support Code for BeagleBone Black

import os
import logging
import smbus

# This is to satisfy the driver includes. hope they work..
# import Adafruit.I2C.Adafruit_I2C as Adafruit_I2C

import hw_platform.hw_config as hw_config

# TODO: Detect if the path to the capemanager is 8 or 9 and configure the
#       variable accordingly


class BeagleBoneSupport(object):
    """ Support package for BeagleBone. Exports the overlays from the
        device tree for the used hardware """

    def __init__(self):
        # every support code has to set this to notify drivers on
        # which platform they are working.
        hw_config.platform = 'BBB'
        hw_config.default_ic2 = 'I2C2'

    def configure_interface(self, name):
        """ Export a specific overlay which is identified by name,
            such as "I2C2" or "UART4" """

        if name == "I2C2":
            os.system("echo BB-I2C1 > /sys/devices/bone_capemgr.9/slots")
            logging.info("BBB:\tExporting device overlay for I2C2...")
        elif name == "UART1":
            pass
        elif name == "UART2":
            pass
        elif name == "UART3":
            pass
        elif name == "UART4":
            os.system("echo BB-UART4 > /sys/devices/bone_capemgr.9/slots")
            logging.info("BBB:\tExporting device overlay for UART4...")

        # ... more devices here
        else:
            logging.error("BBB:\tInterface %s unknown.", name)
            return

        # It's basically just executing a shell command, that exports the
        # device. Each if/elif specifies a string that gets put into the exec
        # command that is issued at the end.

    # TODO: What's up with the different UART numbers here? 1,2,3,4 or 1,2,4,5?
    def lookup_interface(self, bus):
        if bus == "I2C2":
            return 1  # correct???
        elif bus == "UART1":
            return "/dev/ttyO1"
        elif bus == "UART2":
            return "/dev/ttyO2"
        elif bus == "UART4":
            return "/dev/ttyO4"
        elif bus == "UART5":
            return "/dev/ttyO5"
        else:
            return None
