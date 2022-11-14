from HashTable import HashTable


class Scanner:
    def __init__(self, tokens):
        self.__tokens = tokens
        self.__identifiers = []
        self.__symbol_table = HashTable()
        self.__current_line = 0
        self.__pif = []

    def get_ST(self):
        return self.__symbol_table

    def get_PIF(self):
        return self.__pif

    def scan(self, program):
        for line in program:
            self.__current_line += 1
            self.get_tokens_from_line(str(line[1]))

    def get_tokens_from_line(self, line):
        index = 0

        # we ignore spaces and tabs
        while index < len(line) and (line[index] == " " or line[index] == "\t"):
            index += 1

        for token in self.__tokens:
            if line[index:index + len(token)] == token:  # in case we find a valid token from token.in
                print("Valid Token1 - index: " + str(index))
                print("Valid Token: " + token + "\n")
                self.__pif.append([token, -1])  # we put it in pif with position - 1 and jump over the entire token
                index += len(token)
                break

        # we check if the token is an identifier or a constant
        while index < len(line):
            token_is_identifier_or_constant = False

            if is_a_letter(line[index]) and index > 3 and (line.strip()[0:3] == "DEF" or (
                    line[index - 2] == "d" and line[index - 1] == "(")):
                index = self.treat_identifier(line, index)
                token_is_identifier_or_constant = True
                if index == len(line):
                    break

            if (line[index] == "-" or line[index] == "+") and (index + 1) < len(line) and line[
                index + 1] == "0":
                raise Exception("Lexical error: a number cannot start with 0. Line: " + str(self.__current_line))

            if line[index] == "0" and (index + 1) < len(line) and is_a_digit(line[index + 1]):
                raise Exception("Lexical error: a number cannot start with 0. Line: " + str(self.__current_line))

            expression_instead_of_nr = ((line[index] == "-" or line[index] == "+") and (index + 1) < len(
                line) and is_a_digit(line[index + 1]) and len(self.__pif) != 0) and (
                                               self.__pif[len(self.__pif) - 1][0] == "ident" or
                                               self.__pif[len(self.__pif) - 1][0] == "const")

            if not expression_instead_of_nr:
                ends = [")", ",", " ", "\n", "\t"]
                if ((is_a_digit(line[index]) and (
                        index + 1 == len(line) or ((index + 1) < len(line) and (line[index + 1] in ends)))) or (
                        (line[index] == "-" or line[index] == "+") and (index + 1) < len(line) and is_a_digit(
                    line[index + 1]))):
                    index = self.treat_integer_constant(line, index)
                    token_is_identifier_or_constant = True
                    if index == len(line):
                        break

            if line[index] == '“':
                index = self.treat_string_constant(line, index)
                token_is_identifier_or_constant = True

            if line[index] == "\n":
                index = self.treat_character_constant(line, index)
                token_is_identifier_or_constant = True

            if not token_is_identifier_or_constant:  # if it is not an identifier or a constant, we should check if the next token is from token.in (if it is a reserved word, an operator or a separator)
                valid_token = False

                for token in self.__tokens:
                    if line[index:index + len(token)] == token:  # in case we find a valid token from token.in
                        print("Valid Token2 - index: " + str(index))
                        print("Valid Token: " + token + "\n")
                        valid_token = True
                        self.__pif.append(
                            [token, -1])  # we put it in pif with position - 1 and jump over the entire token
                        index += len(token)
                        break

                if not valid_token:
                    for identifier in self.__identifiers:
                        if line[
                           index:index + len(identifier)] == identifier:  # in case we find a valid token from token.in
                            print("Valid Token3 - index: " + str(index))
                            print("Valid Token: " + identifier + "\n")
                            valid_token = True
                            self.__pif.append([identifier, self.__symbol_table.get_position(identifier)])
                            index += len(identifier)
                            break

                if not valid_token and index < len(line) and not (line[index] == " " or line[index] == "\t"):
                    raise Exception("Lexical error: not a valid token. Line: " + str(self.__current_line))

            # while the next characters are spaces or tab, we should ignore them
            while index < len(line) and (line[index] == " " or line[index] == "\t"):
                index += 1

    def treat_identifier(self, line, index):
        print("Identifier - index: " + str(index))

        identifier = ""
        identifier = identifier + line[index]
        index += 1

        while index < len(line) and (is_a_letter(line[index]) or is_a_digit(line[index])):
            identifier = identifier + line[index]
            index += 1

        print("Identifier: " + identifier + "\n")
        self.add_to_pif_and_st(identifier, "identifier")
        self.__identifiers.append(identifier)
        return index

    def treat_character_constant(self, line, index):
        print("Character Constant - index: " + str(index))

        character = ""
        character = character + line[index]
        index += 1

        if index < len(line) and not is_a_letter(line[index]) and not is_a_digit(line[index]):
            raise Exception("Lexical error: characters must be digits or letters. Line: " + str(self.__current_line))

        if index < len(line) and line[index] != "\n":
            character = character + line[index]

        if index == len(line):
            raise Exception("Lexical error: unclosed quotes for characters. Line: " + str(self.__current_line))

        index += 1
        character = character + line[index]
        index += 1
        self.add_to_pif_and_st(character, "const")

        print("Character Constant: " + character + "\n")
        return index

    def treat_string_constant(self, line, index):
        print("String Constant - index: " + str(index))

        string = ""
        string = string + line[index]
        index += 1

        ok = True
        while index < len(line) and line[index] != '”' and ok:
            string += line[index]
            if not is_a_letter(line[index]) and not is_a_digit(line[index]) and not line[index].isspace():
                ok = False
            index += 1

        if not ok:
            raise Exception(
                "Lexical error: strings must contain digits and/or letters. Line: " + str(self.__current_line))

        if index == len(line):
            raise Exception("Lexical error: unclosed quotes for strings. Line: " + str(self.__current_line))

        string = string + line[index]
        index += 1
        self.add_to_pif_and_st(string, "const")

        print("String Constant: " + string + "\n")
        return index

    def treat_integer_constant(self, line, index):
        print("Integer Constant - index: " + str(index))
        sign = 1
        if line[index] == "-" or line[index] == "+":
            if line[index] == "-":
                sign = -1
            index += 1

        number = 0
        while index < len(line) and is_a_digit(line[index]):
            if line[index] == "0":
                number = number * 10
                index += 1
            else:
                number = number * 10 + int(line[index])
                index += 1

        number = number * sign
        print("Integer Constant: " + str(number) + "\n")
        self.add_to_pif_and_st(number, "const")
        return index

    def add_to_pif_and_st(self, token, type):
        position_in_ST = self.__symbol_table.get_position(token)
        if position_in_ST != -1:
            self.__pif.append([type, position_in_ST])
        else:
            self.__symbol_table.add(token)
            position_in_ST_after_add = self.__symbol_table.get_position(token)
            self.__pif.append([type, position_in_ST_after_add])


def is_a_digit(char):
    if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        return True
    return False


def is_a_letter(char):
    if char.lower() in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                        "t", "u", "v", "w", "x", "y", "z"]:
        return True
    return False
