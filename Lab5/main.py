# 1.a. recursive descendant 🙂

class Grammar:
    def __init__(self):
        self.non_terminals = []
        self.terminals = []
        self.productions = {}
        self.is_CFG = True

    def get_non_terminals(self):
        return self.non_terminals

    def get_terminals(self):
        return self.terminals

    def get_productions(self):
        return self.productions

    def get_is_CFG(self):
        return self.is_CFG

    def get_productions_for_a_given_non_terminal(self, non_terminal):
        return self.productions[tuple([non_terminal])]

    def read_from_file(self, file):
        fa = open(file, "r")
        while True:
            line = fa.readline()
            if not line or line == "\n":
                break
            self.non_terminals.append(line.strip('\n'))
        while True:
            line = fa.readline()
            if not line or line == "\n":
                break
            self.terminals.append(line.strip('\n'))
        while True:
            line = fa.readline()
            if not line or line == "\n":
                break
            line = line.strip('\n')
            sides = line.split('->')
            left_terms = tuple(sides[0].strip().split(" "))
            right_terms = tuple(sides[1].strip().split(" "))
            if len(left_terms) != 1:
                self.is_CFG = False
            elif left_terms[0] not in self.non_terminals:
                self.is_CFG = False
            if left_terms not in self.productions.keys():
                self.productions[left_terms] = []
            self.productions[left_terms].append(right_terms)
        fa.close()


def print_menu():
    menu_string = '\nMenu:\n'
    menu_string += '\t 1 - Print non terminals\n'
    menu_string += '\t 2 - Print terminals\n'
    menu_string += '\t 3 - Print productions\n'
    menu_string += '\t 4 - Print productions for a given non terminal\n'
    menu_string += '\t 5 - CFG check\n'
    menu_string += '\t 0 - Exit\n'
    print(menu_string)


def start(file):
    stop = False
    grammar = Grammar()
    grammar.read_from_file(file)
    while not stop:
        print_menu()
        ui_command = input("Please enter a command: ")
        c = ui_command.split()

        if len(c) != 1:
            print("Invalid command!")
        elif c[0] == '0':
            print("Have a nice day! :)")
            stop = True
        elif c[0] == '1':
            printer = "Non terminals: "
            non_terminals = grammar.get_non_terminals()
            for non_t in non_terminals:
                printer += str(non_t)
                printer += " "
            print(printer)
        elif c[0] == '2':
            printer = "Terminals: "
            terminals = grammar.get_terminals()
            for term in terminals:
                printer += str(term)
                printer += " "
            print(printer)
        elif c[0] == '3':
            printer = "Productions:\n  "
            productions = grammar.get_productions()
            for prod in productions:
                for term in prod:
                    printer += term + " "
                printer += "-> "
                for left in productions[prod]:
                    if left != productions[prod][0]:
                        printer += "| "
                    for term in left:
                        printer += term + " "
                printer += "\n  "
            print(printer)
        elif c[0] == '4':
            non_terminal = input("Please enter a non terminal: ")
            printer = "Productions of the non terminal you entered:\n  "
            productions_for_given_non_t = grammar.get_productions_for_a_given_non_terminal(non_terminal)
            for pr in productions_for_given_non_t:
                printer += non_terminal + "-> "
                for el in pr:
                    printer += el + " "
                printer += "\n  "
            print(printer)
        elif c[0] == '5':
            cfg = grammar.get_is_CFG()
            if cfg:
                print("The grammar is CFG! :)\n")
            else:
                print("The grammar is NOT CFG! :(\n")


if __name__ == '__main__':
    file = "C:\\Users\\Isabela\\Desktop\\GitHub\\FLCD\\Lab5\\g2.txt"
    start(file)