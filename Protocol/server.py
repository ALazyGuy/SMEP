import socket
import message


class StorageItem:
    def __init__(self, ip, device):
        self.ip = ip
        self.device = device


class Server:
    __sock = None
    __callbacks = None
    __storage = None

    def __init__(self, port, client):
        self.__port = port
        self.__client = client

    def init(self):
        address = socket.getaddrinfo("0.0.0.0", self.__port)[0][-1]
        self.__sock = socket.socket()
        self.__sock.bind(address)
        self.__sock.listen(1)

    def get_item_by_ip(self, ip):
        if self.__storage is not None:
            for item in self.__storage:
                if item.ip == ip:
                    return item

        return None

    def add_to_storage(self, item):
        if self.__storage is None:
            self.__storage = [item]
        elif self.get_item_by_ip(item.ip) is None:
            self.__storage += [item]
        else:
            return

        self.__client.update_storage(self.__storage)
        print(self.__storage[0].ip, " ", self.__storage[0].device)

    def register_callback(self, message_type, callback):
        if self.__callbacks is None:
            self.__callbacks = {message_type: [callback]}
        elif message_type not in self.__callbacks.keys():
            self.__callbacks[message_type] = [callback]
        else:
            self.__callbacks[message_type] += [callback]

    def run(self):
        self.__listen()

    def __listen(self):
        client = None
        while True:
            try:
                client, client_address = self.__sock.accept()
                msg = message.decode(client.recv(512))
                cl_port = 81
                if msg.device >= len(message.VALIDATORS) or msg.device < 0:
                    err_msg = self.__client.error_generator(message.ErrorType.UNKNOWN_DEVICE)
                    # TODO Change 81 to same port
                    self.__client.send(client_address[0], cl_port, err_msg)
                    client.close()
                    continue
                if not message.VALIDATORS[msg.type](msg):
                    err_msg = self.__client.error_generator(message.ErrorType.INVALID_MESSAGE)
                    self.__client.send(client_address[0], cl_port, err_msg)
                    client.close()
                    continue

                if self.__callbacks is not None and msg.type in self.__callbacks.keys():
                    for callback in self.__callbacks[msg.type]:
                        callback(msg, client_address[0], cl_port)

                print([x for x in msg.calc()])
            except OSError:
                pass
                print("Connection closed")
            finally:
                if client is not None:
                    client.close()
