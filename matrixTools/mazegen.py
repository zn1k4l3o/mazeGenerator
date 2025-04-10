import numpy as np
import random

dirrs2X = [(-2, 0), (2, 0), (0, 2), (0, -2)]
dirrDiag = [(1,1),(1,-1),(-1,-1),(-1,1)]
PATH = 255
WALL = 69
NONE = 0

def isWithinBorders(pos, mazeShape):
    if pos[0] < mazeShape[0] and pos[1] < mazeShape[1] and pos[0] >= 0 and pos[1] >= 0:
        return True

def numOfBorders(pos, maze):
    numOfEmpty = 0
    if (maze[pos[0], pos[1]] != NONE):
        for addY, addX in dirrs2X:
            inBorders = isWithinBorders((pos[0]+int(addY/2), pos[1]+int(addX/2)), maze.shape)
            if (inBorders):
                if (maze[pos[0]+int(addY/2), pos[1]+int(addX/2)] == NONE):
                    numOfEmpty += 1
            elif (maze[pos[0], pos[1]] != NONE):
                numOfEmpty += 1
    return numOfEmpty
    
def createMaze(graf2x1, dfsStart, seed = 1):
    random.seed(seed)
    pathMaze = np.array(graf2x1)

    random.shuffle(dirrs2X)
    currentPos = dfsStart

    pointsToExplore = []

    for addY, addX in dirrs2X:
        nextPos = (currentPos[0] + addY, currentPos[1] + addX)
        if (isWithinBorders(nextPos, pathMaze.shape) and pathMaze[nextPos[0], nextPos[1]] == WALL):
            pointsToExplore.append((currentPos, addY, addX))
    pathMaze[currentPos[0], currentPos[1]] = PATH
    
    while len(pointsToExplore) > 0:
        random.shuffle(dirrs2X)
        currentPos, moveY, moveX = pointsToExplore.pop()
        #print(currentPos, moveY, moveX)
        newPos = (currentPos[0] + moveY, currentPos[1] + moveX)

        for addY, addX in dirrs2X:
            nextPos = (newPos[0] + addY, newPos[1] + addX)
            if (isWithinBorders(nextPos, pathMaze.shape) and pathMaze[nextPos[0], nextPos[1]] == WALL):
                pointsToExplore.append((newPos, addY, addX))

        if (pathMaze[newPos[0], newPos[1]] == WALL):
            pathMaze[newPos[0], newPos[1]] = PATH
            pathMaze[int(currentPos[0]+moveY/2), int(currentPos[1]+moveX/2)] = PATH

    return pathMaze

def findStartEnd(maze, startValue, endValue):
    seMaze = np.array(maze)


def getBorderWalls(maze):
    mazeWidth = maze.shape[1]
    tempMaze = np.array(maze)
    tempMaze[tempMaze > 0] = 1
    '''
    firstWallY = 0
    while maze[firstWallY, int(mazeWidth/2) + 1] == NONE:
        firstWallY += 1
    print(firstWallY)
    startPoint = (firstWallY, int(mazeWidth/2) + 1)
    '''

    height, width = maze.shape
    wallLocations = []

    '''
    wallLocations = []
    for y in range(height):
        for x in range(width):
            if (isBorder((y, x), maze) == 1):
                tempMaze[y, x] = 2
                wallLocations.append((y, x))
    '''

    firstWallY = 0
    while maze[firstWallY, int(mazeWidth/2) + 1] == NONE:
        firstWallY += 1
    print("firstwallY: ",firstWallY)
    addX = 0
    if (mazeWidth % 2 == 0):
        addX = 1
    startPoint = (firstWallY, int(mazeWidth/2) + addX)
    print("start",startPoint)
    currentPoint = startPoint
    wallLocations.append(startPoint)
    
    while True:
        pointAdded = False
        for add in dirrs2X:
            tempPoint = (currentPoint[0] + add[0], currentPoint[1] + add[1])
            midPoint = (currentPoint[0] + int(add[0]/2), currentPoint[1] + int(add[1]/2))
            if (tempPoint not in wallLocations 
                and isWithinBorders(tempPoint, maze.shape) 
                and numOfBorders(tempPoint, maze) == 1 
                and maze[midPoint] != NONE):
                currentPoint = tempPoint
                wallLocations.append(tempPoint)
                pointAdded = True
                break
        if (not pointAdded):
            for add in dirrDiag:
                tempPoint = (currentPoint[0] + add[0], currentPoint[1] + add[1])
                midPoint = (currentPoint[0] + int(add[0]/2), currentPoint[1] + int(add[1]/2))
                if (tempPoint not in wallLocations 
                    and isWithinBorders(tempPoint, maze.shape) 
                    and numOfBorders(tempPoint, maze) == 1 
                    and maze[midPoint] != NONE):
                    currentPoint = tempPoint
                    wallLocations.append(tempPoint)
                    pointAdded = True
                    break
        if (not pointAdded):
            break

    '''
    for line in tempMaze:
        out = ''
        for tile in line:
            if (tile == 1):
                out += '.'
            elif (tile == 2):
                out += 'X'
            else:
                out += ' '
        print(out)
    '''

    return wallLocations


