import random, time, copy, replit
from termcolor import cprint

#Introduction
print()
cprint('Bem-vindo ao Game Campos Minado', 'red')
cprint('=============================', 'red')
print()
print('Espero que goste dessa aventura')


#Sets up the game.
def reset():
    print('''
MENU
=========

-> Para saber instruções, digite 'I'
-> Para jogar imediatamente, digite 'P'
''')

    choice = input('Digite: ').upper()

    if choice == 'I':
        replit.clear()

        #Prints instructions.
        print(open('instructions.txt', 'r').read())

        input('Aperte [enter] para jogar!. ')
        
    elif choice != 'P':
        replit.clear()
        reset()

    #The solution grid.
    b = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    for n in range (0, 10):
        placeBomb(b)

    for r in range (0, 9):
        for c in range (0, 9):
            value = l(r, c, b)
            if value == '*':
                updateValues(r, c, b)

    #Sets the variable k to a grid of blank spaces, because nothing is yet known about the grid.
    k = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

    printBoard(k)

    #Start timer
    startTime = time.time()

    #The game begins!
    play(b, k, startTime)

#Gets the value of a coordinate on the grid.
def l(r, c, b):
    return b[r][c]

#Places a bomb in a random location.
def placeBomb(b):
    r = random.randint(0, 8)
    c = random.randint(0, 8)
    #Checks if there's a bomb in the randomly generated location. If not, it puts one there. If there is, it requests a new location to try.
    currentRow = b[r]
    if not currentRow[c] == '*':
        currentRow[c] = '*'
    else:
        placeBomb(b)

#Adds 1 to all of the squares around a bomb.
def updateValues(rn, c, b):

    #Row above.
    if rn-1 > -1:
        r = b[rn-1]
        
        if c-1 > -1:
            if not r[c-1] == '*':
                r[c-1] += 1

        if not r[c] == '*':
            r[c] += 1

        if 9 > c+1:
            if not r[c+1] == '*':
                r[c+1] += 1

    #Same row.    
    r = b[rn]

    if c-1 > -1:
        if not r[c-1] == '*':
            r[c-1] += 1

    if 9 > c+1:
        if not r[c+1] == '*':
            r[c+1] += 1

    #Row below.
    if 9 > rn+1:
        r = b[rn+1]

        if c-1 > -1:
            if not r[c-1] == '*':
                r[c-1] += 1

        if not r[c] == '*':
            r[c] += 1

        if 9 > c+1:
            if not r[c+1] == '*':
                r[c+1] += 1

#When a zero is found, all the squares around it are opened.
def zeroProcedure(r, c, k, b):

    #Row above
    if r-1 > -1:
        row = k[r-1]
        if c-1 > -1: row[c-1] = l(r-1, c-1, b)
        row[c] = l(r-1, c, b)
        if 9 > c+1: row[c+1] = l(r-1, c+1, b)

    #Same row
    row = k[r]
    if c-1 > -1: row[c-1] = l(r, c-1, b)
    if 9 > c+1: row[c+1] = l(r, c+1, b)

    #Row below
    if 9 > r+1:
        row = k[r+1]
        if c-1 > -1: row[c-1] = l(r+1, c-1, b)
        row[c] = l(r+1, c, b)
        if 9 > c+1: row[c+1] = l(r+1, c+1, b)

#Checks known grid for 0s.
def checkZeros(k, b, r, c):
    oldGrid = copy.deepcopy(k)
    zeroProcedure(r, c, k, b)
    if oldGrid == k:
        return
    while True:
        oldGrid = copy.deepcopy(k)
        for x in range (9):
            for y in range (9):
                if l(x, y, k) == 0:
                    zeroProcedure(x, y, k, b)
        if oldGrid == k:
            return

#Places a marker in the given location.
def marker(r, c, k):
    k[r][c] = '⚐'
    printBoard(k)

#Prints the given board.
def printBoard(b):
    replit.clear()
    print('    A   B   C   D   E   F   G   H   I')
    print('  ╔═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╦═══╗')
    for r in range (0, 9):
        print(r,'║',l(r,0,b),'║',l(r,1,b),'║',l(r,2,b),'║',l(r,3,b),'║',l(r,4,b),'║',l(r,5,b),'║',l(r,6,b),'║',l(r,7,b),'║',l(r,8,b),'║')
        if not r == 8:
            print('  ╠═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╬═══╣')
    print('  ╚═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╩═══╝')

#The player chooses a location.
def choose(b, k, startTime):
    #Variables 'n stuff.
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h' ,'i']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
    #Loop in case of invalid entry.
    while True:
        chosen = input('Escolha o quadrado (ex. E4) ou marque caso ache que exista bomba (ex. mE4): ').lower()
        #Checks for valid square.
        if len(chosen) == 3 and chosen[0] == 'm' and chosen[1] in letters and chosen[2] in numbers:
            c, r = (ord(chosen[1]))-97, int(chosen[2])
            marker(r, c, k)
            play(b, k, startTime)
            break
        elif len(chosen) == 2 and chosen[0] in letters and chosen[1] in numbers: return (ord(chosen[0]))-97, int(chosen[1])
        else: choose(b, k, startTime)    


#The majority of the gameplay happens here.
def play(b, k, startTime):
    #Player chooses square.
    c, r = choose(b, k, startTime)
    #Gets the value at that location.
    v = l(r, c, b)
    #If you hit a bomb, it ends the game.
    if v == '*':
        printBoard(b)
        print('Você Perdeu!')
        #Print timer result.
        print('Tempo: ' + str(round(time.time() - startTime)) + 's')
        #Offer to play again.
        playAgain = input('Jogar Novamente? (Y/N): ').lower()
        if playAgain == 'y':
            replit.clear()
            reset()
        else:
            quit()
    #Puts that value into the known grid (k).
    k[r][c] = v
    #Runs checkZeros() if that value is a 0.
    if v == 0:
        checkZeros(k, b, r, c)
    printBoard(k)
    #Checks to see if you have won.
    squaresLeft = 0
    for x in range (0, 9):
        row = k[x]
        squaresLeft += row.count(' ')
        squaresLeft += row.count('⚐')
    if squaresLeft == 10:
        printBoard(b)
        print('Voce Venceu!')
        #Print timer result.
        print('Tempo: ' + str(round(time.time() - startTime)) + 's')
        #Offer to play again.
        playAgain = input('Jogar Novamente? (Y/N): ')
        playAgain = playAgain.lower()
        if playAgain == 'y':
            replit.clear()
            reset()
        else:
            quit()
    #Repeats!
    play(b, k, startTime)
