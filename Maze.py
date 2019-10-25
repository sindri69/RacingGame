import random

class Cell:
    def __init__(self):
        self.south = False
        self.west = False
        self.isVisited = False
    def setWest(self):
        self.west = True
    def setSouth(self):
        self.south = True
    def setVisited(self):
        self.isVisited = True

class Maze:
    def __init__(self, size): #randomly generates a maze with no cycles
        self.size = size
        self.cells = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(Cell())
            self.cells.append(row)
        count = 1
        stack = []
        posX = 0
        posY = 0
        while count < (size * size):
            #print(posX)
            # print(posY)
            #print(count)
            possibleMoves = []

            if (posX + 1) < size :
                if not self.cells[posX + 1][posY].isVisited:
                    possibleMoves.append("right")
            if 0 <= posX - 1:
                if not self.cells[posX - 1][posY].isVisited:
                    possibleMoves.append("left")
            if (posY + 1) < size:
                if not self.cells[posX][posY + 1].isVisited:
                    possibleMoves.append("up")
            if 0 <= posY - 1:
                if not self.cells[posX][posY - 1].isVisited:
                    possibleMoves.append("down")
            #for bla in possibleMoves:
                #print(bla)
            if not possibleMoves:
                #print("sjomli")
                if self.cells[posX][posY].isVisited == False:
                    self.cells[posX][posY].setVisited()
                    #count += 1
                if stack:
                    tmp = stack.pop()
                posX = tmp[0]
                posY = tmp[1]
            else:
                move = random.choice(possibleMoves)
                if move == "right":
                    self.cells[posX][posY].setVisited()
                    count += 1
                    stack.append((posX, posY))
                    posX += 1
                    self.cells[posX][posY].setWest()    
                elif move == "left":
                    self.cells[posX][posY].setVisited()
                    count += 1
                    stack.append((posX, posY))
                    self.cells[posX][posY].setWest()    
                    posX -= 1
                elif move == "up":
                    self.cells[posX][posY].setVisited()
                    count += 1
                    stack.append((posX, posY))
                    posY += 1
                    self.cells[posX][posY].setSouth()    
                elif move == "down":
                    self.cells[posX][posY].setVisited()
                    count += 1
                    stack.append((posX, posY))
                    self.cells[posX][posY].setSouth()    
                    posY -= 1
