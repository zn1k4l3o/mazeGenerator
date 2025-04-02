from PIL import Image
from shapeExtract.imgshape import getShapeFromImage

def main():

    img = Image.open('mazeGenerator/test_images/1.jpg')
    getShapeFromImage(img)

main()