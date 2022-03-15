import numpy
import pygame


BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
GREEN = (124,252,0)
BLUE = (0, 0, 250)
BROWN = (128,128,0)

blockSize = 30

def display():
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    WINDOW_HEIGHT = height * blockSize
    WINDOW_WIDTH = width * blockSize
    print(WINDOW_HEIGHT, WINDOW_WIDTH)
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)

    while True:
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def drawGrid():
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, BLACK, rect, 1)
            #ygame.draw.rect(SCREEN, GREEN, rect)
    rect = pygame.Rect(s_x * blockSize + 2, (height - s_y - 1) * blockSize + 2, blockSize - 4, blockSize - 4)
    pygame.draw.rect(SCREEN, GREEN, rect)
    rect = pygame.Rect(g_x * blockSize + 2, (height - g_y - 1) * blockSize + 2, blockSize - 4, blockSize - 4)
    pygame.draw.rect(SCREEN, GREEN, rect)
    for i in range(0, height):
        for j in range(0, width):
            if (maze[i][j] == 1):
                rect = pygame.Rect(i * blockSize + 2, (height - j - 1) * blockSize + 2, blockSize - 4, blockSize - 4)
                pygame.draw.rect(SCREEN, BLUE, rect)
            elif (maze[i][j] == 2):
                rect = pygame.Rect(i * blockSize + 2, (height - j - 1) * blockSize + 2, blockSize - 4, blockSize - 4)
                pygame.draw.rect(SCREEN, BROWN, rect)
def display_maze():
    pass

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
    print(list_coor)
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
    maze = [[0 for i in range(width)] for j in range(height)]
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

    for i in range(height):
        for j in range(width):
            print(maze[i][j], end='')
        print("")
    f.close()

inputData()    
display()
