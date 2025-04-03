import numpy as np
from PIL import Image, ImageFile

def crop_fixed_border(img, border=20):
    height, width = img.shape

    x0 = min(height, max(0, border))
    y0 = min(width, max(0, border))
    x1 = max(0, min(height, height - border))
    y1 = max(0, min(width, width - border))

    return img[x0:x1, y0:y1]

def crop_white_space(img):
    mask = img < 255 
    coords = np.argwhere(mask)

    if coords.size == 0:
        return Image.fromarray(img)

    x0, y0 = coords.min(axis=0)
    x1, y1 = coords.max(axis=0)+1

    cropped_img = img[x0:x1, y0:y1]

    return Image.fromarray(cropped_img)

def fill_middle(img):
    dirr = [(0,1), (0,-1), (1, 0), (-1, 0)]
    #newImg = img.convert('RGB')
    imageData = np.array(img, dtype=np.uint8)
    #imageData = img
    newImage = Image.fromarray(imageData)
    newImage.show()
    height, width = imageData.shape
    print(width, height)
    pointsToVisit = [(0,0)]
    while len(pointsToVisit) > 0:
        currPoint = pointsToVisit.pop()
        for pair in dirr:
            new = (currPoint[0] + pair[0], currPoint[1] + pair[1])
            if not(new[0] < 0 or new[1] < 0 or new[1] >= width or new[0] >= height):
                if (imageData[new[0], new[1]] == 255):
                    imageData[new[0], new[1]] = 69
                    #print(new)
                    pointsToVisit.append(new)
    for i in range(height):
        for j in range(width):
            if (imageData[i, j] == 69):
                imageData[i, j] = 255
            elif (imageData[i, j] == 255):
                imageData[i, j] = 0
    return imageData

def getShapeFromImage(image: ImageFile):
    graf = np.zeros((101, 101), dtype=np.bool_)
    thresh = 245
    allWhite =  Image.new("RGBA", image.size, "WHITE")
    if (image.format == 'PNG'):
        allWhite.paste(image, (0,0), image)
    else:
        allWhite = image

    fn = lambda x: 255 if x > thresh else 0
    convertedImage = allWhite.convert('L').point(fn, mode='L')
    imageData = np.asarray(convertedImage, dtype=np.uint8)

    croppedImageData = crop_fixed_border(imageData, border=20)
    filledImageData = fill_middle(croppedImageData)
    finalCroppedImage = crop_white_space(filledImageData)
    finalCroppedImage.show()
    multiplier = 0.07       #how big is the target maze
    #multiplier = 0.005  #test
    newWidth = (int) (finalCroppedImage.width*multiplier)
    newHeight= (int) (finalCroppedImage.height*multiplier)
    print(newHeight,newWidth)
    smallerImage = finalCroppedImage.resize((newWidth, newHeight))
    smallerImage.show()

    graf = np.bitwise_not(np.array(smallerImage, dtype="uint8"))

    graf3X = np.repeat(np.repeat(graf, 3, axis=0), 3, axis=1)
    
    print("mali")
    for line in graf:
        out = ''
        for tile in line:
            out += "X" if tile else '_'
        print(out)
    print("trostruki")
    for line in graf3X:
        out = ''
        for tile in line:
            out += "X" if tile else '_'
        print(out)
    
    return graf3X