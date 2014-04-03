
#
# FishPi - An autonomous drop in the ocean
#
# Simple helper for the Raspberry Pi
#

import os
import smbus
import subprocess

def board_ver():
    proc = subprocess.Popen(['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE, close_fds=True)
    out, err = proc.communicate()
    lines = filter(None, out.split('\n'))
    results = {}
    for line in lines:
        k, v = line.strip().split(':')
        results[k.strip()] = v.strip()
    return results['Revision']

def i2c_bus(bus=""):
    ver = board_ver()
    if int(ver) > 4:
        return smbus.SMBus(1)
    else:
        return smbus.SMBus(0)

def i2c_bus_num():
    ver = board_ver()
    if int(ver) > 4:
        return '1'
    else:
        return '0'

def serial_bus(bus=""):
    return "/dev/ttyUSB0"
    #return "/dev/ttyAMA0"

