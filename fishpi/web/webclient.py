
#
# FishPi - An autonomous drop in the ocean
#
# Webclient for RPC interface
#

import logging
import math
from datetime import datetime

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.protocols.amp import AMP

from commands import *

# callback interval in seconds
callback_interval = 1

class RPCClient(AMP):
    """ Client Protocol for rpc connection. """
    
    def __init__(self):
        logging.debug("RPC:\tCreating Protocol...")
        self.factory = None
        self.data = StatusData()

    def connectionMade(self):
        logging.debug("RPC:\tConnection made.")
    
    def connectionLost(self, reason):
        logging.debug("RPC:\tConnection lost.")
    
    def close_connection(self):
        logging.debug("RPC:\tClosing RPC connection.")
        # tell protocol factory not to attempt reconnects
        if self.factory:
            self.factory.stopTrying()
        # close the actual connection
        # TODO: transport not set
        if self.transport:
            self.transport.loseConnection()
        reactor.stop()

    # RPC Commands
    
    def update(self):
        """ RPC call to get status update. """
        self.callRemote(QueryStatus).addCallback(self.status_update)

    def status_update(self, result):
        """ callback from status update. """
        logging.debug("RPC:\tResponse - %s" % result)
        self.data.lat = result['lat']
        self.data.lon = result['lon']
    
        self.data.gps_heading = result['gps_heading']
        self.data.gps_speed = result['gps_speed']
        self.data.altitude = result['altitude']
    
        self.data.fix = result['fix']
        self.data.num_sat = result['num_sat']
    
        self.data.compass_heading = result['compass_heading']
    
        self.data.datestamp = result['datestamp']
        self.data.timestamp = result['timestamp']
    
        self.data.temperature = result['temperature']

    def cmd_callback(self):
        """ General callback. """
        logging.debug("RPC:\Command executed.")
    
    def halt(self):
        """ RPC call to get call HaltCmd. """
        self.callRemote(HaltCmd)

    def set_manual_mode(self):
        """ RPC call to get call ModeCmd. """
        self.callRemote(ModeCmd, mode="manual")
    
    def set_auto_mode(self):
        """ RPC call to get call ModeCmd. """
        self.callRemote(ModeCmd, mode="auto")

    def set_navigation(self, speed, heading):
        """ RPC call to get call NavigationCmd (for auto-pilot). """
        self.callRemote(NavigationCmd, speed=speed, heading=heading)

    def set_drive(self, throttle, steering):
        """ RPC call to get call ManualDriveCmd (for manual drive). """
        self.callRemote(ManualDriveCmd, throttle=throttle, steering=steering)

    def pulse_heartbeat(self):
        """ RPC call to get call HeartbeatCmd. """
        self.callRemote(HeartbeatCmd).addCallback(self.cmd_callback)
    
    def exit(self):
        """ RPC call to get call ExitCmd. """
        self.callRemote(ExitCmd).addCallback(self.cmd_callback)

class StatusData:
    """ Data from the rpc client calls. """

    def __init__(self):
        self.lat = None
        self.lon = None
        self.gps_heading = None
        self.gps_speed = None
        self.altitude = None
        self.fix = False
        self.num_sat = None
        self.compass_heading = None
        dt = datetime.today()
        self.timestamp = dt.time()
        self.datestamp = dt.date()
        self.temperature = None

class RPCClientFactory(ReconnectingClientFactory):
    """ Factory for rpc client connection. Manages UI reference to active protocol. """
    
    def __init__(self, gui):
        self.gui = gui
        self.protocol = RPCClient

    def startedConnecting(self, connector):
        logging.debug("RPC:\tStarted connecting...")

    def buildProtocol(self, addr):
        logging.debug("RPC:\tConnected.")
        self.resetDelay()
        # build protocol
        rpc_protocol = self.protocol()
        rpc_protocol.factory = self
        self.gui.set_rpc_client(rpc_protocol)
        return rpc_protocol
    
    def clientConnectionLost(self, transport, reason):
        logging.debug("RPC:\tConnection lost - %s" % reason)
        self.gui.lost_rpc_client()
        ReconnectingClientFactory.clientConnectionLost(self, transport, reason)

    def clientConnectionFailed(self, transport, reason):
        logging.debug("RPC:\tConnection failed - %s" % reason)
        self.gui.lost_rpc_client()
        ReconnectingClientFactory.clientConnectionFailed(self, transport, reason)
