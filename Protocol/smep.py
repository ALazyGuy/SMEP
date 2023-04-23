import _thread
import threading

import client
import message
import server


class Smep:

    def __init__(self, device, port, raspberry):
        self.__client = client.Client(device.value)
        self.__server = server.Server(port, self.__client)
        self.__is_controller = device == message.DeviceId.CONTROLLER
        self.__raspberry = raspberry

    @property
    def client(self):
        return self.__client

    def register_callback(self, message_type, callback):
        self.__server.register_callback(message_type.value, callback)

    def start(self):
        self.__server.init()
        if self.__raspberry:
            _thread.start_new_thread(self.__server.run, ())
        else:
            threading.Thread(target=self.__server.run).start()
            