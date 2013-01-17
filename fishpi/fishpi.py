#!/usr/bin/python

#
# FishPi - An autonomous drop in the ocean
#
# Entry point to the control software
# - check cmd line args
# - perform self check
#   - last running state
#   - check power level critical
# - configure devices
#   - scan and configure attached devices
#   - check config file
# - run selected mode
#   0: inactive (exits)
#   1: local process with UI and device control (default)
#   2: manual UI process connected to remote device
#   3: remote device process expecting manual control
#   4: remote device process expecting full auto control

import sys
import logging
import argparse

import ui.controller
from core_kernel import FishPiKernel
from localconfig import FishPiConfig

FISH_PI_VERSION = 0.2

class FishPiRunMode:
    Inactive = 'inactive'
    Local = 'local'
    Manual = 'manual'
    Remote = 'remote'
    Auto = 'auto'
    Modes = [Inactive, Local, Manual, Remote, Auto]

class FishPi:
    """ Entrypoint and setup class. """
    selected_mode = FishPiRunMode.Manual
    config = FishPiConfig()

    def __init__(self):
        # parse cmd line args
        parser = argparse.ArgumentParser(description='FishPi - An autonomous drop in the ocean.')
        parser.add_argument("-m", "--mode", help="operational mode to run", choices=FishPiRunMode.Modes, default=FishPiRunMode.Local, type=str, action='store')
        parser.add_argument("-d", "--debug", help="increase debugging information output", action='store_true')
        parser.add_argument("--version", action='version', version='%(prog)s {0}'.format(FISH_PI_VERSION))
        parser.add_argument("-s", "--server", help="server for remote device", default="raspberrypi.local", type=str, action='store')
        parser.add_argument("-dp", "--devport", help="port for device rpc", default="2040", type=str, action='store')
        parser.add_argument("-cp", "--camport", help="port for camera stream", default="8080", type=str, action='store')
        
        # TODO - add further arguments here
        #parser.add_argument(...)        
        
        # and parse
        selected_args = parser.parse_args()
        self.selected_mode = selected_args.mode
        self.debug = selected_args.debug
        self.server = selected_args.server
        self.rpc_port = selected_args.devport
        self.camera_port = selected_args.camport

        # init rest
        logging.info("FISHPI:\tInitializing FishPi (v{0})...".format(FISH_PI_VERSION))

    def self_check(self):
        # TODO implement check for .lastState file
        # check contents for run mode and stable exit
        logging.info("FISHPI:\tChecking last running state...")
        
        # TODO check for sufficient power for normal operation
        # otherwise implement eg emergency beacon mode
        logging.info("FISHPI:\tChecking sufficient power...")


    def configure_devices(self):
        """ Configures eg i2c and other attached devices."""
        self.config.configure_devices(self.debug)

    def run(self):
        """ Runs selected FishPi mode."""
        logging.info("FISHPI:\tStarting FishPi in mode: {0}".format(self.selected_mode))
        if self.selected_mode == FishPiRunMode.Inactive:
            logging.info("FISHPI:\tInactive mode set - exiting.")
            return 0
        elif self.selected_mode == FishPiRunMode.Local:
            return self.run_ui()
        elif self.selected_mode == FishPiRunMode.Manual:
            return self.run_ui()
        elif self.selected_mode == FishPiRunMode.Remote:
            return self.run_headless()
        elif self.selected_mode == FishPiRunMode.Auto:
            return self.run_auto()
        else:
            logging.error("FISHPI:\tInvalid mode! Exiting.")
            return 1

    def run_ui(self):
        """ Runs in UI mode. """
        if self.selected_mode == FishPiRunMode.Local:
            # configure
            self.configure_devices()
        
            # create controller
            kernel = FishPiKernel(self.config, debug=self.debug)
        
            # run ui loop
            logging.info("FISHPI:\tLaunching UI...")
            ui.controller.run_main_view_tk(kernel)
            logging.info("FISHPI:\tProgram complete - exiting.")
        else:
            # create rpc client
            from web.webclient import RPCClient
            rpc_client = RPCClient(self.server, self.rpc_port, self.camera_port)
            # run ui loop
            logging.info("FISHPI:\tLaunching UI...")
            ui.controller.run_main_view_wx(rpc_client)
            logging.info("FISHPI:\tProgram complete - exiting.")
        # done
        return 0

    def run_headless(self):
        """ Runs in headless (manual) mode. """
        # configure
        self.configure_devices()

        # create controller
        kernel = FishPiKernel(self.config, debug=self.debug)

        # testing
        kernel.list_devices()

        # wait for commands...
        logging.info("FISHPI:\tWaiting for commands...")

        # run internal webhost
        import web.webhost
        web.webhost.run_main_host(kernel)
        logging.info("FISHPI:\tProgram complete - exiting.")
        
        # done
        return 0

    def run_auto(self):
        """ Runs in full auto mode. """
        self.configure_devices()
        
        # create controller
        kernel = FishPiKernel(self.config, debug=self.debug)
        
        # testing
        kernel.list_devices()

        # run scripts
        logging.info("FISHPI:\tRunning autonomous scripts...")
        pass
        logging.info("FISHPI:\tNo autonomous scripts implemented - exiting.")
        # done
        return 0

def main():
    fishPi = FishPi()
    fishPi.self_check()
    return fishPi.run()

if __name__ == "__main__":
    status = main()
    sys.exit(status)
