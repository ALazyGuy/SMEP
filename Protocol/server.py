import socket
import message


class Server:
    __sock = None

    def __init__(self, port):
        self.__port = port

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
                # TODO Implement message processing
            except OSError:
                print("Connection closed")
            finally:
                if client is not None:
                    client.close()
