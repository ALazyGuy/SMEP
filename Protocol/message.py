class Message:
    __fields = None

    def __init__(self, device, msg_type):
        self.__device = device
        self.__type = msg_type

    def calc(self):
        result = [self.__device, self.__type]
        for field in self.__fields:
            result += field.calc()
        return bytearray(result)

    def add_field(self, field):
        if self.__fields is not None:
            self.__fields.append(field)
        else:
            self.__fields = [field]

    @property
    def fields(self):
        return self.__fields


class Field:
    def __init__(self, size, data: []):
        self.__size = size
        self.__data = data

    def calc(self):
        return [self.__size] + self.__data


def decode(message_bytes):
    data = [item for item in message_bytes]
    result = Message(data[0], data[1])
    index = 2
    while index < len(data):
        size = data[index]
        field_data = data[(index + 1):(index + size + 1)]
        index += size + 1
        result.add_field(Field(size, field_data))

    return result

