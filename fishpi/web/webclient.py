
#
# FishPi - An autonomous drop in the ocean
#
# Webclient for RPC interface
#

import logging
import math

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

# callback interval in seconds
callback_interval = 1

class RPCClient:

    def __init__(self, server, rpc_port, camera_port):
        self._server = server
        self._rpc_port = rpc_port
        self._camera_port = camera_port
    
    
    
    @property
    def server(self):
        """ Server address for remote device. """
        return self._server

    @property
    def rpc_port(self):
        """ Port for RPC. """
        return self._rpc_port

    @property
    def camera_port(self):
        """ Port for camera stream. """
        return self._camera_port
