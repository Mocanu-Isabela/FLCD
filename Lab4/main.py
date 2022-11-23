class Transition:
    def __init__(self, source, destination, symbol):
        self.source = source
        self.destination = destination
        self.symbol = symbol


class Run:
    states = []
    alphabet = []
    initial_state = ""
    final_states = []
    transitions = []

    def get_all_from_file(self, states_from_FA, alphabet_from_FA, transitions_from_FA, f_states_from_FA, i_state_from_FA):
        self.states = states_from_FA
        self.alphabet = alphabet_from_FA

        for t in transitions_from_FA:
            trans = Transition(str(t[0]), str(t[1]), str(t[2]))
            if not self.transition_already_exists(trans):
                self.transitions.append(trans)

        for f_s in f_states_from_FA:
            self.final_states.append(f_s)

        self.initial_state = i_state_from_FA[0]

    def transition_already_exists(self, trans):
        for transition in self.transitions:
            if transition.source == trans.source and transition.destination == trans.destination and transition.symbol == trans.symbol:
                return True
            return False

    def get_destination(self, source, symbol):
        destination = ""
        for t in self.transitions:
            if t.source == source and t.symbol == symbol:
                destination = t.destination
                break
        return destination

    def verify_sequence(self, seq):
        if len(seq) == 0:
            if self.initial_state in self.final_states:
                return True
            return False
        current_state = self.initial_state
        for s in seq:
            state = self.get_destination(current_state, s)
            if state == "":
                return False
            else:
                current_state = state
        for final_s in self.final_states:
            if final_s == current_state:
                return True
        return False


def print_menu():
    menu_string = '\nMenu:\n'
    menu_string += '\t 1 - Print states\n'
    menu_string += '\t 2 - Print alphabet\n'
    menu_string += '\t 3 - Print initial state\n'
    menu_string += '\t 4 - Print final states\n'
    menu_string += '\t 5 - Print transitions\n'
    menu_string += '\t 6 - Verify if FA is deterministic or not\n'
    menu_string += '\t 0 - Exit\n'
    print(menu_string)


def start(states, alphabet, initial_state, final_states, transitions):
    stop = False
    run = Run()
    run.get_all_from_file(states, alphabet, transitions, final_states, initial_state)
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
            printer = "States: "
            for state in states:
                printer += str(state)
                printer += " "
            print(printer)
        elif c[0] == '2':
            printer = "Alphabet: "
            for alpha in alphabet:
                printer += str(alpha)

                printer += " "
            print(printer)
        elif c[0] == '3':
            printer = "Initial state: " + str(initial_state[0])
            print(printer)
        elif c[0] == '4':
            printer = "Final states: "
            for f_state in final_states:
                printer += str(f_state)
                printer += " "
            print(printer)
        elif c[0] == '5':
            printer = "Transitions: \n"
            for tran in transitions:
                printer += " "
                tran_to_str = str(tran[0]) + "->" + str(tran[1]) + " :" + str(tran[2]) + "\n"
                printer += str(tran_to_str)
            print(printer)
        elif c[0] == '6':  # 110 ok
            print("Please enter a sequence: ")
            sequence = input()
            verif = run.verify_sequence(sequence)
            if verif:
                print("The sequence is accepted by the FA      YEEEEEY :)")
            else:
                print("The sequence is NOT accepted by the FA")


if __name__ == '__main__':
    file = "C:\\Users\\Isabela\\Desktop\\GitHub\\FLCD\\Lab4\\FA.in"

    fa = open(file, "r")
    program = []
    while True:
        line = fa.readline()
        if not line:
            break
        program.append(line.strip('\n').split(","))
    fa.close()

    FA_states = program[0]
    FA_alphabet = program[1]
    FA_initial_state = program[2]
    FA_final_states = program[3]
    FA_transitions = program[4:]

    start(FA_states, FA_alphabet, FA_initial_state, FA_final_states, FA_transitions)
