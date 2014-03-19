#!/usr/bin/python

# Python library for L3GD20 Gyro Sensor.
# This is a pretty direct port from the Adafruit library for Arduino, except for 
# that it only supports I2C and not SPI.
# It uses the Adafruit libraries for I2C and should work for both Raspberry Pi
# and BeagleBone. 

# Copyright for the Python library 2014 by Sven Chmielewski and the ASPilot Project.
# Copyright for the Adafruit libraries used here and the original L3GD20 library 
# for Arduino by Adafruit Industries.

# This file is part of the ASPilot Project.

from Adafruit_I2C import Adafruit_I2C
import logging


class L3GD20_range(object):
	R250DPS = 1
	R500DPS = 2
	R2000DPS = 3


class L3GD20(Adafruit_I2C):
	
	L3GD20_ADDRESS 		= 0x6B	# 1101011
	L3GD20_POLL_TIMEOUT = 100	# Maximum number of read attempts
	L3GD20_ID			= 0b11010100
	
	L3GD20_SENSITIVITY_250DPS 	= 0.00875	# Roughly 22/256 for fixed point match
	L3GD20_SENSITIVITY_500DPS 	= 0.0175	# Roughly 45/256
	L3GD20_SENSITIVITY_2000DPS 	= 0.070		# Roughly 18/256
	
	L3GD20_DPS_TO_RADS = 0.017453293		# degress/s to rad/s multiplier
	
	# Registers on the chip. Some might be unused.
	L3GD20_REGISTER_WHO_AM_I            = 0x0F   # 11010100   r
	L3GD20_REGISTER_CTRL_REG1           = 0x20   # 00000111   rw
	L3GD20_REGISTER_CTRL_REG2           = 0x21   # 00000000   rw
	L3GD20_REGISTER_CTRL_REG3           = 0x22   # 00000000   rw
	L3GD20_REGISTER_CTRL_REG4           = 0x23   # 00000000   rw
	L3GD20_REGISTER_CTRL_REG5           = 0x24   # 00000000   rw
	L3GD20_REGISTER_REFERENCE           = 0x25   # 00000000   rw
	L3GD20_REGISTER_OUT_TEMP            = 0x26   #            r
	L3GD20_REGISTER_STATUS_REG          = 0x27   #            r
	L3GD20_REGISTER_OUT_X_L             = 0x28   #            r
	L3GD20_REGISTER_OUT_X_H             = 0x29   #            r
	L3GD20_REGISTER_OUT_Y_L             = 0x2A   #            r
	L3GD20_REGISTER_OUT_Y_H             = 0x2B   #            r
	L3GD20_REGISTER_OUT_Z_L             = 0x2C   #            r
	L3GD20_REGISTER_OUT_Z_H             = 0x2D   #            r
	L3GD20_REGISTER_FIFO_CTRL_REG       = 0x2E   # 00000000   rw
	L3GD20_REGISTER_FIFO_SRC_REG        = 0x2F   #            r
	L3GD20_REGISTER_INT1_CFG            = 0x30   # 00000000   rw
	L3GD20_REGISTER_INT1_SRC            = 0x31   #            r
	L3GD20_REGISTER_TSH_XH              = 0x32   # 00000000   rw
	L3GD20_REGISTER_TSH_XL              = 0x33   # 00000000   rw
	L3GD20_REGISTER_TSH_YH              = 0x34   # 00000000   rw
	L3GD20_REGISTER_TSH_YL              = 0x35   # 00000000   rw
	L3GD20_REGISTER_TSH_ZH              = 0x36   # 00000000   rw
	L3GD20_REGISTER_TSH_ZL              = 0x37   # 00000000   rw
	L3GD20_REGISTER_INT1_DURATION       = 0x38    # 00000000   rw
	
	
	def __init__(self, busnum=-1, debug=False, rng=L3GD20_range.R250DPS):
		
		# Adjust logging to debug setting
		if debug:
			logging.basicConfig(level=logging.DEBUG)
		
		logging.info("L3GD20 Interface:\tConnecting to device")
		
		# Invoke I2C instance
		self.gyro = Adafruit_I2C(self.L3GD20_ADDRESS, busnum, debug)
		
		if self.gyro.readU8(self.L3GD20_REGISTER_WHO_AM_I) != self.L3GD20_ID:
			logging.error("L3GD20 Interface:\tWrong device ID")
			return None
			# Maybe raise exception here
		
		#  Switch to normal mode and enable all three channels
		self.gyro.write8(self.L3GD20_REGISTER_CTRL_REG1, 0x0F)
		
		# Adjust resolution
		if rng == L3GD20_range.R250DPS:
			self.gyro.write8(self.L3GD20_REGISTER_CTRL_REG4, 0x00)
			self.sensitivity = self.L3GD20_SENSITIVITY_250DPS
		elif rng == L3GD20_range.R500DPS:
			self.gyro.write8(self.L3GD20_REGISTER_CTRL_REG4, 0x10)
			self.sensitivity = self.L3GD20_SENSITIVITY_500DPS
		elif rng == L3GD20_range.R2000DPS:
			self.gyro.write8(self.L3GD20_REGISTER_CTRL_REG4, 0x20)
			self.sensitivity = self.L3GD20_SENSITIVITY_2000DPS
	
	def gyro16(self, list, idx):
		'''Interpret 16-bit gyroscope component from list'''
		n = list[idx] | (list[idx+1] << 8)		# shift high (second) byte
		return n if n < 32768 else n - 65536	# 2's complement signed
	
	
	def read(self):
		
		# Read gyro values
		list = self.gyro.readList(self.L3GD20_REGISTER_OUT_X_L | 0x80, 6)
		res = [(self.gyro16(list, 0)*self.sensitivity,
				self.gyro16(list, 2)*self.sensitivity,
				self.gyro16(list, 4)*self.sensitivity )]
				
		return res

		
# Simple example
if __name__ == "__main__":
	
	from time import sleep
	
	l3 = L3GD20()
	print("This is the L3GD20 Gyroscope interface.\nOutput format: [Gyroscope X, Y, Z]")
	while True:
		print l3.read()
		sleep(1)
		
		
		
		
