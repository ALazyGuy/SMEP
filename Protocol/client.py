import socket

import message


class Client:
    def __init__(self, device):
        self.__device = device

    def send(self, address, port, msg):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((address, port))
            sock.send(msg.calc())

    def error_generator(self, error_type):
        f = message.Field(0x1, [error_type.value])
        m = message.Message(self.__device, 0x6 + (self.__device == message.DeviceId.CONTROLLER.value))
        m.add_field(f)
        return m
