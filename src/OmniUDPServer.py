import SocketServer
from base.OmniComponent import OmniComponent

__author__ = 'Sefverl'


class OmniUDPServer(SocketServer.UDPServer, OmniComponent):
    def __init__(self, core_instance, server_address, request_handler):
        OmniComponent.__init__(self, core_instance)
        SocketServer.UDPServer.__init__(self, server_address, request_handler)
