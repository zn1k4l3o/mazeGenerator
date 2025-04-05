from PIL import Image
from shapeExtract.imgshape import getShapeFromImage

def main():
    img = Image.open('mazeGenerator/test_images/4.jpg')
    imageMatrix, mazeMatrix = getShapeFromImage(img)
    dfsStart = imageMatrix.shape

main()