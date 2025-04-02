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
    x1, y1 = coords.max(axis=0) + 1

    cropped_img = img[x0:x1, y0:y1]

    return Image.fromarray(cropped_img)

def getShapeFromImage(image: ImageFile):
    graf = np.zeros((101, 101), dtype=np.bool_)
    thresh = 240
    fn = lambda x: 255 if x > thresh else 0
    convertedImage = image.convert('L').point(fn, mode='L')
    imageData = np.asarray(convertedImage, dtype=np.uint8)

    croppedImageData = crop_fixed_border(imageData, border=20)

    finalCroppedImage = crop_white_space(croppedImageData)

    multiplier = 0.02
    newWidth = (int) (finalCroppedImage.width*multiplier)
    newHeight= (int) (finalCroppedImage.height*multiplier)
    print(newHeight,newWidth)
    smallerImage = finalCroppedImage.resize((newWidth, newHeight))
    smallerImage.show()

    graf = np.bitwise_not(np.array(smallerImage, dtype="bool"))
    print(graf)
    
    return graf