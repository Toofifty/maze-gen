import pygame
import random
import time, thread
from pygame.locals import *

# total maze size (height and width)
MAZE_SIZE = 151
# wall thickness (best at 1)
WALL_SIZE = 1
# amount of cut/loops
CUTS = 0

TILE_SIZE = 4

WALL_CHAR = '#'
EMPTY_CHAR = '_'

# directions, in order from 0-3 (u, r, d, l)
DIR_SET = [[0, 1], [1, 0], [0, -1], [-1, 0]]

# initialize pygame and objects
pygame.init()
pygame.display.set_caption("Monster AI Prototype")
screen = pygame.display.set_mode((MAZE_SIZE * TILE_SIZE, MAZE_SIZE * TILE_SIZE))
clock = pygame.time.Clock()
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))

# maze: bit array of current maze
# last_dir: direction last moved (0-3)
# clen: current length of _straight_ path
# x, y: coords of new path
def draw_next_path(surface, maze, last_dir, clen, x, y):
    maze[y][x] = 1
    valid_dirs = []
    for i in range(0, len(DIR_SET)):
        # check bounds
        if y + DIR_SET[i][1] * 2 >= MAZE_SIZE \
                or y + DIR_SET[i][1] * 2 < 0 \
                or x + DIR_SET[i][0] * 2 >= MAZE_SIZE \
                or x + DIR_SET[i][0] * 2 < 0: \
            continue
        # check if there is a path in 2 blocks in any direction
        if maze[y + DIR_SET[i][1]*2][x + DIR_SET[i][0]*2] == 0:
            valid_dirs.append(i)
        # elif random.random() > 0.999:
        #     valid_dirs.append(i)

    # dead end may have been found
    if len(valid_dirs) == 0:
        # look for ways to backtrack to the sides
        for i in range(len(DIR_SET)):
            if y + DIR_SET[i][1] >= MAZE_SIZE \
                    or y + DIR_SET[i][1] < 0 \
                    or x + DIR_SET[i][0] >= MAZE_SIZE \
                    or x + DIR_SET[i][0] < 0: \
                continue

            if maze[y + DIR_SET[i][1] * 1][x + DIR_SET[i][0] * 1] == 1:
                valid_dirs.append(i)

    # couldn't backtrack to the sides, need to change direction
    if len(valid_dirs) == 0:
        new_dir = (last_dir + 2) % 4
    else:
        new_dir = random.choice(valid_dirs)
        if clen % (WALL_SIZE + 1) is not 0:
            # must continue in the same direction
            new_dir = last_dir

    d_dir = DIR_SET[new_dir]
    nx = x + d_dir[0]
    ny = y + d_dir[1]
    pygame.draw.rect(surface, (0, 255, 0), (x * TILE_SIZE, y * TILE_SIZE,
            TILE_SIZE, TILE_SIZE))
    clen = clen + 1 if new_dir is last_dir else 1
    return new_dir, clen, nx, ny

def gen(maze):

    x = int(len(maze) / 2)
    y = x
    new_dir = random.choice([0, 1, 2, 3])
    clen = 0
    x1 = x + int(MAZE_SIZE / 4)
    y1 = y - int(MAZE_SIZE / 4)
    new_dir1 = new_dir
    clen1 = clen

    while True:
        new_dir, clen, x, y = draw_next_path(background, maze, new_dir, clen, x, y)
        #new_dir1, clen1, x1, y1 = draw_next_path(background, maze, new_dir1, clen1, x1, y1)

def main():
    # main maze array
    maze = [[0] * MAZE_SIZE for i in range(MAZE_SIZE)]
    exit = False

    thread.start_new_thread(gen, (maze,))

    while not exit:
        clock.tick(1)
        screen.blit(background, (0, 0))
        draw_screen(background, maze)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                    event.key == K_ESCAPE):
                return

def draw_screen(surface, maze):
    for i in range(MAZE_SIZE):
        for j in range(MAZE_SIZE):
            col = (0, 0, 0) if maze[j][i] is 1 else (255, 255, 255)
            pygame.draw.rect(surface, col, (i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE))

if __name__ == "__main__":
    main()
