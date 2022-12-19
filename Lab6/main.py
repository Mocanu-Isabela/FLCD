# Recursive Descendent - functions corresponding to moves
# (expand, advance, momentary insuccess, back, another try, success)
from grammar import Grammar


class RecursiveDescendent:
    def __init__(self):
        self.s = "q"
        self.i = 0
        self.alpha = []
        self.beta = []
        self.grammar = Grammar()
        file = "C:\\Users\\Isabela\\Desktop\\GitHub\\FLCD\\Lab6\\g2.txt"
        self.grammar.read_from_file(file)
        self.terminals = self.grammar.get_terminals()
        self.non_terminals = self.grammar.get_non_terminals()
        self.initial = self.non_terminals[0]

    def expand(self):
        current = self.beta.pop(0)
        self.alpha.append((current, 1))
        productions = self.grammar.get_productions_for_a_given_non_terminal(current)
        x = 0
        for el in productions[0]:
            self.beta.insert(x, el)
            x += 1

    def advance(self):
        self.i += 1
        current = self.beta.pop(0)
        self.alpha.append((current, 1))

    def momentary_insuccess(self):
        self.s = "b"

    def back(self):
        self.i -= 1
        current = self.alpha.pop(0)
        self.beta.insert(0, current)

    def another_try(self):
        (current, nr) = self.alpha.pop()
        productions = self.grammar.get_productions_for_a_given_non_terminal(current)
        if nr < len(productions):
            self.s = "q"
            self.alpha.append((current, nr + 1))
            x = 0
            for el in productions[nr]:
                self.beta.insert(x, el)
                x += 1
        else:
            if self.i == 1 and current == self.initial:
                self.s = "e"
            else:
                self.beta.insert(0, current)

    def success(self):
        self.s = "f"

    # def start(self):
    #     current = self.beta.pop(0)
    #     if current in self.terminals:
    #         pass  # advance
    #     elif current in self.non_terminals:
    #         pass  # expand
    #     # else:
    #     #     self.s = "e"


def tests():
    rd = RecursiveDescendent()
    rd.beta = ["operator", "program"]
    rd.expand()
    assert rd.alpha == [('operator', 1)]
    assert rd.beta == ['+', 'program']
    rd.advance()
    assert rd.i == 1
    assert rd.beta == ['program']
    assert rd.alpha == [('operator', 1), ('+', 1)]
    rd.momentary_insuccess()
    assert rd.s == "b"
    rd.back()
    assert rd.i == 0
    assert rd.beta == [('operator', 1), 'program']
    assert rd.alpha == [('+', 1)]
    rd.alpha = [("operator", 1), ("type", 1)]
    rd.another_try()
    assert rd.alpha == [('operator', 1), ('type', 2)]
    assert rd.s == "q"
    assert rd.beta == ['bool', ('operator', 1), 'program']
    rd.success()
    assert rd.s == "f"
    print("TEST DONE :)")


if __name__ == '__main__':
    tests()
