from PIL import Image
from matrixTools.imgshape import getShapeFromImage
from matrixTools.mazegen import createMaze

def main():
    img = Image.open('mazeGenerator/test_images/6.jpg')
    imageMatrix, mazeMatrix = getShapeFromImage(img, 0.07)
    print(imageMatrix.shape)
    dfsStart = (imageMatrix.shape[0]+1, imageMatrix.shape[1]+1)
    maze = createMaze(mazeMatrix, dfsStart)
    for line in maze:
        out = ''
        for tile in line:
            if (tile == 69):
                out += "X"
            elif (tile == 255):
                out += "."
            else:
                out += ' '
        print(out)
                
    

main()