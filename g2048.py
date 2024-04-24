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

    def printBoard(self, board = -1):
        if board == -1:
            board = self.board.copy()
        print('\n')
        cleanboard = board.copy()
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

    def slide(self, direction, board):
        directionTuple = self.directions[direction]
        startingCord = int((directionTuple[0]*1.5)+1.5)
        cordList = [[0, 0], [1, 1], [2, 2], [3, 3]]

        latestEmptyList = [-1, -1, -1, -1]

        for i in cordList:
            i[directionTuple[1]] = startingCord

        for i in range(4):
            for j in range(4):
                if latestEmptyList[j] != -1 and board[self.getIndex(cordList[j])] != 0:
                    board[self.getIndex(latestEmptyList[j])] = board[self.getIndex(cordList[j])]
                    board[self.getIndex(cordList[j])] = 0

                    latestEmptyList[j][directionTuple[1]] += directionTuple[0]*-1

                if latestEmptyList[j] == -1 and board[self.getIndex(cordList[j])] == 0:
                    latestEmptyList[j] = cordList[j].copy()

                cordList[j][directionTuple[1]] += directionTuple[0]*-1
        return board

    def merge(self, direction, board):
        directionTuple = self.directions[direction]
        startingCord = int((directionTuple[0]*1.5)+1.5)
        cordList = [[0, 0], [1, 1], [2, 2], [3, 3]]

        for i in cordList:
            i[directionTuple[1]] = startingCord

        for i in range(3):
            for j in range(4):
                lookCord = cordList[j].copy()
                lookCord[directionTuple[1]] += directionTuple[0]*-1
                workingValues = [board[self.getIndex(cordList[j])], board[self.getIndex(lookCord)]]
                if workingValues[0] != 0 and workingValues[1] == workingValues[0]:
                    board[self.getIndex(cordList[j])] = int(workingValues[1])+1
                    board[self.getIndex(lookCord)] = 0

                cordList[j] = lookCord
        return board

    def recursiveFloodSearch(self, board, index, restrictedIndecies):
        restrictedIndecies.append(index)
        count = 1

        cord = (index % 4, index // 4)
        searchCords = [(cord[0]+1, cord[1]), (cord[0]-1, cord[1]), (cord[0], cord[1]+1), (cord[0], cord[1]-1)]

        temp = []
        for i in searchCords:
            if -1 < i[0] < 4 and -1 < i[1] < 4:
                temp.append(i)
        searchCords = temp

        lookNum = board[index]
        for i in searchCords:
            searchIndex = self.getIndex(i)
            if searchIndex in restrictedIndecies:
                continue

            if board[searchIndex] == lookNum:
                count += self.recursiveFloodSearch(board, searchIndex, restrictedIndecies)

        return count

    def getBoardScore(self, direction):
        tempBoard = self.board.copy()

        if direction in ('up', 'down', 'left', 'right'):
            self.slide(direction, tempBoard)
            self.merge(direction, tempBoard)
            self.slide(direction, tempBoard)

        #highest value
        highestValue = max(tempBoard)

        #least filled spaces
        minimizeFilledSpaces = tempBoard.count(0)

        #most number of touching
        restrictedIndecies = []
        completeMatches = []
        for i in range(len(tempBoard)):
            if tempBoard[i] == 0 or i in restrictedIndecies:
                continue

            count = self.recursiveFloodSearch(tempBoard, i, restrictedIndecies)

            completeMatches.append((tempBoard[i], count))

        maximizeTouchingValue = 0
        for i in completeMatches:
            maximizeTouchingValue += (i[0] * (i[1] - 1))

        #bonus
        sortedTableKey = tempBoard.copy()
        sortedTableKey.sort(reverse=True)

        bonusOrder = [15, 14, 13, 12, 8, 9, 10, 11, 7, 6, 5, 4, 0, 1, 2, 3]
        bonus = 0
        for i in range(len(bonusOrder)):
            if tempBoard[bonusOrder[i]] == sortedTableKey[i]:
                bonus += tempBoard[bonusOrder[i]]
            else:
                break

        #total score
        return (highestValue*3, minimizeFilledSpaces, maximizeTouchingValue, bonus, highestValue*3+maximizeTouchingValue+bonus+maximizeTouchingValue)

    def lineOfSight(self, starterIndex, finderIndex):
        starterCord = (starterIndex % 4, starterIndex // 4)
        finderCord = (finderIndex % 4, finderIndex // 4)

        if starterCord[0] == finderCord[0]:
            aligned = True
            cordDistance = starterCord[1] - finderCord[1]
            cordIter = int(cordDistance / abs(cordDistance))
            cordDistance = abs(cordDistance)
            print(cordDistance, '   ', cordIter)

            for i in range(cordDistance-1):
                if self.board[self.getIndex((starterCord[0], starterCord[1] - (i+1) * cordIter))] != 0:
                    aligned = False
                    break

            if aligned:
                return 0, cordIter

        if starterCord[1] == finderCord[1]:
            aligned = True
            cordDistance = starterCord[0] - finderCord[0]
            cordIter = int(cordDistance / abs(cordDistance))
            cordDistance = abs(cordDistance)
            print(cordDistance, '   ', cordIter)

            for i in range(cordDistance - 1):
                if self.board[self.getIndex((starterCord[0], starterCord[0] - (i+1) * cordIter))] != 0:
                    aligned = False
                    break

            if aligned:
                return 1, cordIter

        return False

    def generateNextMove(self):
        priorityOrder = {
            15:('up'),
            14:('right'),
            13:('right'),
            12:('right'),
            8:('down'),
            9:('left'),
            10:('left'),
            11:('left'),
            7:('down'),
            6:('right'),
            5:('right'),
            4:('right'),
            0:('down'),
            1:('left'),
            2:('left'),
            3:('left')
        }

        currentTileValue = 100
        for i, j in enumerate(priorityOrder.keys()):
            lastTileValue = currentTileValue
            currentTileValue = self.board[j]

            if currentTileValue == 0:
                return 'joemama'

            if currentTileValue == lastTileValue:
                return priorityOrder[j]

            if self.board.count(self.board[j]) > 1:
                matchBoard = []
                for k, l in enumerate(self.board):
                    if l == self.board[j] and k != j:
                        matchBoard.append((l, k))
                print(matchBoard)

                for i in matchBoard:
                    los = self.lineOfSight(j, i[1])

                    if los != False:
                        return {(0, 1):'down', (0, -1):'up', (1, -1):'left', (1, 1): 'right'}[los]
        return 'joemama'

    def play(self, direction):
        self.slide(direction, self.board)
        self.merge(direction, self.board)
        self.slide(direction, self.board)
        self.newBlock()

if __name__ == '__main__':
    board2048_1 = board2048()
    board2048_1.newBlock()
    board2048_1.printBoard()
    while True:
        inp = input('>>')

        if not inp in ('w', 'a', 's', 'd', 'p', 'x'):
            break

        if inp == 'p':
            print(board2048_1.getBoardScore('a'))

        elif inp == 'x':
            bestPlay = ['', 0, ()]
            for i in ('down', 'right', 'left', 'up'):
                playValue = board2048_1.getBoardScore(i)
                if playValue[4] > bestPlay[1]:
                    bestPlay = [i, playValue[4], playValue]
            board2048_1.play(bestPlay[0])
            board2048_1.printBoard()
            print(bestPlay)

        else:
            dire = {'w':'up', 'a':'left', 's':'down', 'd':'right'}[inp]
            board2048_1.play(dire)
            board2048_1.printBoard()
            print(board2048_1.generateNextMove())