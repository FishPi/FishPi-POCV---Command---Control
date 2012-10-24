
#
# FishPi - An autonomous drop in the ocean
#
# Drive Controller
#  - provides interface for drive and steering control
#  - using a pwm driver over i2c

#
# Adafruit i2c library (and others) at https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git
#    - example at http://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/library-reference
# PWM controller using i2c to PCA9685 - http://www.nxp.com/documents/data_sheet/PCA9685.pdf
# MicroViper Marine10 - http://www.mtroniks.net/details1.asp/ProductID/185/MicroViper-marine10.htm
# Standard meduim model servo for heading

import time
from Adafruit_I2C import Adafruit_I2C
from Adafruit_PWM_Servo_Driver import PWM

class DriveController:
    """ Provides drive and heading control abstraction from eg PWM servo or ESC devices. """

    # TODO might need tuning or configuring
    #servoMin = 150  # Min pulse length out of 4096
    #servoMax = 600  # Max pulse length out of 4096
    
    # initially setting to full left / right (of servo) to +/- Pi/2
    FULL_LEFT_SERVO = -1.570796
    FULL_RIGHT_SERVO = 1.570796

    # initially setting to full left / right (of allowed movement) to +/- Pi/4
    FULL_LEFT_ALLOWED = -0.785398
    FULL_RIGHT_ALLOWED = 0.785398

    # 'standard' analog servo freq
    ic_pwm_freq = 60

    def __init__(self, i2c_addr=0x40, i2c_bus=None, prop_channel=0, servo_channel=1, debug=False):
        self.debug = debug
        self.prop_channel = prop_channel
        self.servo_channel = servo_channel
        # Initialise the PWM device
        self._pwm = PWM(i2c_addr, i2c_bus=i2c_bus, debug=debug)
        self._pwm.setPWMFreq(self.ic_pwm_freq)
        # Set initial positions to centre
        self.set_servo_pulse(self.prop_channel, 1.5)
        self.set_servo_pulse(self.servo_channel, 1.5)

    def set_throttle(self, throttle_level):
        """ Set drive throttle between -1.0 and 1.0 with 0.0 for zero drive. """
        # TODO check break vs reverse state by storing last set level
        if throttle_level > 1.0 or throttle_level < -1.0:
            raise ValueError("throttle_level %f must be between -1.0 and 1.0." % throttle_level)
        # map input from (-1)..(0)..(1) to (1.0)..(1.5)..(2.0)
        pulse_time = (throttle_level/2.0)+1.5
        if (self.debug):
            print "Setting pulse length to: %f for throttle level %f" % (pulse_time, throttle_level)
        # set PWM pulse length
        self.set_servo_pulse(self.prop_channel, pulse_time)

    def set_heading(self, heading):
        """ Set heading to angle between FULL_LEFT and FULL_RIGHT.
            Input expected as between (-Pi/2) and (Pi/2) and is in radians.
            Negative heading is to port (left) and positive to starboard (right).
        """
        # TODO represents Servo angle not rudder angle - check translation
        # if incoming heading is outside allowable rotation, set to max allowable (eg physical turn of rudder)
        if heading > self.FULL_RIGHT_ALLOWED:
            heading = self.FULL_RIGHT_ALLOWED
        elif heading < self.FULL_LEFT_ALLOWED:
            heading = self.FULL_LEFT_ALLOWED
        # set proportion of desired turn out of full range of servo movement
        # ie if servo can move through -90 to 90 but rudder restricted to -60 to 60 then full left will be -2/3
        # ie a pulse length of 1.33 ms and full right will be 2/3 ie a pulse length of 1.67 ms.
        full_range = self.FULL_RIGHT_SERVO - self.FULL_LEFT_SERVO   # Pi
        pulse_time = (heading/full_range)+1.5
        if (self.debug):
            print "Setting pulse length to :%f for heading %f" % (pulse_time, heading)
        # set PWM pulse length
        self.set_servo_pulse(self.servo_channel, pulse_time)

    def halt(self):
        """ Halt the drive. """
        # TODO check if ESC feedback and can detect current state.
        # TODO check current motor direction and brake to zero.
        # for now, just set to zero output
        self.set_throttle(0.0)

    def set_servo_pulse(self, channel, pulse):
        """ 0.001 is ~1ms pulse so standard servo would be in range 1ms <- 1.5ms -> 2/0ms """
        pulseLength = 1000000                   # 1,000,000 us per second
        pulseLength /= self.ic_pwm_freq         # 60 Hz
        if (self.debug):
            print "%d us per period" % pulseLength
        pulseLength /= 4096                     # 12 bits of resolution
        if (self.debug):
            print "%d us per bit" % pulseLength
        pulse *= 1000
        pulse /= pulseLength
        if (self.debug):
            print "%d pulse sent" % pulse
        self._pwm.setPWM(channel, 0, int(pulse))

