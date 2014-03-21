#
# FishPi - An autonomous drop in the ocean
#
# Support Code for RaspberryPi

import hw_config


class RaspberryPiSupport(object):
    """ Support package for RaspBerry Pi """

    def __init__(self):
        hw_config.platform = 'RPi'
