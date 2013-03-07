
#
# FishPi - An autonomous drop in the ocean
#
# Webclient for RPC interface
#

import logging
import math

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

    def connectionMade(self):
        logging.debug("RPC:\tConnection made.")
    
    def connectionLost(self, reason):
        logging.debug("RPC:\tConnection lost.")
    
    def close_connection(self):
        logging.debug("RPC:\tClosing RPC connection.")
        # TODO: not sure this is the cleanest way to close - check
        if self.transport:
            self.transport.loseConnection()
        reactor.stop()

    def sum(self, a, b):
        self.callRemote(SumCmd, a=a, b=b).addCallback(self.gotResult)

    def gotResult(self, result):
        logging.debug("RPC:\tResponse: %d" % result['status'])

    def update(self):
        self.callRemote(QueryStatus).addCallback(self.status_update)

    def status_update(self, result):
        logging.debug(result)


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
        self.gui.rpc_client = rpc_protocol
        return rpc_protocol
    
    def clientConnectionLost(self, transport, reason):
        logging.debug("RPC:\tConnection lost - %s" % reason)
        self.gui.rpc_client = None
        ReconnectingClientFactory.clientConnectionLost(self, transport, reason)

    def clientConnectionFailed(self, transport, reason):
        logging.debug("RPC:\tConnection failed - %s" % reason)
        self.gui.rpc_client = None
        ReconnectingClientFactory.clientConnectionFailed(self, transport, reason)
