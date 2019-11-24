import random, copy, replit
import rpyc
from rpyc import ThreadedServer


class CampoMinado(rpyc.Service):

    # Gets the value of a coordinate on the grid.
    def exposed_l(self, r, c, b):
        return b[r][c]


    # Places a bomb in a random location.
    def exposed_placeBomb(self, b):
        r = random.randint(0, 8)
        c = random.randint(0, 8)
        # Checks if there's a bomb in the randomly generated location. If not, it puts one there. If there is, it requests a new location to try.
        currentRow = b[r]
        if not currentRow[c] == '*':
            currentRow[c] = '*'
        else:
            self.placeBomb(b)


    # Adds 1 to all of the squares around a bomb.
    def exposed_updateValues(self, rn, c, b):
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
    def exposed_checkZeros(self, k, b, r, c):
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
    def exposed_marker(self, r, c, k):
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


def server():
    t = ThreadedServer(CampoMinado, port=18861)
    t.start()