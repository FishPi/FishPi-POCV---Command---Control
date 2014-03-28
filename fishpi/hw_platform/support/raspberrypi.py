#
# FishPi - An autonomous drop in the ocean
#
# Support Code for RaspberryPi

import subprocess

import hw_platform.hw_config as hw_config


class RaspberryPiSupport(object):
    """ Support package for RaspBerry Pi """

    def __init__(self):
        hw_config.platform = 'RPi'

    def configure_interface(self, name):
        pass

    def board_ver(self):
        proc = subprocess.Popen(['cat', '/proc/cpuinfo'],
            stdout=subprocess.PIPE, close_fds=True)
        out, err = proc.communicate()
        lines = filter(None, out.split('\n'))
        results = {}
        for line in lines:
            k, v = line.strip().split(':')
            results[k.strip()] = v.strip()
        return results['Revision']

    def lookup_interface(self, bus=""):
        if bus == "I2C":
            ver = self.board_ver()
            if int(ver) > 4:
                return 1
            else:
                return 0
        elif bus == "UART":
            return "/dev/ttyUSB0"
            #return "/dev/ttyAMA0"

    def i2c_bus_num(self):
        ver = self.board_ver()
        if int(ver) > 4:
            return '1'
        else:
            return '0'
