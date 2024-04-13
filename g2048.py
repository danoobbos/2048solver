from random import choice

class board2048():
    directions = {
        'up':(0, 1),
        'down':(0, -1),
        'right':(1, 0),
        'left':(-1, 0)
    }

    def __init__(self) -> None:
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
        self.board[choice(indecies)] = choice((1, 2))

    def printBoard(self):
        for i in range(4):
            print(self.board[i*4:i*4+4])

    def getIndex(self, cord:tuple[int, int]):
        index = 4*cord[1] + cord[0]
        if index >= 0 and index <= 15 and isinstance(index, int):
            return index
        return None

board2048_1 = board2048()
board2048_1.newBlock()
board2048_1.printBoard()
print(board2048_1.getIndex((1, 1)))