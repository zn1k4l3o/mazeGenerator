from PIL import Image, ImageChops
from matrixTools.imgshape import getShapeFromImage
from matrixTools.mazegen import createMaze, getBorderWalls
from matrixTools.mazesvg import mazeToSVG
from matrixTools.mazesolve import solveBFS
from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
import os
import numpy as np

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = os.path.join(os.getcwd(), "flask_session")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True

os.makedirs(app.config["SESSION_FILE_DIR"], exist_ok=True)

Session(app)

MAX_CELL_VALUE = 130


def mazeGenerator(
    image=None,
    sizePercentage=None,
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
    areImageOptsSame = (
        image == None and sizePercentage == None and crop == None and threshold == None
    )

    img = image or session.get("REMEMBERED_IMAGE")
    sizePrct = sizePercentage or session.get("REMEMBERED_SIZE_PERCENTAGE")
    cropAmount = crop if crop is not None else session.get("REMEMBERED_CROP_AMOUNT")
    thresholdAmount = (
        threshold if threshold is not None else session.get("REMEMBERED_THRESHOLD")
    )
    cellSize = (
        cellWidth if cellWidth is not None else session.get("REMEMBERED_CELL_SIZE")
    )
    wallSize = (
        wallWidth if wallWidth is not None else session.get("REMEMBERED_WALL_SIZE")
    )
    startWallPercentValue = (
        startWallPercent
        if startWallPercent is not None
        else session.get("REMEMBERED_START_PERCENT")
    )
    endWallPercentValue = (
        endWallPercent
        if endWallPercent is not None
        else session.get("REMEMBERED_END_PERCENT")
    )
    newWallColor = wallColor or session.get("REMEMBERED_WALL_COLOR")
    newSolutionColor = solutionColor or session.get("REMEMBERED_SOLUTION_COLOR")

    try:
        imageMatrix, mazeMatrix = None, None
        if areImageOptsSame:
            imageMatrix = np.array(session.get("REMEMBERED_IMAGE_MATRIX"))
            mazeMatrix = np.array(session.get("REMEMBERED_MAZE_MATRIX"))
        else:
            imageMatrix, mazeMatrix = getShapeFromImage(
                img, sizePrct, threshold=thresholdAmount, cropAmount=cropAmount
            )
            session["REMEMBERED_IMAGE_MATRIX"] = np.array(imageMatrix)
            session["REMEMBERED_MAZE_MATRIX"] = np.array(mazeMatrix)
        addYX = [0, 0]
        if imageMatrix.shape[0] % 2 == 0:
            addYX[0] = 1
        if imageMatrix.shape[1] % 2 == 0:
            addYX[1] = 1
        dfsStart = (imageMatrix.shape[0] + addYX[0], imageMatrix.shape[1] + addYX[1])
        mazeSeed = seed
        if mazeSeed == None:
            mazeSeed = session.get("REMEMBERED_SEED")
        maze = None
        walls = None
        if areImageOptsSame and seed == None:
            maze = np.array(session.get("REMEMBERED_MAZE"))
            walls = list(session.get("REMEMBERED_WALL_POSITIONS"))
        else:
            maze = createMaze(mazeMatrix, dfsStart, mazeSeed)
            session["REMEMBERED_MAZE"] = np.array(maze)
            walls = getBorderWalls(maze)
            session["REMEMBERED_WALL_POSITIONS"] = list(walls)

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
            areImageOptsSame
            and seed == None
            and endWallPercent == None
            and startWallPercent == None
        ):
            mazeSolution = np.array(session.get("REMEMBERED_MAZE_SOLUTION"))
        else:
            mazeSolution = solveBFS(maze, walls[startWallIndex], walls[endWallIndex])
            session["REMEMBERED_MAZE_SOLUTION"] = np.array(mazeSolution)

        svgMaze = mazeToSVG(
            mazeSolution,
            cellSize,
            wallSize,
            newWallColor,
            newSolutionColor,
            showSolution,
        )

        return svgMaze
    except:
        session["REMEMBERED_START_PERCENT"] = None
        session["REMEMBERED_END_PERCENT"] = None
        session["REMEMBERED_SIZE_PERCENTAGE"] = None
        session["REMEMBERED_CELL_SIZE"] = None
        session["REMEMBERED_WALL_SIZE"] = None
        session["REMEMBERED_IMAGE"] = None
        session["REMEMBERED_SEED"] = None
        session["REMEMBERED_WALL_COLOR"] = None
        session["REMEMBERED_SOLUTION_COLOR"] = None
        session["REMEMBERED_CROP_AMOUNT"] = None
        session["REMEMBERED_THRESHOLD"] = None
        return None


def imagesAreEqual(img1, img2):
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
    remembered = session

    (
        startPercentNew,
        endPercentNew,
        sizePercentNew,
        cellSizeNew,
        wallSizeNew,
        imageNew,
        seedNew,
        wallColorNew,
        solutionColorNew,
        cropNew,
        thresholdNew,
    ) = (None, None, None, None, None, None, None, None, None, None, None)
    if startPercent != remembered.get("REMEMBERED_START_PERCENT"):
        session["REMEMBERED_START_PERCENT"] = startPercent
        startPercentNew = startPercent
    if endPercent != remembered.get("REMEMBERED_END_PERCENT"):
        session["REMEMBERED_END_PERCENT"] = endPercent
        endPercentNew = endPercent
    if sizePercent != remembered.get("REMEMBERED_SIZE_PERCENTAGE"):
        session["REMEMBERED_SIZE_PERCENTAGE"] = sizePercent
        sizePercentNew = sizePercent
    if cellSize != remembered.get("REMEMBERED_CELL_SIZE"):
        session["REMEMBERED_CELL_SIZE"] = cellSize
        cellSizeNew = cellSize
    if wallSize != remembered.get("REMEMBERED_WALL_SIZE"):
        session["REMEMBERED_WALL_SIZE"] = wallSize
        wallSizeNew = wallSize
    if not imagesAreEqual(image, remembered.get("REMEMBERED_IMAGE")):
        session["REMEMBERED_IMAGE"] = image
        imageNew = image
    if seed != remembered.get("REMEMBERED_SEED"):
        session["REMEMBERED_SEED"] = seed
        seedNew = seed
    if wallColor != remembered.get("REMEMBERED_WALL_COLOR"):
        session["REMEMBERED_WALL_COLOR"] = wallColor
        wallColorNew = wallColor
    if solutionColor != remembered.get("REMEMBERED_SOLUTION_COLOR"):
        session["REMEMBERED_SOLUTION_COLOR"] = solutionColor
        solutionColorNew = solutionColor
    if crop != remembered.get("REMEMBERED_CROP_AMOUNT"):
        session["REMEMBERED_CROP_AMOUNT"] = crop
        cropNew = crop
    if threshold != remembered.get("REMEMBERED_THRESHOLD"):
        session["REMEMBERED_THRESHOLD"] = threshold
        thresholdNew = threshold

    return (
        startPercentNew,
        endPercentNew,
        sizePercentNew,
        cellSizeNew,
        wallSizeNew,
        imageNew,
        seedNew,
        wallColorNew,
        solutionColorNew,
        cropNew,
        thresholdNew,
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
            if svgMaze == None:
                return jsonify({"state": "fail"})
            svgMazeSolved = mazeGenerator(showSolution=True)
            stringMaze, stringSolvedMaze = str(svgMaze), str(svgMazeSolved)

            return jsonify(
                {"state": "success", "maze": stringMaze, "solved": stringSolvedMaze}
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(use_reloader=False)
