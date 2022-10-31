class HashTable:
    def __init__(self):
        self.__table = {}
        self.__size = 0
        self.__capacity = 100

    def hash_function(self, key):
        return hash(key) % self.__capacity

    def add(self, value):
        index = self.get_position(value)
        if index in self.__table.keys():  # the identifier is already in the ST
            self.__table[index].append(value)
            return index
        self.__table[index] = [value]
        self.__size += 1
        return index

    def get_position(self, key):
        index = self.hash_function(key)
        return index

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
