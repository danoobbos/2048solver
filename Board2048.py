'''
Simple Interface for 2048 Python
-PaiShoFish49
'''

from math import log2, log10, floor
from random import choice

class Board2048():
    '''
    ### Class for a 2048 board.
    it can be any width and any height but the defalut is 4 x 4  
    the data at each cell is stored as log2(x) where x is the value it would be in default 2048  
    for example if a normal 2048 board had 64, this would have 6, merging a 4 and a 4 would give a 5, etc  
    when you see "exp", that refers to the exponent form. Board2048.exp(4) -> 16.  
    cordinates start from the top left and go down and right, like reading. the space in the top left has a cordinate of (0, 0).  
    the x (horizontal) cordinate always comes first, followed by the y (vertical).  
    direction can be "up", "down", "left", or "right".
    '''

    Cordinate = tuple[int, int]
    directions = ['up', 'down', 'left', 'right']
    inverseDirections = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    directionPathSettings = {'up': (0, False), 'down': (3, False), 'left': (0, True), 'right': (3, True)}
    directionTranslation = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}

    newTileTable = ((1, ) * 9) + (2, )

    @staticmethod
    def exp(value: int) -> int:
        if value == 0:
            return 0
        return 2**value

    @staticmethod
    def reverseExp(value: int) -> int:
        if value == 0:
            return 0
        return log2(value)

    @staticmethod
    def getDigits(value: int) -> int:
        if value == 0:
            return 1
        return floor(log10(value)) + 1

    def __init__(self, width: int = 4, height: int = 4) -> None:
        self.board: list[int] = [0] * (width * height)
        self.width: int = width
        self.height: int = height

        self.placeRandom(1)
        self.placeRandom(2)

    def __str__(self) -> str:
        maxDigits = 0
        for i in self.board:
            num = Board2048.exp(i)
            digits = Board2048.getDigits(num)
            if digits > maxDigits:
                maxDigits = digits

        sepString = f'+{('-' + ('-' * maxDigits) + '-' + '+') * self.width}'
        returnString = f'\n\n{sepString}\n'

        for i in range(self.height):
            returnString += '|'
            for j in range(self.width):
                val = self.getValueAtCord((j, i), True)
                val = ' ' if val == 0 else str(val)

                returnString += ' ' + val.rjust(maxDigits, ' ') + ' '
                returnString += '|'

            returnString += f'\n{sepString}\n'

        returnString += '\n'
        return returnString

    def cord2Index(self, cord: Cordinate) -> int:
        return (cord[1] * self.width) + cord[0]

    def isCordOnBoard(self, cord: Cordinate) -> bool:
        if not isinstance(cord, tuple):
            return False

        if len(cord) != 2:
            return False

        if not (isinstance(cord[0], int) and isinstance(cord[1], int)):
            return False

        if not (0 <= cord[0] < self.width):
            return False

        if not (0 <= cord[1] < self.height):
            return False

        return True

    def getValueAtCord(self, cord: Cordinate, exp: bool = False) -> int:
        value = self.board[self.cord2Index(cord)]
        if exp:
            return Board2048.exp(value)
        return value

    def putValueAtCord(self, cord: Cordinate, value: int, exp: bool = False) -> None:
        if exp:
            self.board[self.cord2Index(cord)] = Board2048.reverseExp(value)
        else:
            self.board[self.cord2Index(cord)] = value

    def getPathIterable(self, startingCorner: int, verticalFirst: bool) -> list[Cordinate]:
        '''
        returns an iterable of cordinates that follow the specified path.  
        starting corner is an interger 0-3 where 0 is top-left, 1 is top-right, 2 is bottom-left, and 3 is bottom-right.  
        verticalFirst is a boolean of if the iterable should go vertically first or not.  
        if its true, it might produce [(0, 0), (0, 1), (0, 2), ...], if its false it would produce [(0, 0), (1, 0), (2, 0), ...]
        '''

        step = {
            0: (1, 1),
            1: (-1, 1),
            2: (-1, 1),
            3: (-1, -1)
        }[startingCorner]

        firstSize = self.height if verticalFirst else self.width
        secondSize = self.width if verticalFirst else self.height

        firstReverse = step[1] if verticalFirst else step[0]
        secondReverse = step[0] if verticalFirst else step[1]

        iterable = []
        first = list(range(firstSize))[::firstReverse]
        second = list(range(secondSize))[::secondReverse]
        for s in second:
            for f in first:
                if verticalFirst:
                    iterable.append((s, f))
                else:
                    iterable.append((f, s))

        return iterable

    def switch(self, cord1: Cordinate, cord2: Cordinate) -> None:
        temp = self.getValueAtCord(cord1)
        self.putValueAtCord(cord1, self.getValueAtCord(cord2))
        self.putValueAtCord(cord2, temp)

    def slideOne(self, cord: Cordinate, direction: str) -> None:
        translate = Board2048.directionTranslation[direction]
        if self.getValueAtCord(cord) == 0:
            return

        nextCord = cord
        while True:
            curCord = nextCord
            nextCord = (curCord[0] + translate[0], curCord[1] + translate[1])

            if (self.isCordOnBoard(nextCord)) and (self.getValueAtCord(nextCord) == 0):
                self.switch(curCord, nextCord)
            else:
                break

    def slide(self, direction: str) -> None:
        pathSettings = Board2048.directionPathSettings[direction]
        path = self.getPathIterable(*pathSettings)

        for i in path:
            self.slideOne(i, direction)

    def merge(self, direction: str) -> None:
        pathSettings = Board2048.directionPathSettings[direction]
        path = self.getPathIterable(*pathSettings)
        translate = Board2048.directionTranslation[Board2048.inverseDirections[direction]]

        for i in path:
            currentCordValue = self.getValueAtCord(i)
            if currentCordValue != 0:
                nextCord = (i[0] + translate[0], i[1] + translate[1])
                if self.isCordOnBoard(nextCord):
                    if currentCordValue == self.getValueAtCord(nextCord):
                        self.putValueAtCord(i, currentCordValue+1)
                        self.putValueAtCord(nextCord, 0)

    def placeRandom(self, value: int | None = None):
        allZeros = []
        for i in self.getPathIterable(0, False):
            if self.getValueAtCord(i) == 0:
                allZeros.append(i)

        square = choice(allZeros)
        if value == None:
            self.putValueAtCord(square, choice(Board2048.newTileTable))
        else:
            self.putValueAtCord(square, value)

    def move(self, direction: str) -> None:
        self.slide(direction)
        self.merge(direction)
        self.slide(direction)
        self.placeRandom()

if __name__ == '__main__':
    b = Board2048()
    import keyboard
    print(b)

    while True:
        e = keyboard.read_event()
        if e.event_type != 'up':
            continue

        k = e.name

        if k in 'wasd':
            b.move({
                'w': 'up',
                's': 'down',
                'a': 'left',
                'd': 'right'
            }[k])

            print(b)
        else:
            break