from PIL import Image, ImageChops
from matrixTools.imgshape import getShapeFromImage
from matrixTools.mazegen import createMaze, getBorderWalls
from matrixTools.mazesvg import mazeToSVG
from matrixTools.mazesolve import solveBFS
from flask import Flask, request, render_template, jsonify, send_file, Response
import numpy as np

app = Flask(__name__)

app.config["REMEMBERED_IMAGE"] = None
app.config["REMEMBERED_IMAGE_MATRIX"] = None
app.config["REMEMBERED_MAZE_MATRIX"] = None
app.config["REMEMBERED_MAZE"] = None
app.config["REMEMBERED_START_PERCENT"] = None
app.config["REMEMBERED_END_PERCENT"] = None
app.config["REMEMBERED_WALL_POSITIONS"] = None
app.config["REMEMBERED_SIZE_PERCENTAGE"] = None
app.config["REMEMBERED_SEED"] = None
app.config["REMEMBERED_MAZE_SOLUTION"] = None
app.config["REMEMBERED_CELL_SIZE"] = None
app.config["REMEMBERED_WALL_SIZE"] = None
app.config["REMEMBERED_SEED"] = None
app.config["REMEMBERED_WALL_COLOR"] = None
app.config["REMEMBERED_SOLUTION_COLOR"] = None
app.config["REMEMBERED_SVG_MAZE"] = None
app.config["REMEMBERED_SVG_SOLUTION"] = None
app.config["REMEMBERED_CROP_AMOUNT"] = None
app.config["REMEMBERED_THRESHOLD"] = None

MAX_CELL_VALUE = 130


def mazeGenerator(
    image=None,
    sizePercentage=None,
    dfsOrigin=None,
    startWallPercent=None,
    endWallPercent=None,
    cellWidth: int = None,
    wallWidth: int = None,
    wallColor=None,
    solutionColor=None,
    showSolution=False,
    seed=None,
    crop=None,
    threshold=None,
):
    img, sizePrct, cropAmount, thresholdAmount = (
        image,
        sizePercentage,
        crop,
        threshold,
    )
    if image == None:
        img = app.config["REMEMBERED_IMAGE"]
    if sizePercentage == None:
        sizePrct = app.config["REMEMBERED_SIZE_PERCENTAGE"]
    if crop == None:
        cropAmount = app.config["REMEMBERED_CROP_AMOUNT"]
    if threshold == None:
        thresholdAmount = app.config["REMEMBERED_THRESHOLD"]
    cellSize, wallSize = cellWidth, wallWidth
    if cellSize == None:
        cellSize = app.config["REMEMBERED_CELL_SIZE"]
    if wallSize == None:
        wallSize = app.config["REMEMBERED_WALL_SIZE"]
    endWallPercentValue, startWallPercentValue = endWallPercent, startWallPercent
    if endWallPercentValue == None:
        endWallPercentValue = app.config["REMEMBERED_END_PERCENT"]
    if startWallPercentValue == None:
        startWallPercentValue = app.config["REMEMBERED_START_PERCENT"]
    newWallColor, newSolutionColor = wallColor, solutionColor
    if wallColor == None:
        newWallColor = app.config["REMEMBERED_WALL_COLOR"]
    if solutionColor == None:
        newSolutionColor = app.config["REMEMBERED_SOLUTION_COLOR"]
    imageMatrix, mazeMatrix = None, None
    if image == None and sizePercentage == None and crop == None and threshold == None:
        imageMatrix = np.array(app.config["REMEMBERED_IMAGE_MATRIX"])
        mazeMatrix = np.array(app.config["REMEMBERED_MAZE_MATRIX"])
    else:
        imageMatrix, mazeMatrix = getShapeFromImage(
            img, sizePrct, threshold=thresholdAmount, cropAmount=cropAmount
        )
        app.config["REMEMBERED_IMAGE_MATRIX"] = np.array(imageMatrix)
        app.config["REMEMBERED_MAZE_MATRIX"] = np.array(mazeMatrix)
    addYX = [0, 0]
    if imageMatrix.shape[0] % 2 == 0:
        addYX[0] = 1
    if imageMatrix.shape[1] % 2 == 0:
        addYX[1] = 1
    dfsStart = (imageMatrix.shape[0] + addYX[0], imageMatrix.shape[1] + addYX[1])
    mazeSeed = seed
    if mazeSeed == None:
        mazeSeed = app.config["REMEMBERED_SEED"]
    maze = None
    walls = None
    if (
        image == None
        and sizePercentage == None
        and seed == None
        and crop == None
        and threshold == None
    ):
        maze = np.array(app.config["REMEMBERED_MAZE"])
        walls = list(app.config["REMEMBERED_WALL_POSITIONS"])
    else:
        maze = createMaze(mazeMatrix, dfsStart, mazeSeed)
        app.config["REMEMBERED_MAZE"] = np.array(maze)
        walls = getBorderWalls(maze)
        app.config["REMEMBERED_WALL_POSITIONS"] = list(walls)

    startWallIndex = int(startWallPercentValue / 100 * len(walls))
    endWallIndex = int(endWallPercentValue / 100 * len(walls))
    if startWallIndex == len(walls):
        startWallIndex = startWallIndex % len(walls)
    if endWallIndex == len(walls):
        endWallIndex = endWallIndex % len(walls)
    if endWallIndex == startWallIndex:
        endWallIndex += 3
    if endWallIndex == len(walls):
        endWallIndex = endWallIndex % len(walls)
    maze[walls[startWallIndex]] = 255
    maze[walls[endWallIndex]] = 255

    mazeSolution = None
    if (
        image == None
        and sizePercentage == None
        and seed == None
        and endWallPercent == None
        and startWallPercent == None
        and crop == None
        and threshold == None
    ):
        mazeSolution = np.array(app.config["REMEMBERED_MAZE_SOLUTION"])
    else:
        mazeSolution = solveBFS(maze, walls[startWallIndex], walls[endWallIndex])
        app.config["REMEMBERED_MAZE_SOLUTION"] = np.array(mazeSolution)

    svgMaze = mazeToSVG(
        mazeSolution,
        cellSize,
        wallSize,
        newWallColor,
        newSolutionColor,
        showSolution,
    )

    if showSolution:
        with open("mazeSolved.svg", "w") as f:
            f.write(svgMaze.as_str())
    else:
        with open("maze.svg", "w") as f:
            f.write(svgMaze.as_str())
    return svgMaze


def images_are_equal(img1, img2):
    if img2 == None:
        return False
    if img1.size != img2.size:
        return False

    diff = ImageChops.difference(img1, img2)
    return not diff.getbbox()


def assingValues(
    startPercent,
    endPercent,
    sizePercent,
    cellSize,
    wallSize,
    image,
    seed,
    wallColor,
    solutionColor,
    crop,
    threshold,
):
    (
        newStartPercent,
        newEndPercent,
        newSizePercent,
        newCellSize,
        newWallSize,
        newImage,
        newSeed,
        newWallColor,
        newSolutionColor,
        newCrop,
        newThreshold,
    ) = (None, None, None, None, None, None, None, None, None, None, None)
    if startPercent != app.config["REMEMBERED_START_PERCENT"]:
        newStartPercent = startPercent
        app.config["REMEMBERED_START_PERCENT"] = startPercent
    if endPercent != app.config["REMEMBERED_END_PERCENT"]:
        newEndPercent = endPercent
        app.config["REMEMBERED_END_PERCENT"] = endPercent
    if sizePercent != app.config["REMEMBERED_SIZE_PERCENTAGE"]:
        newSizePercent = sizePercent
        app.config["REMEMBERED_SIZE_PERCENTAGE"] = sizePercent
    if cellSize != app.config:
        newCellSize = cellSize
        app.config["REMEMBERED_CELL_SIZE"] = cellSize
    if wallSize != app.config["REMEMBERED_WALL_SIZE"]:
        newWallSize = wallSize
        app.config["REMEMBERED_WALL_SIZE"] = wallSize
    if not images_are_equal(image, app.config["REMEMBERED_IMAGE"]):
        newImage = image
        app.config["REMEMBERED_IMAGE"] = image
    if seed != app.config["REMEMBERED_SEED"]:
        newSeed = seed
        app.config["REMEMBERED_SEED"] = seed
    if wallColor != app.config["REMEMBERED_WALL_COLOR"]:
        newWallColor = wallColor
        app.config["REMEMBERED_WALL_COLOR"] = wallColor
    if solutionColor != app.config["REMEMBERED_SOLUTION_COLOR"]:
        newSolutionColor = wallColor
        app.config["REMEMBERED_SOLUTION_COLOR"] = solutionColor
    if crop != app.config["REMEMBERED_CROP_AMOUNT"]:
        newCrop = crop
        app.config["REMEMBERED_CROP_AMOUNT"] = crop
    if threshold != app.config["REMEMBERED_THRESHOLD"]:
        newThreshold = threshold
        app.config["REMEMBERED_THRESHOLD"] = threshold

    return (
        newStartPercent,
        newEndPercent,
        newSizePercent,
        newCellSize,
        newWallSize,
        newImage,
        newSeed,
        newWallColor,
        newSolutionColor,
        newCrop,
        newThreshold,
    )


def checkSize(image, sizePercent):
    if (
        image.size[0] * sizePercent > MAX_CELL_VALUE
        or image.size[1] * sizePercent > MAX_CELL_VALUE
    ):
        newSizePercent = MAX_CELL_VALUE / max(image.size[0], image.size[1])
        return newSizePercent
    return sizePercent


@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        startPercent = float(request.form["startIndex"])
        endPercent = float(request.form["endIndex"])
        sizePercent = float(request.form["sizePercent"]) / 100
        cellSize = int(request.form["cellSize"])
        wallSize = int(request.form["wallSize"])
        image = request.files["image"]
        seed = int(request.form["seed"])
        wallColor = request.form["wallColor"]
        solutionColor = request.form["solutionColor"]
        crop = int(request.form["crop"])
        threshold = int(request.form["threshold"])
        if image:

            image = Image.open(image.stream)

            sizePercent = checkSize(image, sizePercent)
            (
                startPercent,
                endPercent,
                sizePercent,
                cellSize,
                wallSize,
                image,
                seed,
                wallColor,
                solutionColor,
                crop,
                threshold,
            ) = assingValues(
                startPercent,
                endPercent,
                sizePercent,
                cellSize,
                wallSize,
                image,
                seed,
                wallColor,
                solutionColor,
                crop,
                threshold,
            )

            svgMaze = mazeGenerator(
                image,
                sizePercent,
                None,
                startPercent,
                endPercent,
                cellSize,
                wallSize,
                wallColor,
                solutionColor,
                False,
                seed,
                crop,
                threshold,
            )
            svgMazeSolved = mazeGenerator(showSolution=True)
            stringMaze, stringSolvedMaze = str(svgMaze), str(svgMazeSolved)

            return jsonify({"maze": stringMaze, "solved": stringSolvedMaze})

    return render_template("index.html")


if __name__ == "__main__":
    app.run(use_reloader=False)
