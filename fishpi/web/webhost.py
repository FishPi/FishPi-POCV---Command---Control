
#
# FishPi - An autonomous drop in the ocean
#
# Webhost for RPC interface
#

import logging
import math

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
from twisted.protocols.amp import AMP

from commands import *

# callback interval in seconds
callback_interval = 1

def run_main_host(kernel, rpc_port):
    """ Runs main RPC server. """

    # heartbeat gets signaled off at each update and on at each client call
    heartbeat = Heartbeat()
    
    reactor.listenTCP(rpc_port, RPCHostFactory(kernel, heartbeat))
    logging.info("RPC:\tRPC server started on port %s...", rpc_port)
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

class RPCHostFactory(Factory):
    
    def __init__(self, kernel, heartbeat):
        self.core_kernel = kernel
        self.heartbeat = heartbeat
        self.protocol = RPCHost
        self.clients = []

class RPCHost(AMP):
    """ Main RPC host. """
    
    def __init__(self):
        logging.debug("RPC:\tprotocol created.")
    
    def connectionMade(self):
        logging.debug("RPC:\tClient connected.")
        self.factory.clients.append(self)
        self._kernel = self.factory.core_kernel
        self._heartbeat = self.factory.heartbeat
        self._heartbeat.pulse()
    
    def connectionLost(self, reason):
        logging.debug("RPC:\tClient disconnected.")
        self.factory.clients.remove(self)
        self._heartbeat.reset()
        self._kernel.halt()

    @HeartbeatCmd.responder
    def heartbeat_cmd(self, enabled):
        """ Enable or disable keep alive signal (or just pulse if no content). """
        self._heartbeat.pulse()
        self._heartbeat.enabled = enabled
        return {'status':enabled}
    
    @HaltCmd.responder
    def halt_cmd(self):
        """ Halt. """
        self._heartbeat.pulse()
        self._kernel.halt()
        return {'status':True}

    @ModeCmd.responder
    def mode_cmd(self, mode):
        """ Set mode. """
        self._heartbeat.pulse()
        if mode == "manual":
            self._kernel.set_manual_mode()
        elif mode == "auto":
            self._kernel.set_auto_pilot_mode()
        return {'status':mode}
    
    @QueryStatus.responder
    def get_status(self):
        """ Get status. """
        logging.debug("RPC:\tQueryStatus")
        self._heartbeat.pulse()
        dt = self._kernel.data.datestamp
        if dt:
            dt = dt.isoformat()
        ts = self._kernel.data.timestamp
        if ts:
            ts = ts.isoformat()

        status = {'fix': self._kernel.data.fix,
            'lat': self._kernel.data.lat,
            'lon': self._kernel.data.lon,
            'gps_heading': self._kernel.data.gps_heading,
            'gps_speed': self._kernel.data.speed,
            'altitude': self._kernel.data.altitude,
            'num_sat': self._kernel.data.num_sat,
            'timestamp': ts,
            'datestamp': dt,
            'compass_heading': self._kernel.data.compass_heading,
            'temperature': self._kernel.data.temperature}
        #print status
        return status

    @NavigationCmd.responder
    def set_navigation(self, speed, heading):
        """ Set navigation. """
        self._heartbeat.pulse()
        self._kernel.set_speed(speed)
        self._kernel.set_heading(heading)
        return {'status': True}

    @ManualDriveCmd.responder
    def set_drive(self, throttle, steering):
        """ Direct drive. """
        self._heartbeat.pulse()
        # throttle
        self._kernel.set_throttle(throttle)

        # steering
        self._kernel.set_steering(steering)
        return {'status': True}

    @CameraCmd.responder
    def set_camera_mode(self, camera_cmd):
        """ Set the camera recording mode """
        self._heartbeat.pulse()  # why this?
        self._kernel.set_camera_mode(camera_cmd)
        return {'status': True}  # maybe this should at some point become a real command status

    @ExitCmd.responder
    def exit_cmd(self):
        """ Exit. """
        self.halt_cmd()
        reactor.stop()

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
