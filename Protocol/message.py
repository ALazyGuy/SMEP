class Message:
    __fields = []

    def __init__(self, device, msg_type):
        self.__device = device
        self.__type = msg_type

    def calc(self):
        result = [self.__device, self.__type]
        for field in self.__fields:
            result += field.calc()
        return bytearray(result)

    def add_field(self, field):
        self.__fields.append(field)


class Field:
    def __init__(self, size, data: []):
        self.__size = size
        self.__data = data

    def calc(self):
        return [self.__size] + self.__data
