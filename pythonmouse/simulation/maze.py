
from micromouse import NORTH_MASK, EAST_MASK, SOUTH_MASK, WEST_MASK
from grid import grid_set_mask, grid_coord_valid

MAZE_X = 16
MAZE_Y = 16

DEFAULT_MAZE = [
    [0x09,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x03],
    [0x0A,0x09,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x01,0x05,0x05,0x05,0x05,0x02],
    [0x0A,0x0A,0x09,0x05,0x05,0x05,0x01,0x05,0x07,0x0D,0x04,0x01,0x05,0x05,0x03,0x0A],
    [0x0A,0x0A,0x0A,0x0B,0x09,0x03,0x0C,0x05,0x03,0x0B,0x09,0x06,0x09,0x05,0x06,0x0A],
    [0x0A,0x0A,0x0A,0x08,0x06,0x0A,0x09,0x03,0x0C,0x02,0x0A,0x0D,0x04,0x05,0x03,0x0A],
    [0x0A,0x0A,0x0A,0x0C,0x03,0x0A,0x0A,0x0C,0x03,0x0C,0x06,0x09,0x05,0x05,0x06,0x0A],
    [0x0A,0x0A,0x0C,0x05,0x06,0x0A,0x0A,0x0D,0x04,0x05,0x03,0x0C,0x05,0x03,0x0B,0x0A],
    [0x0A,0x0A,0x09,0x03,0x0D,0x02,0x0A,0x09,0x01,0x03,0x0C,0x05,0x05,0x06,0x0A,0x0A],
    [0x0A,0x0A,0x0A,0x0C,0x03,0x0A,0x0A,0x0C,0x06,0x0C,0x01,0x07,0x09,0x01,0x02,0x0A],
    [0x0A,0x0A,0x0A,0x09,0x06,0x08,0x06,0x0D,0x01,0x03,0x0C,0x03,0x0A,0x0E,0x0A,0x0A],
    [0x0A,0x0A,0x0A,0x0C,0x05,0x06,0x09,0x03,0x0A,0x0C,0x03,0x0C,0x00,0x05,0x02,0x0A],
    [0x0A,0x0A,0x0C,0x05,0x05,0x03,0x0A,0x0A,0x0C,0x03,0x0C,0x03,0x0C,0x03,0x0A,0x0A],
    [0x0A,0x0A,0x09,0x05,0x05,0x06,0x0A,0x0A,0x0D,0x04,0x03,0x0C,0x03,0x0C,0x02,0x0A],
    [0x08,0x02,0x0A,0x0D,0x05,0x05,0x02,0x0A,0x0D,0x05,0x04,0x03,0x0C,0x03,0x0A,0x0A],
    [0x0A,0x0A,0x0C,0x05,0x05,0x05,0x06,0x0C,0x05,0x05,0x05,0x06,0x0D,0x04,0x06,0x0A],
    [0x0E,0x0C,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x05,0x06],
]

def load_maze(path) -> list[list[int]]:
    maze = [
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
        [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
    ]
    with open(path, 'r') as f:
        for y in range(MAZE_Y-1, -1, -1):
            line = f.readline()
            # top of cell
            x = 0
            for i in range(2, 64, 4):
                if line[i] == '-':
                    grid_set_mask(maze, x, y, NORTH_MASK)
                    if grid_coord_valid(maze, x, y+1):
                        grid_set_mask(maze, x, y+1, SOUTH_MASK)
                x += 1
            line = f.readline()
            # middle of cell
            x = 0
            if line[0] == '|':
                grid_set_mask(maze, x, y, WEST_MASK)
                if grid_coord_valid(maze, x-1, y):
                    grid_set_mask(maze, x-1, y, EAST_MASK)
            for i in range(4, 65, 4):
                if line[i] == '|':
                    grid_set_mask(maze, x, y, EAST_MASK)
                    if grid_coord_valid(maze, x+1, y):
                        grid_set_mask(maze, x+1, y, WEST_MASK)
                x += 1
#            print(maze)
#            exit()
    return maze
