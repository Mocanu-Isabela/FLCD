from Scanner import Scanner


if __name__ == '__main__':
    token_file = "D:\\Facultate\\ANUL III\\an 3 sem I\\Formal Languages and Compiler Design (FLCD)\\Labs\\Lab4\\token.in"
    p1 = "D:\\Facultate\\ANUL III\\an 3 sem I\\Formal Languages and Compiler Design (FLCD)\\Labs\\Lab4\\p1.txt"
    p2 = "D:\\Facultate\\ANUL III\\an 3 sem I\\Formal Languages and Compiler Design (FLCD)\\Labs\\Lab4\\p2.txt"
    p3 = "D:\\Facultate\\ANUL III\\an 3 sem I\\Formal Languages and Compiler Design (FLCD)\\Labs\\Lab4\\p3.txt"
    p1err = "D:\\Facultate\\ANUL III\\an 3 sem I\\Formal Languages and Compiler Design (FLCD)\\Labs\\Lab4\\p1err.txt"

    tokens = []
    f = open(token_file, "r")
    for x in f:
        tokens.append(x.split('\n')[0])
    f.close()

    p = p1
    f = open(p, "r")
    program = []
    count = 0
    while True:
        count += 1
        # Get next line from file
        line = f.readline()
        # if line is empty, then the end of file is reached
        if not line:
            break
        program.append([count, line.strip('\n')])
    f.close()

    scanner = Scanner(tokens)
    scanner.scan(program)
    symbolTable = scanner.get_ST()
    pif = scanner.get_PIF()
    PIFstring = "Token | Position in ST\n"
    for element in pif:
        PIFstring += str(element[0]) + " | " + str(element[1]) + "\n"

    f = open("PIF.out", "w")
    f.write(str(PIFstring))
    f.close()

    f = open("ST.out", "w")
    f.write(symbolTable.printer())
    f.close()

    print("Everything OK! Lexically correct :)")
