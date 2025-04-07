import numpy as np
import random

def isWithinBorders(pos, mazeShape):
    if pos[0] < mazeShape[0] and pos[1] < mazeShape[1] and pos[0] >= 0 and pos[1] >= 0:
        return True

def createMaze(graf2x1, dfsStart, seed = 1):
    dirrs = [(-2, 0), (2, 0), (0, 2), (0, -2)]
    PATH = 255
    WALL = 69
    NONE = 0
    random.seed(seed)
    pathMaze = np.array(graf2x1)

    random.shuffle(dirrs)
    currentPos = dfsStart

    pointsToExplore = []

    for addY, addX in dirrs:
        nextPos = (currentPos[0] + addY, currentPos[1] + addX)
        if (isWithinBorders(nextPos, pathMaze.shape) and pathMaze[nextPos[0], nextPos[1]] == WALL):
            pointsToExplore.append((currentPos, addY, addX))
    pathMaze[currentPos[0], currentPos[1]] = PATH
    
    while len(pointsToExplore) > 0:
        random.shuffle(dirrs)
        currentPos, moveY, moveX = pointsToExplore.pop()
        #print(currentPos, moveY, moveX)
        newPos = (currentPos[0] + moveY, currentPos[1] + moveX)

        for addY, addX in dirrs:
            nextPos = (newPos[0] + addY, newPos[1] + addX)
            if (isWithinBorders(nextPos, pathMaze.shape) and pathMaze[nextPos[0], nextPos[1]] == WALL):
                pointsToExplore.append((newPos, addY, addX))

        if (pathMaze[newPos[0], newPos[1]] == WALL):
            pathMaze[newPos[0], newPos[1]] = PATH
            pathMaze[int(currentPos[0]+moveY/2), int(currentPos[1]+moveX/2)] = PATH

    return pathMaze

        
        


