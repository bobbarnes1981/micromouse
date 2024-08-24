
def grid_coord_valid(grid: list[list], x: int, y: int):
    return x >= 0 and y >= 0 and x < len(grid[0]) and y < len(grid)

def grid_get(grid: list[list], x: int, y: int):
    return grid[len(grid)-1-y][x]

def grid_set(grid: list[list], x: int, y: int, value):
    grid[len(grid)-1-y][x] = value

def grid_x(grid: list[list]):
    return len(grid[0])

def grid_y(grid: list[list]):
    return len(grid)

def grid_check_mask(grid: list[list], x: int, y: int, mask: int):
    return (grid_get(grid, x, y) & mask) == mask
