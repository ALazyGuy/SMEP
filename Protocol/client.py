import socket

import message


class Client:
    __storage = None

    def __init__(self, device):
        self.__device = device

    def get_item_by_ip(self, ip):
        if self.__storage is not None:
            for item in self.__storage:
                if item.ip == ip:
                    return item

        return None

    def send(self, address, port, msg):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((address, port))
            sock.send(msg.calc())

    def update_storage(self, storage):
        self.__storage = storage

    def normal_generator(self, msg_type, data):
        m = message.Message(self.__device, msg_type)

        if data is not None:
            for field_data in data:
                m.add_field(message.Field(len(field_data), field_data))

        return m

    def error_generator(self, error_type):
        f = message.Field(0x1, [error_type])
        m = message.Message(self.__device, 0x6 + (self.__device == message.DeviceId.CONTROLLER))
        m.add_field(f)
        return m
