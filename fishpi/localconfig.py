
#
# FishPi - An autonomous drop in the ocean
#
# Configuration for:
#  - loading i2c devices and other driver code
#  - user directory for input / output files eg images and maps
#

import logging
import logging.handlers

import os
import platform
import subprocess
import time

class FishPiConfig(object):
    """ Responsible for configuration of FishPi. 
        Reads offline configuration files centrally.
        Scans and detects connected devices and provides driver classes.
        Provides common file location paths (for consistency).
    """
    
    _devices = []
    _root_dir = os.path.join(os.getenv("HOME"), "fishpi")

    def __init__(self):
        # TODO setup logging (from config)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        console = logging.StreamHandler()
        logger.addHandler(console)
        
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

        # add file logging
        log_file_stem = os.path.join(self.logs_path, 'fishpi_%s.log' % time.strftime('%Y%m%d_%H%M%S'))
        handler = logging.handlers.RotatingFileHandler(log_file_stem, backupCount=50)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # can force new file start if needed
        #handler.doRollover()
        
        # default attachments to None
        self.gps_sensor = None
        self.compass_sensor = None
        self.temperature_sensor = None
        self.drive_controller = None
        self.camera_controller = None
        
        # TODO any other init
        pass
    
    #
    # file / paths section
    #
    
    @property
    def config_file(self):
        return os.path.join(self._root_dir, ".fishpi_config")
    
    @property
    def navigation_data_path(self):
        return os.path.join(self._root_dir, "navigation")
    
    @property
    def imgs_path(self):
        return os.path.join(self._root_dir, "imgs")
    
    @property
    def logs_path(self):
        return os.path.join(self._root_dir, "logs")

    def resources_folder(self):
        """ Configured resources folder relative to code paths. """
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')

    #
    # device configuration section
    #
 
    @property
    def devices(self):
        """ Attached devices. """
        return self._devices

    def configure_devices(self, debug=False):
        """ Configures i2c devices when running in appropriate environment. """
        
        # only configure devices for Linux
        if not(platform.system() == "Linux"):
            logging.info("CFG:\tNot running on Linux distro. Not configuring i2c or other devices.")
            self.set_dummy_devices()
            return
        
        # although i2c may work if in correct user group, GPIO needs confirming.
        # for now, clearer just to object if not running as root (sudo)
        #if not(os.getuid() == 0):
        #    logging.info("Not running on as root. Not configuring i2c or other devices.")
        #    self.set_dummy_devices()
        #    return
            
        # running as root on linux so can scan for devices and configure them
        # although inline imports normally not encouraged
        # enables me to load dependencies only when I know I can (eg linux, i2c, root, etc...)
        import raspberrypi
    
        # i2c devices
        try:
            logging.info("CFG:\tConfiguring i2c devices...")
            # scan for connected devices
            i2c_addresses = self.scan_i2c(debug=debug)

            # lookup available device drivers by address
            for addr, in_use in i2c_addresses:
                device_name, device_driver = self.lookup(addr, debug=debug)
                self._devices.append([addr, device_name, device_driver, in_use])
                            
        except Exception as ex:
            logging.exception("CFG:\tError scanning i2c devices - %s" % ex)

        # if no GPS (eg i2c) set up, then import a serial one. Should check for device present first.
        if not(self.gps_sensor):
            try:
                from sensor.GPS_serial import GPS_AdafruitSensor
                self.gps_sensor = GPS_AdafruitSensor(serial_bus=raspberrypi.serial_bus(), debug=debug)
            except Exception as ex:
                logging.warning("CFG:\tError setting up GPS over serial - %s" % ex)

        # CameraController (over USB)
        try:
            from sensor.camera import CameraController
            self.camera_controller = CameraController(self, debug=debug)
        except Exception as ex:
            logging.info("CFG:\tCamera support unavailable - %s" % ex)
            self.camera_controller = DummyCameraController(self.resources_folder())

        # any remaining dummy devices
        if not(self.drive_controller):
            self.drive_controller = DummyDriveController()
    
        # TODO add non i2c device detection eg webcams on /dev/video*, provide driver classes

    def lookup(self, addr, debug=False):
        """ lookup available device drivers by hex address,
            import and create driver class,
            setup particular devices so easily retrieved by consumers. """
        if(debug):
            logging.debug("CFG:\tChecking for driver for device at i2c %s" % addr)
        
        # TODO replace with reading from config? probably use ConfigParser?
        # note: i2c addresses can conflict
        # could scan registers etc to confirm count etc?
        import raspberrypi
        
        if addr == 0x68:
            return "RTC", "Driver not loaded - DS1307"
        
        elif addr == 0x20:
            try:
                from sensor.GPS_I2C import GPS_NavigatronSensor
                self.gps_sensor = GPS_NavigatronSensor(i2c_bus=raspberrypi.i2c_bus(), debug=debug)
            except Exception as ex:
                logging.warning("CFG:\tError setting up GPS over i2c - %s" % ex)
            return "GPS", self.gps_sensor
        
        elif addr == 0x48:
            try:
                from sensor.temperature_TMP102 import TemperatureSensor
                self.temperature_sensor = TemperatureSensor(i2c_bus=raspberrypi.i2c_bus(), debug=debug)
            except Exception as ex:
                logging.warning("CFG:\tError setting up TEMPERATURE over i2c - %s" % ex)
            return "TEMPERATURE", self.temperature_sensor
                    
        elif addr == 0x60:
            try:
                from sensor.compass_CMPS10 import Cmps10_Sensor
                self.compass_sensor = Cmps10_Sensor(i2c_bus=raspberrypi.i2c_bus(), debug=debug)
            except Exception as ex:
                logging.warning("CFG:\tError setting up COMPASS over i2c - %s" % ex)
            return "COMPASS", self.compass_sensor
        
        elif addr == 0x40: #or addr == 0x70:
            # DriveController (using Adafruit PWM board) (not sure what 0x70 address is for...)
            try:
                from vehicle.drive_controller import AdafruitDriveController
                # TODO pwm addresses from config?
                self.drive_controller = AdafruitDriveController(i2c_addr=addr, i2c_bus=raspberrypi.i2c_bus(), debug=debug)
            except Exception as ex:
                logging.info("CFG:\tError setting up DRIVECONTROLLER over i2c - %s" % ex)
                self.drive_controller = DummyDriveController()
            return "DRIVECONTROLLER", self.drive_controller
        
        elif addr == 0x32:
            # DriveController (using RaspyJuice)
            try:
                from vehicle.drive_controller import PyJuiceDriveController
                # TODO pwm addresses from config?
                self.drive_controller = PyJuiceDriveController(i2c_addr=addr, i2c_bus=raspberrypi.i2c_bus(), debug=debug)
            except Exception as ex:
                logging.info("CFG:\tError setting up DRIVECONTROLLER over i2c - %s" % ex)
                self.drive_controller = DummyDriveController()
            return "DRIVECONTROLLER", self.drive_controller
    
        elif addr == 0x1E:
            return "COMPASS", "Driver not loaded - HMC5883L"
                
        elif addr == 0x53 or addr == 0x1D:
            # 0x53 when ALT connected to HIGH
            # 0x1D when ALT connected to LOW
            return "ACCELEROMETER", "Driver not loaded - ADXL345"
                
        elif addr == 0x69:
            # 0x68 when AD0 connected to LOW - conflicts with DS1307!
            # 0x69 when AD0 connected to HIGH
            return "GYRO", "Driver not loaded - ITG3200"
                
        else:
            return "unknown", None

    def scan_i2c(self, debug=False):
        """scans i2c port returning a list of detected addresses.
            Requires sudo access.
            Returns True for in use by a device already (ie UU observed)"""
        
        import raspberrypi
	
        proc = subprocess.Popen(['sudo', 'i2cdetect', '-y', raspberrypi.i2c_bus_num()], 
                stdout = subprocess.PIPE,
                close_fds = True)
        std_out_txt, std_err_txt = proc.communicate()

        if debug:
            logging.debug(std_out_txt)
            logging.debug(std_err_txt)
        
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
                    logging.info("    ...device at: %s %s", hex(16*i+j), cell)
                    hexAddr = 16*i+j
                    if cell == "UU":
                        addr.append([hexAddr, True])
                    else:
                        addr.append([hexAddr, False])
        
        return addr

    def set_dummy_devices(self):
        """ Initialises 'dummy' devices that usually just log on actions. """
        self.camera_controller = DummyCameraController(self.resources_folder())
        self.drive_controller = DummyDriveController()


class DummyCameraController(object):
    """ 'Dummy' camera controller that just logs. """
    
    def __init__(self, resources_folder):
        self.enabled = False
        from PIL import Image
        temp_image_path = os.path.join(resources_folder, 'camera.jpg')
        self._last_img = Image.open(temp_image_path)
    
    def capture_now(self):
        if self.enabled:
            logging.debug("CAM:\tCapture image.")
        pass
    
    @property
    def last_img(self):
        return self._last_img

class DummyDriveController(object):
    """ 'Dummy' drive controller that just logs. """
    
    # current state
    throttle_level = 0.0
    steering_angle = 0.0
    
    def __init__(self):
        pass
    
    def set_throttle(self, throttle_level):
        logging.debug("DRIVE:\tThrottle set to: %s" % throttle_level)
        self.throttle_level = throttle_level
        pass
    
    def set_steering(self, angle):
        logging.debug("DRIVE:\tSteering set to: %s" % angle)
        self.steering_angle = angle
        pass
    
    def halt(self):
        logging.debug("DRIVE:\tDrive halting.")
        self.throttle_level = 0.0
        self.steering_angle = 0.0
        pass

