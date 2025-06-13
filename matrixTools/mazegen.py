import numpy as np
import random

dirrs2X = [(-2, 0), (2, 0), (0, 2), (0, -2)]
dirrDiag = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
PATH = 255
WALL = 69
NONE = 0


def isWithinBorders(pos, mazeShape):
    if pos[0] < mazeShape[0] and pos[1] < mazeShape[1] and pos[0] >= 0 and pos[1] >= 0:
        return True


def numOfBorders(pos, maze):
    numOfEmpty = 0
    if maze[pos[0], pos[1]] != NONE:
        for addY, addX in dirrs2X:
            inBorders = isWithinBorders(
                (pos[0] + int(addY / 2), pos[1] + int(addX / 2)), maze.shape
            )
            if inBorders:
                if maze[pos[0] + int(addY / 2), pos[1] + int(addX / 2)] == NONE:
                    numOfEmpty += 1
            elif maze[pos[0], pos[1]] != NONE:
                numOfEmpty += 1
    return numOfEmpty


def createMaze(graf2x1, dfsStart, seed=1):
    random.seed(seed)
    pathMaze = np.array(graf2x1)

    random.shuffle(dirrs2X)

    pointsToExplore = [(dfsStart, dirrs2X[0][0], dirrs2X[0][1])]

    while len(pointsToExplore) > 0:
        random.shuffle(dirrs2X)
        currentPos, moveY, moveX = pointsToExplore.pop()
        newPos = (currentPos[0] + moveY, currentPos[1] + moveX)

        for addY, addX in dirrs2X:
            nextPos = (newPos[0] + addY, newPos[1] + addX)
            if (
                isWithinBorders(nextPos, pathMaze.shape)
                and pathMaze[nextPos[0], nextPos[1]] == WALL
            ):
                pointsToExplore.append((newPos, addY, addX))

        if pathMaze[newPos[0], newPos[1]] == WALL:
            pathMaze[newPos[0], newPos[1]] = PATH
            pathMaze[int(currentPos[0] + moveY / 2), int(currentPos[1] + moveX / 2)] = (
                PATH
            )

    return pathMaze


def checkIsPathWall(tempPoint, wallLocations, maze):
    return (
        tempPoint not in wallLocations
        and isWithinBorders(tempPoint, maze.shape)
        and numOfBorders(tempPoint, maze) == 1
    )


def getBorderWalls(maze):
    mazeWidth = maze.shape[1]
    wallLocations = []
    addX = 0
    if int((mazeWidth - 1) / 2) % 2 == 0:
        addX = 1
    firstWallY = 0
    while maze[firstWallY, int(mazeWidth / 2) + addX] == NONE:
        firstWallY += 1
    startPoint = (firstWallY, int(mazeWidth / 2) + addX)
    currentPoint = startPoint
    wallLocations.append(startPoint)

    while True:
        pointAdded = False
        for add in dirrs2X:
            tempPoint = (currentPoint[0] + add[0], currentPoint[1] + add[1])
            midPoint = (
                currentPoint[0] + int(add[0] / 2),
                currentPoint[1] + int(add[1] / 2),
            )
            if (
                checkIsPathWall(tempPoint, wallLocations, maze)
                and maze[midPoint[0], midPoint[1]] == WALL
            ):
                currentPoint = tempPoint
                wallLocations.append(tempPoint)
                pointAdded = True
                break
        if not pointAdded:
            for add in dirrDiag:
                tempPoint = (currentPoint[0] + add[0], currentPoint[1] + add[1])
                if checkIsPathWall(tempPoint, wallLocations, maze):
                    currentPoint = tempPoint
                    wallLocations.append(tempPoint)
                    pointAdded = True
                    break
        if not pointAdded:
            break

    return wallLocations
