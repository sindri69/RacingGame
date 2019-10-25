import random

def ballMovement(maze, speed, ori, posX, posZ): # makes the ball move around the maze semi-randomly
    moves = []
    if ori == "north":
        if posZ != maze.size - 1:
            if maze.cells[posX][posZ + 1].south: moves.append("north") 
        if maze.cells[posX][posZ].west: moves.append("west") 
        if posX != maze.size - 1:
            if maze.cells[posX + 1][posZ].west: moves.append("east") 
    elif ori == "south":
        if maze.cells[posX][posZ].south: moves.append("south") 
        if maze.cells[posX][posZ].west: moves.append("west") 
        if posX != maze.size - 1:
            if maze.cells[posX + 1][posZ].west: moves.append("east") 
    elif ori == "east":
        if posZ != maze.size - 1:
            if maze.cells[posX][posZ + 1].south: moves.append("north") 
        if posX != maze.size - 1:
            if maze.cells[posX + 1][posZ].west: moves.append("east") 
        if maze.cells[posX][posZ].south: moves.append("south") 
    elif ori == "west":
        if posZ != maze.size - 1:
            if maze.cells[posX][posZ + 1].south: moves.append("north") 
        if maze.cells[posX][posZ].south: moves.append("south") 
        if maze.cells[posX][posZ].west: moves.append("west") 
    if not moves:
        if ori == "north": ori = "south"
        if ori == "south": ori = "north"
        if ori == "west": ori = "east"
        if ori == "east": ori = "west"
    else: ori = random.choice(moves)
    time = speed / 3.0
    return (time, ori)