import pygame, random, thread, time, sys
from pygame.locals import *

# total maze size (height and width)
# must be odd
MAZE_SIZE = 191
# wall thickness (best at 1)
# must be >= 1
WALL_SIZE = 1
# straightens out paths
# 0 for no forced straightening
STRAIGHT_MULT = 25
# width of borders
BORDERS = 1
# amount of cut/loops added
CUTS = 5

TILE_SIZE = 2

WALL_CHAR = '#'
PATH_CHAR = '_'

# directions, in order from 0-3 (u, r, d, l)
DIR_SET = [[0, 1], [1, 0], [0, -1], [-1, 0]]

# order of events
# search for empty directions (u, r, d, l)
# path 2 in a direction
# save direction to array
# repeat 1-2 until a dead end is hit
# backtrack through direction array until (1)

def create_path(surface, maze, path, x, y):
    valid = []
    for i in range(len(DIR_SET)):
        nx = x + DIR_SET[i][0] * (WALL_SIZE + 1)
        ny = y + DIR_SET[i][1] * (WALL_SIZE + 1)
        if nx < 0 or ny < 0 or nx >= MAZE_SIZE or ny >= MAZE_SIZE:
            continue

        if maze[ny][nx] is 0:
            valid.append(i)

    if len(valid) is 0:
        # dead end hit, do 1 step of backtracking
        last_move = path.pop()
        for i in range(1, WALL_SIZE + 2):
            bx = x - last_move[0] * i
            by = y - last_move[1] * i
            draw_box(surface, (255, 0, 0), bx, by)
        return bx, by

    else:
        # give higher chance of staying straight
        if len(path) > 0 and DIR_SET.index(path[-1]) in valid:
            for i in range(STRAIGHT_MULT):
                valid.append(DIR_SET.index(path[-1]))
        move = DIR_SET[random.choice(valid)]
        path.append(move)
        for i in range(1, WALL_SIZE + 2):
            nx = x + move[0] * i
            ny = y + move[1] * i
            maze[ny][nx] = 1
            draw_box(surface, (0, 255, 0), nx, ny)
        return nx, ny

def create_cut(background, maze):
    cut = False
    while not cut:
        cut_x = int(random.random() * (MAZE_SIZE / (WALL_SIZE + 1))) * (WALL_SIZE + 1)
        cut_y = int(random.random() * (MAZE_SIZE / (WALL_SIZE + 1))) * (WALL_SIZE + 1)
        print cut_x, cut_y
        if maze[cut_y][cut_x] is 0:
            maze[cut_y][cut_x] = 1
            cut = True

def init_pygame():
    # initialize pygame and objects
    pygame.init()
    pygame.display.set_caption("Maze generator")
    screen = pygame.display.set_mode((MAZE_SIZE * TILE_SIZE,
            MAZE_SIZE * TILE_SIZE))
    clock = pygame.time.Clock()
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    return screen, clock, background

def visual(steps_per_frame=1):
    # main maze array
    maze = [[0] * MAZE_SIZE for i in range(MAZE_SIZE)]
    exit = False

    screen, clock, background = init_pygame()

    cuts = 0
    path = []
    x, y = create_path(None, maze, path, int(MAZE_SIZE / 2), int(MAZE_SIZE / 2))

    while not exit:
        clock.tick(120)
        screen.blit(background, (0, 0))
        draw_screen(background, maze)
        draw_path(background, path)
        for i in range(steps_per_frame):
            if len(path) > 0:
                x, y = create_path(background, maze, path, x, y)
            elif cuts < CUTS:
                create_cut(background, maze)
                cuts += 1
            elif not exit:
                to_file(maze)
                exit = True
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                    event.key == K_ESCAPE):
                return

def gen():
    # main maze array
    maze = [[0] * MAZE_SIZE for i in range(MAZE_SIZE)]
    exit = False

    cuts = 0
    path = []
    x, y = create_path(None, maze, path, int(MAZE_SIZE / 2), int(MAZE_SIZE / 2))

    while len(path) > 0:
        x, y = create_path(None, maze, path, x, y)
    while cuts < CUTS:
        create_cut(None, maze)
        cuts += 1
    to_file(maze)

def draw_box(surface, colour, x, y):
    if surface is not None:
        #pygame.draw.rect(surface, colour, (x * TILE_SIZE, y * TILE_SIZE,
        #        TILE_SIZE, TILE_SIZE))
        surface.fill(colour, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE,
                TILE_SIZE))

def draw_path(surface, path):
    x = int(MAZE_SIZE / 2)
    y = x
    for dirp in path:
        for i in range(WALL_SIZE + 1):
            x += dirp[0]
            y += dirp[1]
            draw_box(surface, (0, 0, 255), x, y)

def draw_screen(surface, maze):
    for i in range(MAZE_SIZE):
        for j in range(MAZE_SIZE):
            if maze[j][i] is 1:
                draw_box(surface, (255, 255, 255), i, j)

def to_file(maze):
    # add borders
    for i in range(1, BORDERS + 1):
        maze[i] = [0] + [1] * (MAZE_SIZE - 2) + [0]
        maze[-(i + 1)] = [0] + [1] * (MAZE_SIZE - 2) + [0]
        for line in maze[1:-2]:
            line[i] = 1
            line[-(i + 1)] = 1
    # create output string
    string = "\n".join(["".join([str(bit) for bit in line]) for line in maze])\
            .replace('0', WALL_CHAR).replace('1', PATH_CHAR)
    # write
    with open("maze.txt", 'w') as f:
        f.write(string)

if __name__ == "__main__":
    start = time.time()
    if len(sys.argv) > 1 and sys.argv[1] == "visual":
        if len(sys.argv) > 2:
            visual(int(sys.argv[2]))
        else:
            visual()
    else:
        gen()
    raw_input()
    print '\nGenerated in %dms' % (1000 * (time.time() - start))
