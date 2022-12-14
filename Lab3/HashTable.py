class HashTable:
    def __init__(self):
        self.__table = {}
        self.__size = 0
        self.__capacity = 80

    def hash_function(self, key):
        return hash(key) % self.__capacity

    def add(self, value):
        index = self.hash_function(value)
        if index in self.__table.keys():  # the identifier is already in the ST
            self.__table[index].append(value)
            return index
        self.__table[index] = [value]
        self.__size += 1
        return index

    def get_size(self):
        return self.__size

    def get_position(self, value):
        index = self.hash_function(value)
        if index not in self.__table.keys():
            return (-1, -1)
        index2 = self.__table[index].index(value)
        position = (index, index2)
        return position

    def printer(self):
        ST = "Position | Symbol\n"
        for token in self.__table.values():
            index = self.get_position(token[0])
            ST += str(index) + " | " + str(token) + "\n"
        return ST
