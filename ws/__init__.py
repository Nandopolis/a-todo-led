from .ws_server import WsServerFactory, WsServerProtocol


ws_factory = WsServerFactory(u"ws://0.0.0.0:8080")
ws_factory.protocol = WsServerProtocol


from .serial_client import SerialClientProtocol


serial = SerialClientProtocol()
