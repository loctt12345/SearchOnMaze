import numpy
import pygame
from collections import deque as queue
import sys
from queue import PriorityQueue
import copy


BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
GREEN = (124,252,0)
BLUE = (0, 0, 250)
RED = (255, 0, 0)
BROWN = (128,128,0)
dRow = [ -1, 0, 1, 0]
dCol = [ 0, 1, 0, -1]
blockSize = 30

def display(grid):
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    WINDOW_HEIGHT = height * blockSize
    WINDOW_WIDTH = width * blockSize
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)

    while True:
        drawGrid(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def drawGrid(grid):
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)
            #ygame.draw.rect(SCREEN, GREEN, rect)
    rect = pygame.Rect(s_x * blockSize + 2, (height - s_y - 1) * blockSize + 2, blockSize - 4, blockSize - 4)
    pygame.draw.rect(SCREEN, GREEN, rect)
    pygame.draw.circle(SCREEN, RED, rect.center, 5)
    rect = pygame.Rect(g_x * blockSize + 2, (height - g_y - 1) * blockSize + 2, blockSize - 4, blockSize - 4)
    pygame.draw.rect(SCREEN, GREEN, rect)
    pygame.draw.circle(SCREEN, RED, rect.center, 5)
    for j in range(height):
        for i in range(width):
            if (grid[i][height - j - 1] == 1):
                rect = pygame.Rect(i * blockSize + 2, j * blockSize + 2, blockSize - 4, blockSize - 4)
                pygame.draw.rect(SCREEN, BLUE, rect)
            elif (grid[i][height - j - 1] == 2):
                rect = pygame.Rect(i * blockSize + 2, j * blockSize + 2, blockSize - 4, blockSize - 4)
                pygame.draw.rect(SCREEN, BROWN, rect)
            elif (grid[i][height - j - 1] == 3):
                rect = pygame.Rect(i * blockSize + 2, j * blockSize + 2, blockSize - 4, blockSize - 4)
                pygame.draw.rect(SCREEN, WHITE, rect)
                pygame.draw.circle(SCREEN, RED, rect.center, 5)

def bresenham(x1, y1, x2, y2, mark=None):
      dx, dy            = x1 - x2, y1 - y2
      dx_abs, dy_abs    = abs(dx), abs(dy)
      px, py            = 2 * dy_abs - dx_abs, 2 * dx_abs - dy_abs

      # X-axis dominates
      if dx_abs > dy_abs:
         if dx < 0:
            xs, xe, y   = x1, x2, y1
         else:
            xs, xe, y   = x2, x1, y2

         while xs <= xe:

            # Color cells on line
            maze[y][xs] = 1

            # Mark cells on line
            if mark is not None:
               mark[y][xs] = True

            xs          += 1
            if px < 0:
               px       += 2 * dy_abs
            else:
               y        += (1 if dx * dy > 0 else -1) 
               px       += 2 * (dy_abs - dx_abs)

      # Y-axis dominates
      else:
         if dy < 0:
            ys, ye, x   = y1, y2, x1
         else:
            ys, ye, x   = y2, y1, x2

         while ys <= ye:
            maze[ys][x] = 1

            if mark is not None:
               mark[ys][x] = True

            ys          += 1
            if py < 0:
               py       += 2 * dx_abs
            else:
               x        += (1 if dx * dy > 0 else -1)
               py       += 2 * (dx_abs - dy_abs)

def find_convex_polygon(list_coor):
    #ist_coor.sort(key=compare)
    list_coor.append(list_coor[0])
    for i in range(len(list_coor) - 1):
       bresenham(list_coor[i][1], list_coor[i][0], list_coor[i+1][1], list_coor[i+1][0])

def inputData():
    f = open("input.txt", "r")
    lines = f.read().splitlines()
    lines_converted = []
    for line in lines:
        line = line.split()
        for i in range(len(line)):
            line[i] = int(line[i])
        lines_converted.append(line)
    global maze, width, height, s_x, s_y, g_x, g_y, n_obstacle
    width = lines_converted[0][0]
    height = lines_converted[0][1]
    maze = [[0 for i in range(height)] for j in range(width)]
    s_x = lines_converted[1][0]
    s_y = lines_converted[1][1]
    g_x = lines_converted[1][2]
    g_y = lines_converted[1][3]
    n_obstacle = lines_converted[2][0]
    for i in range(n_obstacle):
        list_coor = []
        for j in range(0, len(lines_converted[i + 3]) - 1, 2) :
            list_coor.append((lines_converted[i + 3][j], lines_converted[i + 3][j + 1]))
        find_convex_polygon(list_coor)
        for j in range(0, len(lines_converted[i + 3]) - 1, 2) :
            maze[lines_converted[i + 3][j]][lines_converted[i + 3][j + 1]] = 2

    """for j in range(height):
        for i in range(width):
            print(maze[i][height - j - 1], end='')
        print("")"""
    f.close()

def checkInside(x, y):
    if (x >= width or x < 0 or y >= height or y < 0):
        return False
    return True

def check(x, y, mark):
    if (not checkInside(x, y)):
        return False
    if (maze[x][y] == 1 or maze[x][y] == 2):
        return False
    if (mark[x][y]):
        return False
    return True

def BFS():
    cost_return = 0
    mark = [[ False for i in range(height)] for i in range(width)]
    trace = [[ (-1, -1) for i in range(height)] for i in range(width)]
    q = queue()
    q.append((s_x, s_y))
    mark[s_x][s_y] = True
    while (len(q) > 0):
        cell = q.popleft()
        x = cell[0]
        y = cell[1]
        if (x == g_x and y == g_y):
            break
        # Go to the adjacent cells
        for i in range(4):
            adjx = x + dRow[i]
            adjy = y + dCol[i]
            if (check(adjx, adjy, mark)):
                q.append((adjx, adjy))
                mark[adjx][adjy] = True
                trace[adjx][adjy] = (x, y)

    x = g_x
    y = g_y
    while (trace[x][y] != (-1, -1)):
        x1 = trace[x][y][0]
        y1 = trace[x][y][1]
        x = x1
        y = y1
        maze[x][y] = 3
        cost_return += 1
    maze[s_x][s_y] = 0
    return cost_return

def uniform_cost_search():
    q = PriorityQueue()
    q.put((0, [(s_x, s_y)]))
    mark = [[ False for i in range(height)] for i in range(width)]
    while (not q.empty()):
        pair = q.get()
        current = pair[1][-1]
        if (current == (g_x, g_y)):
            #return pair[1]
            for cell in pair[1]:
                maze[cell[0]][cell[1]] = 3
            maze[s_x][s_y] = 0
            maze[g_x][g_y] = 0
            return pair[0]
        
        if not mark[current[0]][current[1]]:
            for i in range(4):
                adjx = current[0] + dRow[i]
                adjy = current[1] + dCol[i]
                if (checkInside(adjx, adjy)):
                    #print(adjx, adjy)
                    new_path = list(pair[1])
                    new_path.append((adjx, adjy))
                    cost = 1
                    if (maze[adjx][adjy] == 1):
                        cost = 10**8
                    q.put(((pair[0] + cost), new_path))

        mark[current[0]][current[1]] = True

def DFS(current, maxDepth, mark, path):
    if (not check(current[0], current[1], mark)):
        return False
    mark[current[0]][current[1]] = True
    if (current == (g_x, g_y)):
        return True;
    if (maxDepth <= 0):
        return False
    for i in range(4):
        adjx = current[0] + dRow[i]
        adjy = current[1] + dCol[i]
        path.append((adjx, adjy))
        if (DFS((adjx, adjy), maxDepth - 1, mark, path)):
            return True
        path.pop()
    return False

def iterative_deepening_search(maxDepth):
    for limit in range(maxDepth):
        mark = [[ False for i in range(height)] for i in range(width)]
        path = []
        if (DFS((s_x, s_y), limit, mark, path)):
            for (x, y) in path:
                maze[x][y] = 3
            maze[s_x][s_y] = 0
            maze[g_x][g_y] = 0
            return len(path)
    return -1

def heuristic(x):
    return abs(x[0] - g_x) + abs(x[1] - g_y)

def greedyBFS():
    cost_return = 0
    q = PriorityQueue()
    mark = [[ False for i in range(height)] for i in range(width)]
    trace = [[ (-1, -1) for i in range(height)] for i in range(width)]
    q.put((heuristic((s_x, s_y)), (s_x, s_y)))
    mark[s_x][s_y] = True
    while (not q.empty()):
        pair = q.get()[1]
        if (pair == (g_x, g_y)):
            break
        for i in range(4):
            adjx = pair[0] + dRow[i]
            adjy = pair[1] + dCol[i]
            if (check(adjx, adjy, mark)):
                mark[adjx][adjy] = True
                q.put((heuristic((adjx, adjy)), (adjx, adjy)))
                trace[adjx][adjy] = (pair[0], pair[1])

    x = g_x
    y = g_y
    while (trace[x][y] != (-1, -1)):
        x1 = trace[x][y][0]
        y1 = trace[x][y][1]
        x = x1
        y = y1
        maze[x][y] = 3
        cost_return += 1
    maze[s_x][s_y] = 0
    maze[g_x][g_y] = 0
    return cost_return

def fromStartToCurrent(x):
    return abs(x[0] - s_x) + abs(x[1] - s_y)

def aStar():
    cost_return = 0
    q = PriorityQueue()
    mark = [[ False for i in range(height)] for i in range(width)]
    trace = [[ (-1, -1) for i in range(height)] for i in range(width)]
    q.put((heuristic((s_x, s_y)) + fromStartToCurrent((s_x, s_y)), (s_x, s_y)))
    mark[s_x][s_y] = True
    while (not q.empty()):
        pair = q.get()[1]
        if (pair == (g_x, g_y)):
            break
        for i in range(4):
            adjx = pair[0] + dRow[i]
            adjy = pair[1] + dCol[i]
            if (check(adjx, adjy, mark)):
                mark[adjx][adjy] = True
                q.put((heuristic((adjx, adjy)) + fromStartToCurrent((adjx, adjy)), (adjx, adjy)))
                trace[adjx][adjy] = (pair[0], pair[1])

    x = g_x
    y = g_y
    while (trace[x][y] != (-1, -1)):
        x1 = trace[x][y][0]
        y1 = trace[x][y][1]
        x = x1
        y = y1
        maze[x][y] = 3
        cost_return += 1
    maze[s_x][s_y] = 0
    maze[g_x][g_y] = 0
    return cost_return

def main():
    inputData()
    print("Choose algorithm for robot: ")
    print("1.Breadth-first search")
    print("2.Uniform-cost search")
    print("3.Iterative deepening search")
    print("4.Greedy-best first search")
    print("5.Graph-search A*")
    choice = int(input())
    if choice == 1:
        print("Cost:", BFS())
    elif choice == 2:
        print("Cost:", uniform_cost_search())
    elif choice == 3:
        maxDepth = width * height
        print(maxDepth)
        print("Cost:", iterative_deepening_search(maxDepth))
    elif choice == 4:
        print("Cost:", greedyBFS())
    elif choice == 5:
        print("Cost:", aStar())
    display(maze)
 
if __name__ == "__main__":
    main()
