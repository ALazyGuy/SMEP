import socket
import message


class Server:
    __sock = None

    def __init__(self, port, device_id):
        self.__port = port
        self.__device_id = device_id

    def init(self):
        address = socket.getaddrinfo("0.0.0.0", self.__port)[0][-1]
        self.__sock = socket.socket()
        self.__sock.bind(address)
        self.__sock.listen(1)

    def run(self):
        self.__listen()

    def __listen(self):
        client = None
        while True:
            try:
                client, client_address = self.__sock.accept()
                msg = message.decode(client.recv(512))
                if msg.device >= len(message.VALIDATORS) or msg.device < 0:
                    print(message.ErrorType.UNKNOWN_DEVICE)
                    client.close()
                    continue
                if not message.VALIDATORS[msg.type](msg):
                    print(message.ErrorType.INVALID_MESSAGE)
                    client.close()
                    continue
                print([x for x in msg.calc()])
            except OSError:
                print("Connection closed")
            finally:
                if client is not None:
                    client.close()
