import svg

WALL = 69

def mazeToSVG(maze, unitSize):
    size = maze.shape
    sizeTrue = (int((maze.shape[0]-1)/2),int((maze.shape[1]-1)/2))
    svgElements = []
    for y in range(0,size[0], 2):
        lineLength = 0
        startX = 0
        #print("novi red", y)
        for x in range(0,size[1]):
            if (maze[y, x] == WALL):
                if (lineLength == 0):
                    startX = x
                lineLength += 1
            if ((maze[y, x] != WALL or x == size[1]-1) and lineLength > 0):
                #print("x: " , x , "lineLength: " ,lineLength)
                if (lineLength > 1):
                    #startX = x - lineLength
                    #lineLength = int((lineLength-1)/2)
                    realY = int(y/2)*unitSize
                    realX = int(x/2)*unitSize
                    realStartX = int(startX/2)*unitSize
                    #print("sx: {0}, ex: {1}, sy: {2}, ey: {3}".format(realStartX, realX, realY, realY))
                    svgElements.append(svg.Line(x1=realStartX,
                                                y1=realY,
                                                x2=realX, 
                                                y2=realY, 
                                                stroke="red", 
                                                stroke_width=2))
                lineLength = 0
    print()
    print()
    #print("Druga strana")
    
    for x in range(0,size[1]):
        lineLength = 0
        startY = 0
        #print("novi red", x)
        for y in range(0,size[0]):
            if (maze[y, x] == WALL):
                if (lineLength == 0):
                    startY = y
                lineLength += 1
            if ((maze[y, x] != WALL or y == size[0]-1) and lineLength > 0):
                #print("y: " , y , "lineLength: " , lineLength)
                if (lineLength > 1):
                    realY = int(y/2)*unitSize
                    realX = int(x/2)*unitSize
                    realStartY = int((startY)/2)*unitSize
                    svgElements.append(svg.Line(x1=realX,
                                                y1=realStartY,
                                                x2=realX, 
                                                y2=realY, 
                                                stroke="red", 
                                                stroke_width=2))
                lineLength = 0
    
    #ispraviti velicine
    canvas = svg.SVG(
    width=unitSize*sizeTrue[1],
    height=unitSize*sizeTrue[0],
    elements=svgElements
)
    #print(canvas)
    return canvas