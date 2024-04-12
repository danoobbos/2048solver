from random import choice

class board2048():

    def __init__(self) -> None:
        self.directions = {
            'up':(-1, 1),
            'down':(1, 1),
            'right':(1, 0),
            'left':(-1, 0)
        }

        self.board = [
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0
        ]

    def newBlock(self):
        indecies = []
        for i, j in enumerate(self.board):
            if j == 0:
                indecies.append(i)

        if len(indecies) == 0:
            return
        
        self.board[choice(indecies)] = choice((1, 2))

    def printBoard(self):
        print('\n')
        cleanboard = self.board.copy()
        boardstr = ''
        for i in range(len(cleanboard)):
            if cleanboard[i] == 0:
                cleanboard[i] = '_'
            boardstr = boardstr + str(cleanboard[i])
        for i in range(4):
            print(boardstr[i*4:i*4+4])
        print('\n')

    def getIndex(self, cord:tuple[int, int]):
        index = 4*cord[1] + cord[0]
        if index >= 0 and index <= 15 and isinstance(index, int):
            return index
        return None
    
    def slide(self, direction):
        directionTuple = self.directions[direction]
        startingCord = int((directionTuple[0]*1.5)+1.5)
        cordList = [[0, 0], [1, 1], [2, 2], [3, 3]]

        latestEmptyList = [-1, -1, -1, -1]

        for i in cordList:
            i[directionTuple[1]] = startingCord
        
        for i in range(4):
            for j in range(4):
                if latestEmptyList[j] != -1 and self.board[self.getIndex(cordList[j])] != 0:
                    self.board[self.getIndex(latestEmptyList[j])] = self.board[self.getIndex(cordList[j])]
                    self.board[self.getIndex(cordList[j])] = 0

                    latestEmptyList[j][directionTuple[1]] += directionTuple[0]*-1

                if latestEmptyList[j] == -1 and self.board[self.getIndex(cordList[j])] == 0:
                    latestEmptyList[j] = cordList[j].copy()
                
                cordList[j][directionTuple[1]] += directionTuple[0]*-1
    
    def merge(self, direction):
        directionTuple = self.directions[direction]
        startingCord = int((directionTuple[0]*1.5)+1.5)
        cordList = [[0, 0], [1, 1], [2, 2], [3, 3]]

        for i in cordList:
            i[directionTuple[1]] = startingCord
        
        for i in range(3):
            for j in range(4):
                lookCord = cordList[j].copy()
                lookCord[directionTuple[1]] += directionTuple[0]*-1
                workingValues = [self.board[self.getIndex(cordList[j])], self.board[self.getIndex(lookCord)]]
                if workingValues[0] != 0 and workingValues[1] == workingValues[0]:
                    print(f'got here {workingValues}')
                    self.board[self.getIndex(cordList[j])] = int(workingValues[1])+1
                    self.board[self.getIndex(lookCord)] = 0
                
                cordList[j] = lookCord
    
    def play(self, direction):
        self.slide(direction)
        self.merge(direction)
        self.slide(direction)
        self.newBlock()

board2048_1 = board2048()
board2048_1.newBlock()
board2048_1.printBoard()
while True:
    inp = input('>>')
    if not inp in ('w', 'a', 's', 'd'):
        break
    dire = {'w':'up', 'a':'left', 's':'down', 'd':'right'}[inp]
    board2048_1.play(dire)
    board2048_1.printBoard()