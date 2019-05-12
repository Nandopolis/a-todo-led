import json

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.logger import Logger


class WsServerFactory(WebSocketServerFactory):
    def __init__(self, uri):
        WebSocketServerFactory.__init__(self, uri)
        self.client = None


class WsServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        self.log = Logger(namespace="new")
        self.log.debug("peer: {peer}", peer=request.peer)
        self.log.namespace = request.peer[5:]

    def onOpen(self):
        if None != self.factory.client:
            self.sendMessage("there is already a client".encode("utf8"))
            self.sendClose()
        else:
            self.factory.client = self
            self.log.debug("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        from . import serial
        
        if isBinary:
            self.log.debug("Binary message received: {data}", data=payload)
            self.sendMessage("invalid operation".encode("utf8"))
            self.sendClose()
        else:
            try:
                raw_data = payload.decode('utf8').strip()
                data = json.loads(raw_data)
                self.log.debug("Text message received: {data}", data=data)
                if not "data_type" in data:
                    self.sendMessage("invalid operation".encode("utf8"))
                    self.sendClose()
                else:
                    if data["data_type"] == "counter":
                        self.log.debug("serial: {s}", s=serial)
                        serial.sendMessage("s")
            except Exception as e:
                self.log.error("error: {e}", e=e)
                self.sendClose()
    
    def onClose(self, wasClean, code, reason):
        self.log.debug("WebSocket connection closed: {0}".format(reason))
        if self == self.factory.client:
            self.factory.client = None

