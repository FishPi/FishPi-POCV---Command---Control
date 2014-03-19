# ASPilot GPSD Interface Library
#
# This file is part of the ASPilot project
#
# TODO: -Implement formatting
#       -Write unit and functional tests for interface

import Adafruit_BBIO.UART as UART
import gps
import serial
from subprocess import call
import logging


class GPSDError(Exception):
	"""Exception indicating that an error occured while working with GPSD"""
	pass


class gpsdInterface():
	# constants and stuff here
	uart_tty_map = {"UART1": "/dev/ttyO1", 'UART2': "/dev/ttyO2", "UART4": "/dev/ttyO4", "UART5": "/dev/ttyO5"}
	
	def __init__(self, uart="UART4", debug=False):
		if debug:
			logging.basicConfig(level=logging.DEBUG)
		self.debug = debug
		self.uart = uart		# not really useful right now, might be once the cleanup() method works
		
		# Map UART to ttyO interface
		if not self.uart in self.uart_tty_map:
			logging.error("GPSD Interface:\tThe serial interface %s is not supported.", uart)
			return 1		# TODO: Specify error codes to allow more detailed error description or raise descriptive exception here
		self.tty = self.uart_tty_map[self.uart]
		
		UART.setup(uart)
		self.ser = serial.Serial(port=self.tty, baudrate=9600)
		self.ser.close()
		self.ser.open()
		if self.ser.isOpen():
			call(["gpsd", self.tty])
			self.session = gps.gps(mode=gps.WATCH_ENABLE)
			logging.info("GPSD Interface:\tInitialization complete.")
		else:
			logging.error("GPSD Interface:\tCould not open serial port.")
			return 1
	
	def tear_down(self):
		self.session.close()
		call(["killall", "gpsd"])
		self.ser.close()
		# UART.cleanup(uart)	# not functional right now according to Adafruit
		logging.info("GPSD Interface:\tTear-down complete.")
		return 0
	
	def read_raw_gpsd_data(self):
		'''Read the newest data from gpsd and return it'''
		try:
			#if self.session.waiting():
			report = self.session.next()
			return report
			#else:
			#	return None
		except StopIteration:
			raise GPSDError()
	
	def read(self):
		'''Read the newest data from gpsd and return a formatted version. Not active right now.'''
		return self.read_raw_gpsd_data()


if __name__ == "__main__":
	from time import sleep
	gps_handler = gpsdInterface(debug=True)
	print 'ASPilot gpsd Interface Example'
	while True:
		print gps_handler.read_raw_gpsd_data()
		sleep(1)
