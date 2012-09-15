
#
# FishPi - An autonomous drop in the ocean
#
# Drive Controller
#  - provides interface for drive and steering control
#

#
# Adafruit i2c library (and others) at https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git
#    - example at http://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/library-reference

import time
from Adafruit_I2C import Adafruit_I2C
from Adafruit_PWM_Servo_Driver import PWM

from FishPiConfig import FishPiConfig

class DriveController:
    
    servoMin = 150  # Min pulse length out of 4096
    servoMax = 600  # Max pulse length out of 4096
    
    prop_channel = 0
    servo_channel = 1

    def __init__(self, config):
        self._config = config
        # pick up i2c drivers for address
        
        # Initialise the PWM device using the default address
        # bmp = PWM(0x40, debug=True)
        pwm = PWM(0x40, debug=True)
        pwm.setPWMFreq(60)                        # Set frequency to 60 Hz


    def set_drive(self):
        pwm.setPWM(self.prop_channel, 0, servoMin)
        time.sleep(1)
        pwm.setPWM(self.prop_channel, 0, servoMax)
        time.sleep(1)

    def set_heading(self):
        pwm.setPWM(self.servo_channel, 0, servoMin)
        time.sleep(1)
        pwm.setPWM(self.servo_channel, 0, servoMax)
        time.sleep(1)

    def halt(self):
        pwm.setPWM(self.prop_channel, 0, servoMin)

    def setServoPulse(channel, pulse):
        pulseLength = 1000000                   # 1,000,000 us per second
        pulseLength /= 60                       # 60 Hz
        print "%d us per period" % pulseLength
        pulseLength /= 4096                     # 12 bits of resolution
        print "%d us per bit" % pulseLength
        pulse *= 1000
        pulse /= pulseLength
        pwm.setPWM(channel, 0, pulse)

