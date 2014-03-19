

#
# FishPi - An autonomous drop in the ocean
#
# A new localconfig with a different approach:
# Load a config file (or various) with information about sensors and actuators.
# Drivers are imported dynamically and hardware is set up when needed.
# If a device can not be loaded (or is not specified) a dummy is used instead.
# All drivers need a unified interface for this approach. That means that all
# drivers that are provided by the vendor need a wrapper that creates
# the interface.

import ConfigParser
import logging
import logging.handlers
import os
import platform
import time


class ConfigError(Exception):
    pass


class FishPiConfig(object):

    _devices = []
    _platform = ""
    _root_dir = os.path.join(os.getenv("HOME"), "fishpi")

    def __init__(self):

        self.hardware_model = []    # list of already configured hardware

        # default attachments to None
        self.gps_sensor = None
        self.compass_sensor = None
        self.temperature_sensor = None
        self.drive_controller = None
        self.camera_controller = None

        # load vehicle constants
        self._vehicle_constants = VehicleConstants()

        self.setup_dirs()
        self.setup_logging()

    @property
    def vehicle_constants(self):
        return self._vehicle_constants

    #
    # RPC config
    #

    @property
    def server_name(self):
        return self._server_name

    @server_name.setter
    def server_name(self, value):
        self._server_name = value

    @property
    def rpc_port(self):
        return self._rpc_port

    @rpc_port.setter
    def rpc_port(self, value):
        self._rpc_port = value

    @property
    def camera_port(self):
        return self._camera_port

    @camera_port.setter
    def camera_port(self, value):
        self._camera_port = value

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
        return os.path.join(os.path.dirname(os.path.realpath(__file__)),
            'resources')

    #
    # device configuration section
    #

    @property
    def devices(self):
        """ Attached devices. """
        return self._devices

    # TODO: Insert checks if all important parameters
    #       are present in config file!!

    def configure_devices(self, debug=False):
        """ The setup of all external devices happens here.
            Config data is loaded from file, where fhe platform and the
            connected devices are specified. The resources are imported
            dynamically and the device drivers are set up. """

        # only configure devices for Linux
        if not(platform.system() == "Linux"):
            logging.info("CFG:\tNot running on Linux distro. " +
                "Not configuring i2c or other devices.")
            self._set_dummy_devices()
            return

        device_conf = self.load_config_file('devices.conf')

        if not 'Platform' in device_conf:
            logging.error("CFG:\tSection \"Platform\" not found in " +
                "config file. Only adding dummy devices.")
            self._set_dummy_devices()
            return

        # Load platform support code
        try:
            self.platform_support = self._load_platform_code(
                device_conf['Platform'])()
        except ConfigError:
            return
        del device_conf['Platform']  # Don't need this anymore

        # Load device drivers and configure hardware
        self._load_device_drivers(device_conf, debug)

        # Add dummies for devices that are still missing.
        self._set_dummy_devices()

    def setup_dirs(self):
        """ Create directories """
        if not os.path.exists(self._root_dir):
            os.makedirs(self._root_dir)
        if not os.path.exists(self.navigation_data_path):
            os.makedirs(self.navigation_data_path)
        if not os.path.exists(self.imgs_path):
            os.makedirs(self.imgs_path)
        if not os.path.exists(self.logs_path):
            os.makedirs(self.logs_path)

    def setup_logging(self):
        """ Create and configure logging. """
        # TODO setup logging (from config)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        console = logging.StreamHandler()
        logger.addHandler(console)

        # add file logging
        log_file_stem = os.path.join(self.logs_path, 'fishpi_%s.log' %
            time.strftime('%Y%m%d_%H%M%S'))
        handler = logging.handlers.RotatingFileHandler(log_file_stem,
            backupCount=50)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # can force new file start if needed
        #handler.doRollover()

    def load_config_file(self, file_name):
        """ loads a config file and parses the values. """
        # loading config file
        parser = ConfigParser.RawConfigParser()
        try:
            parser.readfp(open(file_name))
        except IOError:
            logging.error("CFG:\tConfig file %s could not be opened.",
                file_name)
            return None

        # parsing config file
        section_list = parser.sections()
        config = dict()
        for section in section_list:
            config[section] = dict(parser.items(section))
        return config

    def _import_module(self, module_path):
        """ Imports a given Python module """
        try:
            # extracting the last element as module name
            package_list = module_path.split('.')
            module_name = package_list[-1]
            del package_list[-1]
            package = '.'.join(package_list)

            if package:
                module = __import__(package + "." + module_name,
                    fromlist=[package])
            else:
                module = __import__(module_name)
        except ImportError, e:
            logging.error("CFG:\t%s", e)
            return None
        logging.info("CFG:\tImported module %s", module_name)
        return module

    def _load_class(self, class_name, module_path):
        """ Imports a given Python module using _import_module() and
            returns a handle to a specific class in that module """
        module = self._import_module(module_path)
        try:
            ret_class = getattr(module, class_name)
        except Exception:
            logging.error("CFG:\tError while loading %s", class_name)
            return None
        return ret_class

    # let's not use that yet!
    def _load_platform_code(self, platform_conf):
        """ Interpret the platform configuration and import
            the needed libraries """
        logging.info("CFG:\tLoading support module for platform %s..." %
            platform_conf['platform'])

        platform_support_class = self._load_class(platform_conf['driver'],
            platform_conf['module'])

        if platform_support_class is None:
            logging.error("CFG:\tCould not load platform support package. " +
                "Exiting.")
            raise ConfigError
        return platform_support_class()

    def _load_device_drivers(self, device_conf, debug=False):
        # Iterate through devices
        for k in device_conf.keys():
            if not device_conf[k]['interface'] in self.hardware_model:

                # Activate hardware interface
                self.platform_support.configure_interface(
                    device_conf[k]['interface'])

                # Append interface to list
                self.hardware_model.append(device_conf[k]['interface'])

            device_class = self._load_class(device_conf[k]['driver'],
                                    device_conf[k]['module'])
            if device_class is None:
                logging.error("CFG:\tCould not load device driver %s. " +
                    "Configuring dummy device instead."
                    % device_conf[k]['driver'])
                continue
            else:
                # Get device driver handle
                device_handle = device_class(debug=debug)

            if k == 'GPS':
                self._gps_sensor = device_handle
                logging.info("CFG:\tFor GPS loaded driver %s" %
                    device_conf[k]['driver'])
            elif k == 'Magnetometer':
                self._magnetometer_sensor = device_handle
                logging.info("CFG:\tFor magnetometer loaded driver %s" %
                    device_conf[k]['driver'])
            elif k == 'Accelerometer':
                self._accelerometer_sensor = device_handle
                logging.info("CFG:\tFor accelerometer loaded driver %s" %
                    device_conf[k]['driver'])
            elif k == 'Compass':
                self._compass_sensor = device_handle
                logging.info("CFG:\tFor compass loaded driver %s" %
                    device_conf[k]['driver'])
            elif k == 'Gyro':
                self._gyro_sensor = device_handle
                logging.info("CFG:\tFor gyroscope loaded driver %s" %
                    device_conf[k]['driver'])
            elif k == 'Temperature':
                self.temperature_sensor = device_handle
                logging.info("CFG:\tFor temperature sensor loaded driver %s" %
                    device_conf[k]['driver'])
            elif k == 'Drive':
                self.drive_controller = device_handle
                logging.info("CFG:\tFor drive controller loaded driver %s" %
                    device_conf[k]['driver'])

    def _scan_i2c(self, debug=False):
        """ Internal function to scan an I2C bus for devices """
        pass

    def _set_dummy_devices(self):
        """ Goes through the list of devices and adds a dummy for every
            missing device """

        if not self.gps_sensor:
            pass
            # set dummy gps here. gpsfake in combination with gpsd?

        if not self.compass_sensor:
            pass
            # set dummy compass here.

        if not self.temperature_sensor:
            pass
            # set dummy temp sensor here. what is this thing for anyways?

        if not self.drive_controller:
            self.drive_controller = DummyDriveController()

        if not self.camera_controller:
            self.camera_controller = DummyCameraController(
                self.resources_folder())


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


class VehicleConstants:
    """ Constants as configured for a particular physical vehicle. """

    def __init__(self):
        # TODO: calibrate, test and read from config

        # constants for pid controller of throttle
        self.pid_drive_gain_p = 1.0
        self.pid_drive_gain_i = 0.0
        self.pid_drive_gain_d = 0.0
        self.drive_dead_zone = 0.3
        self.drive_max_response = 1.0

        # constants for pid controller of steering
        self.pid_heading_gain_p = 0.9
        self.pid_heading_gain_i = 0.4
        self.pid_heading_gain_d = 0.1
        self.heading_dead_zone = None
        # Pi/4
        self.heading_max_response = 0.785398


if __name__ == "__main__":
    config = FishPiConfig()
    config.configure_devices()
    # create instance, and call for testing.
