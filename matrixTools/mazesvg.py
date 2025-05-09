import svg

WALL = 69
SOLUTION = 3

def mazeToSVG(maze, unitSize:int, strokeWidth=1, wallStrokeColor="#000000", solutionStrokeColor = "#ffffff", showSolution = True):
    size = maze.shape
    sizeTrue = (int((maze.shape[0]-1)/2),int((maze.shape[1]-1)/2))
    svgElements = []
    for y in range(0,size[0]):
        tile = maze[y,0]
        lineLength = 0
        startX = 0
        for x in range(0,size[1]):
            if ((maze[y, x] != tile or x == size[1]-1) and lineLength > 0):
                if (lineLength > 1 and tile in [WALL, SOLUTION]):
                    realY = int(y/2)*unitSize+strokeWidth + (unitSize/2 if tile == SOLUTION else 0)
                    realX = int(x/2)*unitSize+strokeWidth - (unitSize/2 if tile == SOLUTION else 0)
                    realStartX = int(startX/2)*unitSize+strokeWidth + (unitSize/2 if tile == SOLUTION else 0)
                    if (tile == WALL or (tile == SOLUTION and showSolution)):
                        svgElements.append(svg.Line(x1=realStartX,
                                                    y1=realY,
                                                    x2=realX, 
                                                    y2=realY, 
                                                    stroke= (solutionStrokeColor if tile == SOLUTION else wallStrokeColor), 
                                                    stroke_width=strokeWidth,
                                                    stroke_linecap="round"))
                if (maze[y, x] in [WALL, SOLUTION]):
                    startX = x
                lineLength = 0
                tile = maze[y, x]
            if (maze[y, x] == tile):
                lineLength += 1
    
    for x in range(0,size[1]):
        tile = maze[0,x]
        lineLength = 0
        startY = 0
        for y in range(0,size[0]):
            if ((maze[y, x] != tile or y == size[0]-1) and lineLength > 0):
                if (lineLength > 1 and tile in [WALL, SOLUTION]):
                    realY = int(y/2)*unitSize+strokeWidth - (unitSize/2 if tile == SOLUTION else 0)
                    realX = int(x/2)*unitSize+strokeWidth + (unitSize/2 if tile == SOLUTION else 0)
                    realStartY = int(startY/2)*unitSize+strokeWidth + (unitSize/2 if tile == SOLUTION else 0)
                    if (tile == WALL or (tile == SOLUTION and showSolution)):
                        svgElements.append(svg.Line(x1=realX,
                                                    y1=realStartY,
                                                    x2=realX, 
                                                    y2=realY, 
                                                    stroke=(solutionStrokeColor if tile == SOLUTION else wallStrokeColor), 
                                                    stroke_width=strokeWidth,
                                                    stroke_linecap="round"))
                if (maze[y, x] in [WALL, SOLUTION]):
                    startY = y
                lineLength = 0
                tile = maze[y, x]
            if (maze[y, x] == tile):
                lineLength += 1
    
    #print("hmm",unitSize)
    #print("hmmmmm",sizeTrue[1])
    #print("hmmmmmmmm",strokeWidth)
    width=(unitSize*sizeTrue[1])+(strokeWidth*2)
    height=unitSize*sizeTrue[0]+strokeWidth*2
    #print(height, width)
    viewbox = svg.ViewBoxSpec(0, 0, width, height)
    canvas = svg.SVG(viewBox=viewbox, elements=svgElements)
    return canvas