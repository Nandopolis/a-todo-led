import json

from twisted.internet.serialport import SerialPort
from twisted.logger import Logger
from twisted.protocols.basic import LineReceiver


class SerialClientProtocol(LineReceiver):
    def connectionMade(self):
        self.log = Logger(namespace="serial")
        self.log.debug("serial port connected")

    def lineReceived(self, line):
        from . import ws_factory
        
        self.log.debug("serial rx: {line}", line=line)
        try:
            data = line.strip()
            if data == b"r":
                if not ws_factory.client:
                    self.log.error("websocket client not connected")
                else:
                    self.log.debug("serial tx: k")
                    self.sendLine(b"k")
                    data_json = json.dumps({"data_type": "counter"})
                    self.log.debug("sending data to ws: {data}", data=data_json)
                    ws_factory.client.sendMessage(data_json.encode("utf8"))
            else:
                commands = data.split(b"#")
                data_array = []
                for command in commands:
                    values = command.split(b",")
                    cmd = values[0].decode()
                    data_dict = {"data_type": cmd}
                    if values[0] in [b"vel", b"pos", b"lap"] :
                        if len(values) > 1:
                            data_dict[cmd + "_1"] = int.from_bytes(values[1], "big") if values[1] else 0
                        else:
                            data_dict[cmd + "_1"] = 0
                        if len(values) > 2:
                            data_dict[cmd + "_2"] = int.from_bytes(values[2], "big")
                        else:
                            data_dict[cmd + "_2"] = 0
                    elif values[0] == b"goal":
                        data_dict["goal_lap"] = int.from_bytes(values[1], "big")
                    elif values[0] == b"play":
                        if len(values) > 1:
                            data_dict["status"] = True if int.from_bytes(values[1], "big") == 1 else False
                        else:
                            data_dict["status"] = False
                    elif values[0] == b"win":
                        data_dict["winner"] = int.from_bytes(values[1], "big")
                    elif values[0] == b"time":
                        if len(values) > 1:
                            data_dict["seconds"] = int.from_bytes(values[1], "big") / 1000
                        else:
                            data_dict["seconds"] = 0.0
                    else:
                        self.log.error("command not supported: {cmd}", cmd=values[0])
                        data_dict = None
                    if data_dict:
                        data_array.append(data_dict)
                if data_array:
                    if  not ws_factory.client:
                        self.log.error("websocket client not connected")
                    else:
                        data_json = json.dumps(data_array)
                        self.log.debug("sending data to ws: {data}", data=data_json)
                        ws_factory.client.sendMessage(data_json.encode("utf8"))
                    pass
        except Exception as e:
            self.log.error("error: {e}", e=e)

    def sendMessage(self, message: str):
        self.log.debug("serial tx: {message}", message=message)
        self.sendLine(message.encode("utf8"))
