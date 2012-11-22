
#
# FishPi - An autonomous drop in the ocean
#
# Webhost for RPC interface
#

import logging
import math

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

# callback interval in seconds
callback_interval = 1

def run_main_host(kernel):
    """ Runs main RPC server. """

    # heartbeat gets signaled off at each update and on at each client call
    heartbeat = Heartbeat()
    
    RPC_PORT = 2040
    factory = Factory()
    factory.core_kernel = kernel
    factory.heartbeat = heartbeat
    factory.protocol = RPCHost
    factory.clients = []
    reactor.listenTCP(RPC_PORT, factory)
    logging.info("RPC:\tRPC server started on port %s...", RPC_PORT)
    reactor.callLater(5, update_callback, kernel, heartbeat)
    reactor.run()

def update_callback(kernel, heartbeat):
    """ Callback to perform updates etc. Needs to reregister callback at end. """
    # update kernel
    logging.debug("RPC:\tIn update...")
    
    # check client pulse - otherwise halt vehicle
    if not(heartbeat.is_alive()):
        logging.debug("RPC:\tNo client keep alive call - halting.")
        kernel.halt()
    
    # do update
    kernel.update()
    
    # expect client pulse before next update
    heartbeat.reset()
    # reregister callback
    reactor.callLater(callback_interval, update_callback, kernel, heartbeat)

class Heartbeat:
    """ Maintains a heartbeat from client to server calls. Could be done on a timeout. """

    def __init__(self):
        self._pulse = True
        self._enabled = True

    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value):
        self._pulse = True
        self._enabled = value
    
    def is_alive(self):
        if self.enabled:
            return self._pulse
        else:
            return True
    
    def pulse(self):
        if self.enabled:
            self._pulse = True

    def reset(self):
        if self.enabled:
            self._pulse = False
    
class RPCHost(Protocol):
    """ Main RPC host. """

    def connectionMade(self):
        logging.debug("RPC:\tClient connected.")
        self.factory.clients.append(self)
        self._kernel = self.factory.core_kernel
        self._heartbeat = self.factory.heartbeat

    def connectionLost(self, reason):
        logging.debug("RPC:\tClient disconnected.")
        self.factory.clients.remove(self)
        self._heartbeat.reset()
        self._kernel.halt()

    def dataReceived(self, data):
        """ Process data received. """
        try:
            logging.debug("RPC:\tRec\t%s", data)
            # pulse heartbeat
            self._heartbeat.pulse()
            cells = data.split(':')
            if len(cells) > 1:
                command = cells[0]
                content = cells[1]

                # parse and execute
                msg, should_exit = self.exec_cmds(command.lower().strip(), content.lower().strip())
                
                # respond
                self.message(msg)
                
                # exit if required
                if should_exit:
                    reactor.stop()
        except Exception as ex:
            logging.exception("RPC:\tError in rpc call - %s" % ex)
        
    def message(self, message):
        """ Respond with message. """
        logging.debug("RPC:\tSent\t%s", message)
        self.transport.write(str(message) + '\n')

    def exec_cmds(self, command, content):
        """ Parse and execute commands. """
        msg = ""
        should_exit = False

        # enable or disable keep alive signal (or just pulse if no content)
        if command == "hb":
            if content == "on":
                self._heartbeat.enabled = True
                msg = "HB enabled."
            elif content == "off":
                self._heartbeat.enabled = False
                msg = "HB disabled."
        
        # halt
        elif command == "halt":
            self._kernel.halt()
            msg = "Vehicle halted."
    
        # mode
        elif command == "mode":
            if content == "manual":
                self._kernel.set_manual_mode()
                msg = "Manual mode set."
            elif content == "auto":
                self._kernel.set_auto_pilot_mode()
                msg = "Auto mode set."
                    
        # get status
        elif command == "status":
            fix = self._kernel.data.fix
            lat = self._kernel.data.lat
            lon = self._kernel.data.lon
            gps_heading = self._kernel.data.gps_heading
            gps_speed = self._kernel.data.speed
            altitude = self._kernel.data.altitude
            num_sat = self._kernel.data.num_sat
            timestamp = self._kernel.data.timestamp
            datestamp = self._kernel.data.datestamp
            compass_heading = self._kernel.data.compass_heading
            temperature = self._kernel.data.temperature
            msg = "(fix, lat, lon, gps_heading, gps_speed, altitude, num_sat, timestamp, datestamp, compass, temperature):\t(%d, %f, %f, %f, %f, %f, %d, %s, %s, %f, %f)" % (fix, lat, lon, gps_heading, gps_speed, altitude, num_sat, timestamp, datestamp, compass_heading, temperature)

        # set navigation
        elif command == "nav":
            cells = content.split(',')
            if len(cells) > 1:
                sub_command = cells[0]
                sub_content = float(cells[1])
                if sub_command == "s":
                    self._kernel.set_speed(sub_content)
                    msg = "Speed set:%f" % sub_content
                elif sub_command == "h":
                    self._kernel.set_heading(sub_content)
                    msg = "Heading set:%f" % sub_content
                # other nav commands

        # direct drive
        elif command == "drive":
            cells = content.split(',')
            if len(cells) > 1:
                sub_command = cells[0]
                sub_content = float(cells[1])
                if sub_command == "t":
                    throttle_level = sub_content
                    # expected +/- 100
                    throttle_act = float(throttle_level)/100.0
                    # adjustment for slider so min +/- .3 so if in .05 to .3 range, jump to .3
                    if throttle_act > 0.05 and throttle_act < 0.3:
                        throttle_act = 0.3
                    elif throttle_act < -0.05 and throttle_act > -0.3:
                        throttle_act = -0.3
                    self._kernel.set_throttle(throttle_act)
                    msg = "Throttle set:%f" % throttle_act
                elif sub_command == "s":
                    angle = sub_content
                    angle_in_rad = (float(angle)/180.0)*math.pi
                    # adjustment for slider in opposite direction - TODO - move to drive controller
                    angle_in_rad = angle_in_rad * -1.0
                    self._kernel.set_steering(angle_in_rad)
                    msg = "Steering set:%f" % angle
    
        # img enable / disable
        elif command == "cam":
            if content == "on":
                self._kernel.set_capture_img_enabled(True)
                msg = "Camera enabled."
            elif content == "off":
                self._kernel.set_capture_img_enabled(False)
                msg = "Camera disabled."

        # exit
        elif command == "exit":
            should_exit = True
            msg = "Exiting."

        return msg, should_exit

