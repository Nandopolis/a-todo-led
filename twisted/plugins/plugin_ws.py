from twisted.application import internet
from twisted.application.service import IServiceMaker, MultiService
from twisted.internet import reactor
from twisted.internet.serialport import SerialPort
from twisted.plugin import IPlugin
from twisted.python import usage
from zope.interface import implementer

from ws import ws_factory, serial


class Options(usage.Options):
    optParameters = [
        ["port", "p", u'/dev/ttyACM0', "serial port"],
        ["baudrate", "b", 115200, "serial baudrate"],
    ]


@implementer(IServiceMaker, IPlugin)
class WsServiceMaker(object):
    tapname = "ws"
    description = "Run a websocket server, and receives data from a serial device, plugin for a-todo-led game"
    options = Options

    def makeService(self, options):
        service = MultiService()

        ws_service = internet.TCPServer(8080, ws_factory)
        ws_service.setName("ws_server")
        ws_service.setServiceParent(service)

        port = options["port"]
        baudrate = int(options["baudrate"])
        serial_device = SerialPort(serial, port, reactor, baudrate=baudrate)

        return service


# Now construct an object which *provides* the relevant interfaces
# The name of this variable is irrelevant, as long as there is *some*
# name bound to a provider of IPlugin and IServiceMaker.

serviceMaker = WsServiceMaker()
