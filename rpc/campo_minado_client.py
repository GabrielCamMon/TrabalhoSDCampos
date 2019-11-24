import rpyc as rpyc
import time, replit

from termcolor import cprint


def client():

    config = {'allow_public_attrs': True}
    cm = rpyc.connect('localhost', 18861, config=config)
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
                cm.root.marker(r, c, k)
                play(b, k, startTime)
                break
            elif len(chosen) == 2 and chosen[0] in letters and chosen[1] in numbers:
                return (ord(chosen[0])) - 97, int(chosen[1])
            else:
                choose(b, k, startTime)

        # The majority of the gameplay happens here.

    def printBoard(b):
        replit.clear()
        print('    A   B   C   D   E   F   G   H   I')
        print('  ╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗')
        for r in range(0, 9):
            print(r, '║', cm.root.l(r, 0, b), '║', cm.root.l(r, 1, b), '║', cm.root.l(r, 2, b), '║', cm.root.l(r, 3, b), '║',
                  cm.root.l(r, 4, b), '║', cm.root.l(r, 5, b),
                  '║', cm.root.l(r, 6, b), '║', cm.root.l(r, 7, b), '║', cm.root.l(r, 8, b), '║')
            if not r == 8:
                print('  ╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣')
        print('  ╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝')


    def play(b, k, startTime):
        # Player chooses square.
        c, r = choose(b, k, startTime)
        # Gets the value at that location.
        v = cm.root.l(r, c, b)
        # If you hit a bomb, it ends the game.
        if v == '*':
            printBoard(b)
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
            cm.root.checkZeros(k, b, r, c)
        printBoard(k)
        # Checks to see if you have won.
        squaresLeft = 0
        for x in range(0, 9):
            row = k[x]
            squaresLeft += row.count(' ')
            squaresLeft += row.count('⚐')
        if squaresLeft == 10:
            printBoard(b)
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
            cm.root.placeBomb(b)

        for r in range(0, 9):
            for c in range(0, 9):
                value = cm.root.l(r, c, b)
                if value == '*':
                    cm.root.updateValues(r, c, b)

        # Sets the variable k to a grid of blank spaces, because nothing is yet known about the grid.
        k = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

        printBoard(k)

        # Start timer
        startTime = time.time()

        # The game begins!
        play(b, k, startTime)

    reset()
