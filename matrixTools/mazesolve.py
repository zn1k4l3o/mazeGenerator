from collections import deque

def solveBFS(maze, start, goal):
    queue = deque([start])
    visited = set()
    came_from = {}
    nodes_visited = 0

    while queue:
        current = queue.popleft()
        nodes_visited += 1

        if current == goal:
            break

        y, x = current
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if (0 <= ny < len(maze) and 0 <= nx < len(maze[0]) 
                and maze[ny][nx] == 255 and (ny, nx) not in visited):
                visited.add((ny, nx))
                queue.append((ny, nx))
                came_from[(ny, nx)] = (y, x)

    return pathToMaze(maze, getPathFromNodes(came_from, start, goal))

def getPathFromNodes(endToStartPath, start, end):
    correctPath = []
    currentPos = end
    correctPath.append(currentPos)
    while (currentPos != start):
        currentPos = endToStartPath[currentPos]
        correctPath.append(currentPos)
    
    return correctPath

def pathToMaze(maze, path):
    for y, x in path:
        maze[y, x] = 3
    return maze
