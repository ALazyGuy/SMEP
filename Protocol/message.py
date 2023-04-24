from enum import IntEnum

VALIDATORS = [
    lambda msg: msg.fields is None and msg.device == 0x0,
    lambda msg: msg.fields is None and msg.device != 0x0,
    lambda msg: msg.fields is None and msg.device == 0x0,
    lambda msg: msg.fields is None and msg.device != 0x0,
    lambda msg: msg.fields is None and msg.device == 0x0,
    lambda msg: msg.fields is None and msg.device != 0x0,
    lambda msg: msg.fields is not None and len(msg.fields) == 1 and msg.device == 0x0,
    lambda msg: msg.fields is not None and len(msg.fields) == 1 and msg.device != 0x0
]


class DeviceId(IntEnum):
    CONTROLLER = 0x0
    KETTLE = 0x1


class MessageType(IntEnum):
    INITIAL_SCAN = 0x0
    ONLINE = 0x1,
    ACCEPTED_SERVER = 0x2,
    ACCEPTED_CLIENT = 0x3,
    ERROR_SERVER = 0x6,
    ERROR_CLIENT = 0x7


class ErrorType(IntEnum):
    UNKNOWN_DEVICE = 0x0
    INVALID_MESSAGE = 0x1


class Message:
    __fields = None

    def __init__(self, device, msg_type):
        self.__device = device
        self.__type = msg_type

    def calc(self):
        result = [self.__device, self.__type]
        if self.__fields is not None:
            for field in self.__fields:
                result += field.calc()
        return bytearray(result)

    def add_field(self, field):
        if self.__fields is not None:
            self.__fields.append(field)
        else:
            self.__fields = [field]

    @property
    def device(self):
        return self.__device

    @property
    def type(self):
        return self.__type

    @property
    def fields(self):
        return self.__fields


class Field:
    def __init__(self, size, data: []):
        self.__size = size
        self.__data = data

    @property
    def data(self):
        return int.from_bytes(bytes(self.__data), "big")

    @property
    def raw_data(self):
        return self.__data

    def calc(self):
        return [self.__size] + self.__data


def decode(message_bytes):
    data = [item for item in message_bytes]
    result = Message(data[0], data[1])
    index = 2
    while index < len(data):
        size = data[index]
        if index + size >= len(data):
            break
        field_data = data[(index + 1):(index + size + 1)]
        index += size + 1
        result.add_field(Field(size, field_data))

    return result

