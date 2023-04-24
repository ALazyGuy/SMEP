import _thread
import threading

import client
import message
import server


class Smep:

    def __init__(self, device, port, raspberry):
        self.__client = client.Client(device)
        self.__server = server.Server(port, self.__client)
        self.__is_controller = device == message.DeviceId.CONTROLLER
        self.__raspberry = raspberry

    @property
    def client(self):
        return self.__client

    def register_callback(self, message_type, callback):
        self.__server.register_callback(message_type, callback)

    def start(self):
        self.__register_handshake_callbacks()
        self.__server.init()
        if self.__raspberry:
            _thread.start_new_thread(self.__server.run, ())
        else:
            threading.Thread(target=self.__server.run).start()

    def __client_accept_callback(self, msg, ip, port):
        self.__server.add_to_storage(server.StorageItem(ip, msg.device))
        response = self.__client.normal_generator(message.MessageType.ACCEPTED_SERVER, None)
        self.__client.send(ip, port, response)

    def __server_initial_scan_callback(self, msg, ip, port):
        self.__server.add_to_storage(server.StorageItem(ip, msg.device))
        response = self.__client.normal_generator(message.MessageType.ACCEPTED_CLIENT, None)
        self.__client.send(ip, port, response)
        response = self.__client.normal_generator(message.MessageType.ONLINE, None)
        self.__client.send(ip, port, response)

    def __register_handshake_callbacks(self):
        if self.__is_controller:
            self.__server.register_callback(message.MessageType.ACCEPTED_CLIENT, self.__client_accept_callback)
        else:
            self.__server.register_callback(message.MessageType.INITIAL_SCAN, self.__server_initial_scan_callback)
