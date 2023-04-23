import socket
import message


class Server:
    __sock = None

    def __init__(self, port, client):
        self.__port = port
        self.__client = client

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
                print([x for x in msg.calc()])
            except OSError:
                print("Connection closed")
            finally:
                if client is not None:
                    client.close()
