
#
# FishPi - An autonomous drop in the ocean
#
# Temperature Sensor using Tmp102 TI chip over I2C
#

#
# Adafruit i2c library (and others) at https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git

# from Adafruit_I2C import Adafruit_I2C
from Adafruit_I2C import Adafruit_I2C

class TemperatureSensor:
    """ Temperature Sensor using Tmp102 TI chip over I2C """

    def __init__(self, address=0x48, interface="", hw_interface="-1", debug=False):
        if hw_interface is None:
            self.i2c = Adafruit_I2C(address, debug=debug)
        else:
            self.i2c = Adafruit_I2C(address, busnum=int(hw_interface), debug=debug)
        self.address = address
        self.debug = debug

    def read_sensor(self):
        """ Read sensor values. """
        # set mode to read sensor
        self.i2c.write8(0x00, 1)
        # read 2 registers
        result = self.i2c.readList(0x00, 2)
        # convert to something useful... 
        return self._convert_12b_split(result[0], result[1])

    def _convert_12b_split(self, msb, lsb):
        value = (msb<<4) | (lsb>>4)
        return self._convert_12b(value)

    def _convert_12b(self, value_in):
        """ Converts a 12 bit value from binary to degrees centigrade.
            Resolution for ADC from tmp102 is 0.0625 C per count.
            Negative numbers in twos complement with msb=1.
        """
        if ((value_in & (1<<11)) >> 11):
            return float(int('0b'+''.join('1' if c == '0' else '0' for c in bin(value_in-1).lstrip('-0b')),2)) * -0.0625
        else:
            return float(value_in) * 0.0625

