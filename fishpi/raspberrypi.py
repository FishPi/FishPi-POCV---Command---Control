
#
# FishPi - An autonomous drop in the ocean
#
# Simple helper for the Raspberry Pi
#

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

def i2c_bus():
	ver = board_ver()
	if int(ver) > 4:
		return smbus.SMBus(1)
	else:
		return smbus.SMBus(0)

def serial_bus():
	return "/dev/ttyAMA0"

