
def grid_coord_valid(grid: list[list[any]], x: int, y: int) -> bool:
    return x >= 0 and y >= 0 and x < len(grid[0]) and y < len(grid)

def grid_get(grid: list[list[any]], x: int, y: int) -> any:
    return grid[len(grid)-1-y][x]

def grid_set(grid: list[list[any]], x: int, y: int, value: any) -> None:
    grid[len(grid)-1-y][x] = value

def grid_x(grid: list[list[any]]) -> int:
    return len(grid[0])

def grid_y(grid: list[list[any]]) -> int:
    return len(grid)

def grid_get_mask(grid: list[list[any]], x: int, y: int, mask: int) -> bool:
    return (grid_get(grid, x, y) & mask) == mask

def grid_set_mask(grid: list[list[any]], x: int, y: int, mask: int) -> None:
    grid_set(grid, x, y, grid_get(grid, x, y) | mask)
