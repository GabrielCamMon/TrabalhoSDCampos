import random, time, copy, replit
from termcolor import cprint


class CampoMinado:

    # Gets the value of a coordinate on the grid.
    def l(self, r, c, b):
        return b[r][c]


    # Places a bomb in a random location.
    def placeBomb(self, b):
        r = random.randint(0, 8)
        c = random.randint(0, 8)
        # Checks if there's a bomb in the randomly generated location. If not, it puts one there. If there is, it requests a new location to try.
        currentRow = b[r]
        if not currentRow[c] == '*':
            currentRow[c] = '*'
        else:
            self.placeBomb(b)


    # Adds 1 to all of the squares around a bomb.
    def updateValues(self, rn, c, b):
        # Row above.
        if rn - 1 > -1:
            r = b[rn - 1]

            if c - 1 > -1:
                if not r[c - 1] == '*':
                    r[c - 1] += 1

            if not r[c] == '*':
                r[c] += 1

            if 9 > c + 1:
                if not r[c + 1] == '*':
                    r[c + 1] += 1

        # Same row.
        r = b[rn]

        if c - 1 > -1:
            if not r[c - 1] == '*':
                r[c - 1] += 1

        if 9 > c + 1:
            if not r[c + 1] == '*':
                r[c + 1] += 1

        # Row below.
        if 9 > rn + 1:
            r = b[rn + 1]

            if c - 1 > -1:
                if not r[c - 1] == '*':
                    r[c - 1] += 1

            if not r[c] == '*':
                r[c] += 1

            if 9 > c + 1:
                if not r[c + 1] == '*':
                    r[c + 1] += 1


    # When a zero is found, all the squares around it are opened.
    def zeroProcedure(self, r, c, k, b):
        # Row above
        if r - 1 > -1:
            row = k[r - 1]
            if c - 1 > -1: row[c - 1] = self.l(r - 1, c - 1, b)
            row[c] = self.l(r - 1, c, b)
            if 9 > c + 1: row[c + 1] = self.l(r - 1, c + 1, b)

        # Same row
        row = k[r]
        if c - 1 > -1: row[c - 1] = self.l(r, c - 1, b)
        if 9 > c + 1: row[c + 1] = self.l(r, c + 1, b)

        # Row below
        if 9 > r + 1:
            row = k[r + 1]
            if c - 1 > -1: row[c - 1] = self.l(r + 1, c - 1, b)
            row[c] = self.l(r + 1, c, b)
            if 9 > c + 1: row[c + 1] = self.l(r + 1, c + 1, b)


    # Checks known grid for 0s.
    def checkZeros(self, k, b, r, c):
        oldGrid = copy.deepcopy(k)
        self.zeroProcedure(r, c, k, b)
        if oldGrid == k:
            return
        while True:
            oldGrid = copy.deepcopy(k)
            for x in range(9):
                for y in range(9):
                    if self.l(x, y, k) == 0:
                        self.zeroProcedure(x, y, k, b)
            if oldGrid == k:
                return


    # Places a marker in the given location.
    def marker(self, r, c, k):
        k[r][c] = '⚐'
        self.printBoard(k)


    # Prints the given board.
    def printBoard(self, b):
        replit.clear()
        print('    A   B   C   D   E   F   G   H   I')
        print('  ╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗')
        for r in range(0, 9):
            print(r, '║', self.l(r, 0, b), '║', self.l(r, 1, b), '║', self.l(r, 2, b), '║', self.l(r, 3, b), '║',
                  self.l(r, 4, b), '║', self.l(r, 5, b),
                  '║', self.l(r, 6, b), '║', self.l(r, 7, b), '║', self.l(r, 8, b), '║')
            if not r == 8:
                print('  ╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣')
        print('  ╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝')







def executar_jogo():

    cm = CampoMinado()
    # The player chooses a location.
    def choose(b, k, startTime):
        # Variables 'n stuff.
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
        # Loop in case of invalid entry.
        while True:
            chosen = input('Escolha o quadrado (ex. E4) ou marque caso ache que exista bomba (ex. mE4): ').lower()
            # Checks for valid square.
            if len(chosen) == 3 and chosen[0] == 'm' and chosen[1] in letters and chosen[2] in numbers:
                c, r = (ord(chosen[1])) - 97, int(chosen[2])
                cm.marker(r, c, k)
                play(b, k, startTime)
                break
            elif len(chosen) == 2 and chosen[0] in letters and chosen[1] in numbers:
                return (ord(chosen[0])) - 97, int(chosen[1])
            else:
                choose(b, k, startTime)

        # The majority of the gameplay happens here.


    def play(b, k, startTime):
        # Player chooses square.
        c, r = choose(b, k, startTime)
        # Gets the value at that location.
        v = cm.l(r, c, b)
        # If you hit a bomb, it ends the game.
        if v == '*':
            cm.printBoard(b)
            print('Você Perdeu!')
            # Print timer result.
            print('Tempo: ' + str(round(time.time() - startTime)) + 's')
            # Offer to play again.
            playAgain = input('Jogar Novamente? (Y/N): ').lower()
            if playAgain == 'y':
                replit.clear()
                reset()
            else:
                quit()
        # Puts that value into the known grid (k).
        k[r][c] = v
        # Runs checkZeros() if that value is a 0.
        if v == 0:
            cm.checkZeros(k, b, r, c)
        cm.printBoard(k)
        # Checks to see if you have won.
        squaresLeft = 0
        for x in range(0, 9):
            row = k[x]
            squaresLeft += row.count(' ')
            squaresLeft += row.count('⚐')
        if squaresLeft == 10:
            cm.printBoard(b)
            print('Voce Venceu!')
            # Print timer result.
            print('Tempo: ' + str(round(time.time() - startTime)) + 's')
            # Offer to play again.
            playAgain = input('Jogar Novamente? (Y/N): ')
            playAgain = playAgain.lower()
            if playAgain == 'y':
                replit.clear()
                reset()
            else:
                quit()
        # Repeats!
        play(b, k, startTime)


    print()
    cprint('Bem-vindo ao Game Campos Minado', 'red')
    cprint('=============================', 'red')
    print()
    print('Espero que goste dessa aventura')


    # Sets up the game.
    def reset():
        print('''
MENU
=========

-> Para saber instruções, digite 'I'
-> Para jogar imediatamente, digite 'P'
'''
        )

        choice = input('Digite: ').upper()

        if choice == 'I':
            replit.clear()

            # Prints instructions.
            print(open('instructions.txt', 'r').read())

            input('Aperte [enter] para jogar!. ')

        elif choice != 'P':
            replit.clear()
            reset()

        # The solution grid.
        b = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        for n in range(0, 10):
            cm.placeBomb(b)

        for r in range(0, 9):
            for c in range(0, 9):
                value = cm.l(r, c, b)
                if value == '*':
                    cm.updateValues(r, c, b)

        # Sets the variable k to a grid of blank spaces, because nothing is yet known about the grid.
        k = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

        cm.printBoard(k)

        # Start timer
        startTime = time.time()

        # The game begins!
        play(b, k, startTime)

    reset()
