from PIL import Image
from matrixTools.imgshape import getShapeFromImage
from matrixTools.mazegen import createMaze, getBorderWalls

def main():
    img = Image.open('mazeGenerator/test_images/10.jpg')
    imageMatrix, mazeMatrix = getShapeFromImage(img, 0.05)
    print(imageMatrix.shape)
    addYX = [0,0]
    if (imageMatrix.shape[0] % 2 == 0):
        addYX[0] = 1
    if (imageMatrix.shape[1] % 2 == 0):
        addYX[1] = 1
    dfsStart = (imageMatrix.shape[0] + addYX[0], imageMatrix.shape[1] + addYX[1])
    maze = createMaze(mazeMatrix, dfsStart)
    #ne intuitivno
    #dva slidera za start i end - 0-100%, 0-360
    walls = getBorderWalls(mazeMatrix)
    print(len(walls))
    startValue = 0
    endValue = int(len(walls)/2)
    #maze[walls[startValue][0]*2+1, walls[startValue][1]*2+1] = 1
    #maze[walls[endValue][0]*2+1, walls[endValue][1]*2+1] = 2

    for i in range(len(maze)):
        line = maze[i]
        out = ''
        for ti in range(len(line)):
            tile = maze[i, ti]
            if (walls[startValue] == (i, ti)):
                out += 'S'
            elif (walls[endValue] == (i, ti)):
                out += 'E'
            elif ((i, ti) in walls):
                out += "#"
            elif (tile == 69):
                out += "X"
            elif (tile == 255):
                out += "."
            else:
                out += ' '
        print(out)
                
main()