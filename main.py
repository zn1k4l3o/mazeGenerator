from PIL import Image
from matrixTools.imgshape import getShapeFromImage
from matrixTools.mazegen import createMaze, getBorderWalls
from matrixTools.mazesvg import mazeToSVG
from matrixTools.mazesolve import solveBFS

def main():
    img = Image.open('mazeGenerator/test_images/4.jpg')
    imageMatrix, mazeMatrix = getShapeFromImage(img, 0.07)
    #print(imageMatrix.shape)
    addYX = [0,0]
    if (imageMatrix.shape[0] % 2 == 0):
        addYX[0] = 1
    if (imageMatrix.shape[1] % 2 == 0):
        addYX[1] = 1
    dfsStart = (imageMatrix.shape[0] + addYX[0], imageMatrix.shape[1] + addYX[1])
    maze = createMaze(mazeMatrix, dfsStart, seed=69)
    #ne intuitivno
    #dva slidera za start i end - 0-100%, 0-360
    walls = getBorderWalls(maze)
    startValue = 0
    endValue = int(len(walls)/2)
    maze[walls[startValue]] = 255
    maze[walls[endValue]] = 255

    mazeSolution = solveBFS(maze, walls[startValue], walls[endValue])
    #print(mazeSolutionCoords)
    
    for i in range(len(mazeSolution)):
        line = mazeSolution[i]
        out = ''
        for ti in range(len(line)):
            tile = mazeSolution[i, ti]
            if (tile == 69):
                out += "X"
            elif (tile == 255):
                out += "."
            elif (tile == 3):
                out += '#'
            else:
                out += ' '
        print(out)


    svgMaze = mazeToSVG(mazeSolution, 20, 3, "#ef22ee", "#009999")
    with open("result.svg", "w") as f:
        f.write(svgMaze.as_str())
    print(maze.shape)

                
main()