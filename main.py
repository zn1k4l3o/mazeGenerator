from PIL import Image
from matrixTools.imgshape import getShapeFromImage
from matrixTools.mazegen import createMaze, getBorderWalls
from matrixTools.mazesvg import mazeToSVG

def main():
    img = Image.open('mazeGenerator/test_images/4.jpg')
    imageMatrix, mazeMatrix = getShapeFromImage(img, 0.11)
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
    walls = getBorderWalls(maze)
    startValue = 0
    endValue = int(len(walls)/2)
    maze[walls[startValue]] = 255
    maze[walls[endValue]] = 255

    for i in range(len(maze)):
        line = maze[i]
        out = ''
        for ti in range(len(line)):
            tile = maze[i, ti]
            if (tile == 69):
                out += "X"
            elif (tile == 255):
                out += "."
            else:
                out += ' '
        print(out)

    svgMaze = mazeToSVG(maze, 10)
    with open("result.svg", "w") as f:
        f.write(svgMaze.as_str())
    
                
main()