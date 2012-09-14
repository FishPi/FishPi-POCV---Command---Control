
#
# FishPi - An autonomous drop in the ocean
#
# Configuration for:
#  - loading i2c devices and driver code
#  - user directory for input / output files eg images and maps
#

#
# Adafruit i2c library (and others) at https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git
#

import logging

import os
import platform
import subprocess

#from Adafruit_I2C import Adafruit_I2C

class FishPiConfig(object):
    """ Responsible for configuration of FishPi. 
        Reads offline configuration files centrally.
        Scans and detects connected devices and provides driver classes.
        Provides common file location paths (for consistency).
    """
    
    _devices = []
    _root_dir = "/home/pi/fishpi/"

    def __init__(self):
        if os.path.exists(self.config_file):
            # TODO read any static config from file
            pass
        # create directories
        if not os.path.exists(self._root_dir):
            os.makedirs(self._root_dir)
        if not os.path.exists(self.navigation_data_path):
            os.makedirs(self.navigation_data_path)
        if not os.path.exists(self.imgs_path):
            os.makedirs(self.imgs_path)
        if not os.path.exists(self.logs_path):
            os.makedirs(self.logs_path)

        # TODO any other init
        # TODO setup logging (from Main)
        pass
    
    #
    # file / paths section
    #
    
    @property
    def config_file(self):
        return self._root_dir + ".fishpi_config"
    
    @property
    def navigation_data_path(self):
        return self._root_dir + "navigation"
    
    @property
    def imgs_path(self):
        return self._root_dir + "imgs"
    
    @property
    def logs_path(self):
        return self._root_dir + "logs"

    #
    # device configuration section
    #
 
    @property
    def devices(self):
        """ Attached devices. """
        return self._devices

    def configure_devices(self):
        """ Configures i2c devices when running in appropriate environment. """
        # TEMP only run i2c scan on Linux, logs errors
        if platform.system() == "Linux":
            try:
                logging.info("Configuring i2c devices...")
                # scan for connected devices
                i2c_addresses = self.scan_i2c()

                # lookup available device drivers by address
                for addr, in_use in i2c_addresses:
                    device_name, device_driver = self.lookup(addr)
                    self._devices.append([addr, device_name, device_driver, in_use])
            except Exception as ex:
                logging.exception("Error scanning i2c devices!")
        else:
            logging.info("Not running on Linux distro. Not configuring i2c devices.")
        
        # TODO add non i2c device detection eg webcams on /dev/video*, provide driver classes

    def lookup(self, addr):
        """ lookup available device drivers by hex address. """
        # note: i2c addresses can conflict
        # could scan registers etc to confirm count etc?

        # TODO replace with reading from config
        # probably use ConfigParser
        if addr == 0x68:
            return "DS1307", "DS1307.py"
        elif addr == 0x20:
            return "GPS", "NavigtronGPS.py"
        elif addr == 0x48:
            return "TMP102", "TMP102.py"
        elif addr == 0x60:
            return "CMPS10", "CMPS10.py"
        elif addr == 0x40 or addr == 0x70:
            return "PCA9685", "Adafruit_PWM_Servo_Driver.py"
        elif addr == 0x1E:
            return "HMC5883L", "HMC5883L.py"
        elif addr == 0x53 or addr == 0x1D:
            # 0x53 when ALT connected to HIGH
            # 0x1D when ALT connected to LOW
            return "ADXL345", "ADXL345.py"
        elif addr == 0x69:
            # 0x68 when AD0 connected to LOW - conflicts with DS1307!
            # 0x69 when AD0 connected to HIGH
            return "ITG3200", "ITG3200.py"
        else:
            return "unknown", ""

    def scan_i2c(self):
        """scans i2c port returning a list of detected addresses.
            Requires sudo access.
            Returns True for in use by a device already (ie UU observed)"""
        
        proc = subprocess.Popen(['sudo', 'i2cdetect', '-y', '0'], 
                stdout = subprocess.PIPE,
                close_fds = True)
        std_out_txt, std_err_txt = proc.communicate()

        # TODO could probably be neater with eg format or regex
        # i2c returns
        #  -- for unused addresses
        #  UU for addresses n use by a device
        #  0x03 to 0x77 for detected addresses
        # need to keep columns if care about UU devices
        addr = []
        lines = std_out_txt.rstrip().split("\n")
        
        if lines[0] in "command not found":
            raise RuntimeError("i2cdetect not found")
        
        for i in range(0,8):
            for j in range(0,16):
                idx_i = i+1
                idx_j = j*3+4
                cell = lines[idx_i][idx_j:idx_j+2].strip()
                if cell and cell != "--":
                    logging.info("    ...device at:", hex(16*i+j), cell)
                    hexAddr = 16*i+j
                    if cell == "UU":
                        addr.append([hexAddr, True])
                    else:
                        addr.append([hexAddr, False])
        
        return addr


