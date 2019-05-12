from .ws_server import WsServerFactory, WsServerProtocol


ws_factory = WsServerFactory(u"ws://localhost:8080")
ws_factory.protocol = WsServerProtocol


from .serial_client import SerialClientProtocol


serial = SerialClientProtocol()
