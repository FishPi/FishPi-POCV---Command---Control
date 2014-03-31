#
# FishPi - An autonomous drop in the ocean
#


from time import sleep
import sys

sys.path.append("../../")

import hw_platform.hw_config as hw_config
hw_config.platform = 'BBB'

from hw_platform.support.beaglebone import BeagleBoneSupport

from gpsd_interface import gpsdInterface

bbb = BeagleBoneSupport()
bbb.configure_interface('UART4')

gps_handler = gpsdInterface(interface="UART4", hw_interface="/dev/ttyO4",
    debug=True)
print 'FishPi gpsd Interface Example'
while True:
    print gps_handler.read_raw_gpsd_data()
    sleep(1)
