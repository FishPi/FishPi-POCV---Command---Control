#
# FishPi - An autonomous drop in the ocean
#
# TODO: -Enable for RaspberryPi as well. BBB-specific stuff from here should
#        go to the platform library

# how to make the fishpi directory available everywhere?
import hw_platform.hw_config as hw_config

if hw_config.platform == 'BBB':
   import Adafruit_BBIO.UART as UART

import gps
import serial
from subprocess import call
from time import sleep
import logging


class GPSDError(Exception):
    """Exception indicating that an error occured while working with GPSD"""
    pass


class gpsdInterface():
    # constants and stuff here
    bbb_uart_tty_map = {
        "UART1": "/dev/ttyO1",
        'UART2': "/dev/ttyO2",
        "UART4": "/dev/ttyO4",
        "UART5": "/dev/ttyO5",
        "default": "/dev/ttyO4"}

    rpi_uart_tty_map = {"default": "/dev/ttyAMA0"}

    def __init__(self, uart="default", debug=False):
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        self.debug = debug
        #self.uart = uart        # not really useful right now, might be once the cleanup() method works
        self.uart = "UART4"
        self.num_sat = 0

        # Map UART to ttyO interface
        if not self.uart in self.bbb_uart_tty_map:
            logging.error("GPSD Interface:\tThe serial interface %s " +
                "is not supported.", uart)
            return 1
        self.tty = self.bbb_uart_tty_map[self.uart]

        if hw_config.platform is None:
            logging.error("GPSD Interface:\tHardware platform is not " +
                "specified! Won't set up sensor.")
            return 1

        # Do setup for BeagleBone Black
        if hw_config.platform == 'BBB':
            if not self.setup_bbb():
                return 1
        # Do setup for RaspberryPi
        elif hw_config.platform == 'RPi':
            self.tty = self.rpi_uart_tty_map[self.uart]

        call(["gpsd", self.tty])
        self.session = gps.gps(mode=gps.WATCH_ENABLE)
        logging.info("GPSD Interface:\tInitialization complete.")

    def setup_bbb(self):
        # Ugly inline import right here! Booya.
        #import Adafruit_BBIO.UART as UART

        self.tty = self.bbb_uart_tty_map[self.uart]
        num_failed_tries = 0
        while not self.setup_bbb_uart():
            if num_failed_tries < 10:
                logging.error("GPSD Interface:\tCould not connect to " +
                    "serial interface. Trying again..")
                num_failed_tries += 1
            else:
                logging.error("GPSD Interface:\tFailed to connect to " +
                    "serial interface. Aborting.")
                return False
        return True

    def setup_bbb_uart(self):
        # Is this necessary if I don't want to use it myself??
        UART.setup(self.uart)
        self.ser = serial.Serial(port=self.tty, baudrate=9600)
        self.ser.close()
        self.ser.open()
        if self.ser.isOpen():
            return True
        else:
            return False

    def tear_down(self):
        self.session.close()
        call(["killall", "gpsd"])
        if hw_config.platform == 'BBB':
            self.ser.close()
        # UART.cleanup(uart)    # not functional right now according to Adafruit
        logging.info("GPSD Interface:\tTear-down complete.")
        return 0

    def read_raw_gpsd_data(self):
        """Read the newest data from gpsd and return it"""
        try:
            #if self.session.waiting():
            report = self.session.next()
            return report
            #else:
            #   return None
        except StopIteration:
            raise GPSDError()

    def read(self):
        """Read the newest data from gpsd and return a formatted version.
            Not active right now."""
        data = self.read_raw_gpsd_data()

        if data['class'] == 'TPV':
            if data['mode'] == 1:  # really a number, not a string?
                return (
                    1,      # fix
                    0.0,    # lat
                    0.0,    # lon
                    0.0,    # heading
                    0.0,    # speed
                    0.0,    # altitude
                    self.num_sat,  # num_sat
                    "",     # timestamp
                    "")     # datestamp
            else:
                return (
                    data['mode'],
                    data['lat'],
                    data['lon'],
                    data['track'],
                    data['speed'],
                    self.num_sat,
                    data['time'].split('T')[1],
                    data['time'].split('T')[2])
        elif data['class'] == 'SKY':
            if 'satellites' in data.keys():
                self.num_sat = len(data['satellites'])
            else:
                self.num_sat = 0


if __name__ == "__main__":
    from time import sleep
    gps_handler = gpsdInterface(debug=True)
    print 'ASPilot gpsd Interface Example'
    while True:
        print gps_handler.read_raw_gpsd_data()
        sleep(1)
