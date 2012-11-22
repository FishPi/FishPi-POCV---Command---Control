
#
# FishPi - An autonomous drop in the ocean
#
# Webhost for RPC interface
#

import logging

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

def run_main_host(kernel):
    """ Runs main RPC server. """

    RPC_PORT = 2040
    factory = Factory()
    factory.core_kernel = kernel
    factory.protocol = RPCHost
    factory.clients = []
    reactor.listenTCP(RPC_PORT, factory)
    logging.info("RPC:\tRPC server started on port %s...", RPC_PORT)
    # reactor.callLater(callback_interval, update_callback)
    reactor.run()
    
class RPCHost(Protocol):
    """ Main RPC host. """

    def connectionMade(self):
        logging.debug("RPC:\tClient connected.")
        self.factory.clients.append(self)
        self._kernel = self.factory.core_kernel

    def connectionLost(self, reason):
        logging.debug("RPC:\tClient disconnected.")
        self.factory.clients.remove(self)
        self._kernel.halt()

    def dataReceived(self, data):
        """ Process data received. """
        try:
            logging.debug("RPC:\tRec\t%s", data)
            cells = data.split(':')
            if len(cells) > 1:
                command = cells[0]
                content = cells[1]

                msg = ""
                should_exit = False
                # TODO: implement cmds
                if command == "heading":
                    msg = "compass heading:\t%f" % self._kernel.data.compass_heading

                elif command == "speed":
                    msg = "speed:\t%f" % self._kernel.data.speed

                elif command == "exit":
                    should_exit = True
                    reactor.stop()

                if not(should_exit):
                    # broadcast
                    #for c in self.factory.clients:
                        #c.message(msg)

                    # respond
                    self.message(msg)
        
        except Exception as ex:
            logging.exception("RPC:\tError in rpc call - %s" % ex)
        
    def message(self, message):
        logging.debug("RPC:\tSent\t%s", message)
        self.transport.write(str(message) + '\n')

