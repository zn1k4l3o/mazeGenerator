from PIL import Image, ImageChops
from matrixTools.imgshape import getShapeFromImage
from matrixTools.mazegen import createMaze, getBorderWalls
from matrixTools.mazesvg import mazeToSVG
from matrixTools.mazesolve import solveBFS
from flask import Flask, request, render_template, jsonify, send_file, Response
from io import BytesIO
import numpy as np 

app = Flask(__name__)

app.config['REMEMBERED_IMAGE'] = None
app.config['REMEMBERED_IMAGE']
app.config['REMEMBERED_MAZE'] = None
app.config['REMEMBERED_START_PERCENT'] = None
app.config['REMEMBERED_END_PERCENT'] = None
app.config['REMEMBERED_WALL_POSITIONS'] = None
app.config['REMEMBERED_SIZE_PERCENTAGE'] = None
app.config['REMEMBERED_SEED'] = None
app.config['REMEMBERED_MAZE_SOLUTION'] = None
app.config['REMEMBERED_CELL_SIZE'] = None
app.config['REMEMBERED_WALL_SIZE'] = None
app.config['REMEMBERED_SEED'] = None

def printMaze(maze):
    for i in range(len(maze)):
        line = maze[i]
        out = ''
        for ti in range(len(line)):
            tile = maze[i, ti]
            if (tile == 69):
                out += "X"
            elif (tile == 255):
                out += "."
            elif (tile == 3):
                out += '#'
            else:
                out += ' '
        print(out)

def main():
    '''
    img = Image.open('mazeGenerator/test_images/12.jpg')
    imageMatrix, mazeMatrix = getShapeFromImage(img, 0.07)
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


    svgMaze = mazeToSVG(mazeSolution, 20, 3, "#ef22ee", "#009999", showSolution=True)
    with open("result.svg", "w") as f:
        f.write(svgMaze.as_str())
    print(maze.shape)
    '''
    
def mazeGenerator(image = None,
                sizePercentage = None, 
                dfsOrigin = None, 
                startWallPercent = None, 
                endWallPercent = None, 
                cellWidth:int = None, 
                wallWidth:int = None, 
                wallColor ="#ef22ee", 
                solutionColor="#009999", 
                showSolution=False,
                seed=None):
    img, sizePrct = image, sizePercentage
    if (image == None):
        img = app.config["REMEMBERED_IMAGE"]
    if (sizePercentage == None):
        sizePrct = app.config['REMEMBERED_SIZE_PERCENTAGE']
    cellSize, wallSize = cellWidth, wallWidth
    if (cellSize == None):
        cellSize = app.config['REMEMBERED_CELL_SIZE']
    if (wallSize == None):
        wallSize = app.config['REMEMBERED_WALL_SIZE']
    endWallPercentValue, startWallPercentValue = endWallPercent, startWallPercent
    if (endWallPercentValue == None):
        endWallPercentValue = app.config['REMEMBERED_END_PERCENT']
    if (startWallPercentValue == None):
        startWallPercentValue = app.config['REMEMBERED_START_PERCENT']
    imageMatrix, mazeMatrix = getShapeFromImage(img, sizePrct)
    addYX = [0,0]
    if (imageMatrix.shape[0] % 2 == 0):
        addYX[0] = 1
    if (imageMatrix.shape[1] % 2 == 0):
        addYX[1] = 1
    dfsStart = (imageMatrix.shape[0] + addYX[0], imageMatrix.shape[1] + addYX[1])
    mazeSeed = seed
    if (mazeSeed == None):
        mazeSeed = app.config['REMEMBERED_SEED']
    maze = None
    walls = None
    if (image == None and sizePercentage == None and seed == None):
        maze = np.array(app.config['REMEMBERED_MAZE'])
        walls = list(app.config['REMEMBERED_WALL_POSITIONS'])
    else: 
        maze = createMaze(mazeMatrix, dfsStart, mazeSeed)
        app.config['REMEMBERED_MAZE'] = np.array(maze)
        walls = getBorderWalls(maze)
        app.config['REMEMBERED_WALL_POSITIONS'] = list(walls)

    startWallIndex = int(startWallPercentValue/100 * len(walls))
    endWallIndex = int(endWallPercentValue/100 * len(walls))
    if (endWallIndex == startWallIndex): endWallIndex += 3
    maze[walls[startWallIndex]] = 255
    maze[walls[endWallIndex]] = 255

    mazeSolution = None
    if (image == None and sizePercentage == None and seed == None and endWallIndex == None and startWallIndex == None):
        mazeSolution = np.array(app.config['REMEMBERED_MAZE_SOLUTION'])
    else: mazeSolution = solveBFS(maze, walls[startWallIndex], walls[endWallIndex])
    svgMaze = mazeToSVG(mazeSolution, cellSize, wallSize, wallColor, solutionColor, showSolution)
    if (showSolution):
        with open("mazeSolved.svg", "w") as f:
            f.write(svgMaze.as_str())
    else:
        with open("maze.svg", "w") as f:
            f.write(svgMaze.as_str())
    return svgMaze

def images_are_equal(img1, img2):
    if (img2 == None):
        return False
    if img1.size != img2.size:
        return False
    
    diff = ImageChops.difference(img1, img2)
    return not diff.getbbox()

def assingValues(startPercent, endPercent, sizePercent, cellSize, wallSize, image, seed):
    newStartPercent, newEndPercent, newSizePercent, newCellSize, newWallSize, newImage, newSeed = None, None, None, None, None, None, None
    if (startPercent != app.config['REMEMBERED_START_PERCENT']):
        newStartPercent = startPercent
        app.config['REMEMBERED_START_PERCENT'] = startPercent
    if (endPercent != app.config['REMEMBERED_END_PERCENT']):
        newEndPercent = endPercent
        app.config['REMEMBERED_END_PERCENT'] = endPercent
    if (sizePercent != app.config['REMEMBERED_SIZE_PERCENTAGE']):
        newSizePercent = sizePercent
        app.config['REMEMBERED_SIZE_PERCENTAGE'] = sizePercent
    if (cellSize != app.config):
        newCellSize = cellSize
        app.config['REMEMBERED_CELL_SIZE'] = cellSize
    if (wallSize != app.config['REMEMBERED_WALL_SIZE']):
        newWallSize = wallSize
        app.config['REMEMBERED_WALL_SIZE'] = wallSize
    if (not images_are_equal(image, app.config['REMEMBERED_IMAGE'])):
        newImage = image
        app.config['REMEMBERED_IMAGE'] = image
    if (seed != app.config['REMEMBERED_SEED']):
        newSeed = seed
        app.config['REMEMBERED_SEED'] = seed

    return newStartPercent, newEndPercent, newSizePercent, newCellSize, newWallSize, newImage, newSeed

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        startPercent = float(request.form["startIndex"])
        endPercent = float(request.form["endIndex"])
        sizePercent = float(request.form["sizePercent"])/100
        cellSize = int(request.form["cellSize"])
        wallSize = int(request.form["wallSize"])
        image = request.files['image']
        seed = 69
        if image:

            image = Image.open(image.stream)
            
            image_io = BytesIO()
            image.save(image_io, format=image.format)
            image_io.seek(0)

            startPercent, endPercent, sizePercent, cellSize, wallSize, image, seed = assingValues(startPercent, endPercent, sizePercent, cellSize, wallSize, image, seed)
            svgMaze = mazeGenerator(image, sizePercent, None, startPercent, endPercent, cellSize, wallSize, "#00ffff", "#f50655", False, seed)

            svgMazeSolved = mazeGenerator(showSolution=True)
            stringMaze, stringSolvedMaze = str(svgMaze), str(svgMazeSolved)

            return jsonify({"maze": stringMaze, "solved":stringSolvedMaze})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
