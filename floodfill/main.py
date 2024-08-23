import argparse
import logging
import pygame
import time

NORTH_MASK = 0x01
EAST_MASK = 0x02
SOUTH_MASK = 0x04
WEST_MASK = 0x08

NORTH_CHECKED_MASK = 0x10
EAST_CHECKED_MASK = 0x20
SOUTH_CHECKED_MASK = 0x40
WEST_CHECKED_MASK = 0x80

SCALE = 2

CELL_SIZE = 18

MOUSE_STATE_SCAN = 1
MOUSE_STATE_FLOOD = 2
MOUSE_STATE_MOVE = 3

MOUSE_MODE_SEARCH_1 = 1
MOUSE_MODE_RETURN_TO_START_1 = 2
MOUSE_MODE_SEARCH_2 = 3
MOUSE_MODE_RETURN_TO_START_2 = 4
MOUSE_MODE_FAST_RUN = 5

FLOOD_EMPTY = -1

MAZE_X = 16
MAZE_Y = 16
MAZE = [
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

def grid_coord_valid(grid: list[list], x: int, y: int):
    return x >= 0 and y >= 0 and x < len(grid[0]) and y < len(grid)

def grid_coord_get(grid: list[list], x: int, y: int):
    return grid[len(grid)-1-y][x]

def grid_coord_set(grid: list[list], x: int, y: int, value):
    grid[len(grid)-1-y][x] = value

def grid_x(grid: list[list]):
    return len(grid[0])

def grid_y(grid: list[list]):
    return len(grid)

def grid_check_mask(grid: list[list], x: int, y: int, mask: int):
    return (grid_coord_get(grid, x, y) & mask) == mask

# TODO: implement queue?

class Mouse():
    width = 8
    height = 10
    """Represents the micromouse"""
    def __init__(self):
        self.location = (0,0)
        self.facing = NORTH_MASK
        self.state = MOUSE_STATE_SCAN
        self.mode = MOUSE_MODE_SEARCH_1
        self.cells = [
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
        self.flood = [
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
            [FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY,FLOOD_EMPTY],
        ]
        self.queue = []
        self.start_target = (0,0)
        self.goal_targets = [(7,7),(7,8),(8,7),(8,8)]
        self.current_origin = self.start_target
        self.current_targets = self.goal_targets
    def flood_map(self, targets: list[tuple]):
        # clear
        for x in range(grid_x(self.flood)):
            for y in range(grid_y(self.flood)):
                grid_coord_set(self.flood, x, y, FLOOD_EMPTY)
        # set target
        for target in targets:
            grid_coord_set(self.flood, target[0], target[1], 0)
            self.queue.append(target)
        # flood
        while len(self.queue) > 0:
            coord = self.queue.pop(0)
            score = grid_coord_get(self.flood, coord[0], coord[1])
            x = coord[0]
            y = coord[1]+1
            if grid_coord_valid(self.flood, x, y) and not self.wall_north(coord[0], coord[1]):
                if grid_coord_get(self.flood, x, y) == FLOOD_EMPTY:
                    grid_coord_set(self.flood, x, y, score+1)
                    self.queue.append((x, y))
            x = coord[0]+1
            y = coord[1]
            if grid_coord_valid(self.flood, x, y) and not self.wall_east(coord[0], coord[1]):
                if grid_coord_get(self.flood, x, y) == FLOOD_EMPTY:
                    grid_coord_set(self.flood, x, y, score+1)
                    self.queue.append((x, y))
            x = coord[0]
            y = coord[1]-1
            if grid_coord_valid(self.flood, x, y) and not self.wall_south(coord[0], coord[1]):
                if grid_coord_get(self.flood, x, y) == FLOOD_EMPTY:
                    grid_coord_set(self.flood, x, y, score+1)
                    self.queue.append((x, y))
            x = coord[0]-1
            y = coord[1]
            if grid_coord_valid(self.flood, x, y) and not self.wall_west(coord[0], coord[1]):
                if grid_coord_get(self.flood, x, y) == FLOOD_EMPTY:
                    grid_coord_set(self.flood, x, y, score+1)
                    self.queue.append((x, y))
    def tick(self):
        logging.debug('mouse tick')
        if self.state == MOUSE_STATE_SCAN:
            self.scan()
            self.state = MOUSE_STATE_FLOOD
        elif self.state == MOUSE_STATE_FLOOD:
            self.flood_map(self.current_targets)
            self.state = MOUSE_STATE_MOVE
        elif self.state == MOUSE_STATE_MOVE:
            self.move()
            self.state = MOUSE_STATE_SCAN
        if self.mode == MOUSE_MODE_SEARCH_1:
            print('search 1')
            if grid_coord_get(self.flood, self.location[0], self.location[1]) == 0:
                self.mode = MOUSE_MODE_RETURN_TO_START_1
                self.current_origin = self.location
                self.current_targets = [self.start_target]
                self.flood_map(self.current_targets)
        elif self.mode == MOUSE_MODE_RETURN_TO_START_1:
            print('return to start 1')
            if grid_coord_get(self.flood, self.location[0], self.location[1]) == 0:
                self.mode = MOUSE_MODE_SEARCH_2
                self.current_origin = self.start_target
                self.current_targets = self.goal_targets
                self.flood_map(self.current_targets)
        elif self.mode == MOUSE_MODE_SEARCH_2:
            print('search 2')
            if grid_coord_get(self.flood, self.location[0], self.location[1]) == 0:
                self.mode = MOUSE_MODE_RETURN_TO_START_2
                self.current_origin = self.location
                self.current_targets = [self.start_target]
                self.flood_map(self.current_targets)
        elif self.mode == MOUSE_MODE_RETURN_TO_START_2:
            print('return to start 2')
            if grid_coord_get(self.flood, self.location[0], self.location[1]) == 0:
                self.mode = MOUSE_MODE_FAST_RUN
                self.current_origin = self.start_target
                self.current_targets = self.goal_targets
                self.flood_map(self.current_targets)
        elif self.mode == MOUSE_MODE_FAST_RUN:
            print('fast run')
            # TODO: should use optimal route
            pass
    def get_routes_for_current_origin(self):
        routes = self.get_routes(self.current_origin, 0, 8)
        filtered_routes = []
        # check for completed routes
        for route in routes:
            coord = route['route'][-1]
            if grid_coord_get(self.flood, coord[0], coord[1]) == 0:
                filtered_routes.append(route)
        if len(filtered_routes) == 0:
            # no completed routes
            return [r['route'] for r in routes]
        elif len(filtered_routes) == 1:
            # single complete route
            return [r['route'] for r in filtered_routes]
        else:
            # multiple complete routes
            filtered_routes.sort(key=lambda x: x['score'], reverse=False) # sort ascending
            return [filtered_routes[0]['route']]
    def get_routes(self, origin, depth, limit):
        routes = []
        route = []
        current_loc = origin
        current_dir = None
        current_score = 0
        required_val = grid_coord_get(self.flood, current_loc[0], current_loc[1])
        while current_loc:
            route.append(current_loc)
            directions = self.get_directions(current_loc[0], current_loc[1])
            required_val = required_val - 1
            if len(directions) == 0:
                # no directions
                current_loc = None
                current_dir = None
                routes.append({'score':current_score,'route':route})
            elif len(directions) == 1:
                # single direction
                if directions[0]['value'] == required_val:
                    # correct value
                    current_loc = directions[0]['coord']
                    if current_dir != directions[0]['dir']:
                        current_score+=1
                    current_dir = directions[0]['dir']
                else:
                    # wrong value
                    current_loc = None
                    current_dir = None
                    routes.append({'score':current_score,'route':route})
            else:
                # multiple directions
                if directions[0]['value'] == directions[1]['value']:
                    # multiple routes
                    if depth < limit and directions[0]['value'] == required_val:
                        current_loc = None
                        current_dir = None
                        # correct value
                        for direction in directions:
                            if directions[0]['value'] == direction['value']:
                                sub_routes = self.get_routes(direction['coord'], depth+1, limit)
                                for sub_route in sub_routes:
                                    routes.append({'score':current_score+sub_route['score'],'route':route+sub_route['route']})
                    else:
                        # wrong value
                        current_loc = None
                        current_dir = None
                        routes.append({'score':current_score,'route':route})
                else:
                    # single route
                    if directions[0]['value'] == required_val:
                        # correct value
                        current_loc = directions[0]['coord']
                        if current_dir != directions[0]['dir']:
                            current_score+=1
                        current_dir = directions[0]['dir']
                    else:
                        # wrong value
                        current_loc = None
                        current_dir = None
                        routes.append({'score':current_score,'route':route})
        return routes
    def scan(self):
        logging.debug("check for walls")
        if self.facing == NORTH_MASK:
            self.scan_west(self.location[0], self.location[1])
            self.scan_north(self.location[0], self.location[1])
            self.scan_east(self.location[0], self.location[1])
        if self.facing == EAST_MASK:
            self.scan_north(self.location[0], self.location[1])
            self.scan_east(self.location[0], self.location[1])
            self.scan_south(self.location[0], self.location[1])
        if self.facing == SOUTH_MASK:
            self.scan_east(self.location[0], self.location[1])
            self.scan_south(self.location[0], self.location[1])
            self.scan_west(self.location[0], self.location[1])
        if self.facing == WEST_MASK:
            self.scan_south(self.location[0], self.location[1])
            self.scan_west(self.location[0], self.location[1])
            self.scan_north(self.location[0], self.location[1])
    def get_directions(self, x: int, y: int):
        directions = []
        dir = self.check_north(x, y)
        if dir:
            directions.append(dir)
        dir = self.check_east(x, y)
        if dir:
            directions.append(dir)
        dir = self.check_south(x, y)
        if dir:
            directions.append(dir)
        dir = self.check_west(x, y)
        if dir:
            directions.append(dir)
        if len(directions) == 0:
            raise Exception("No direction")
        directions.sort(key=lambda x: x['value'], reverse=False) # sort ascending
        return directions
    def move(self):
        logging.debug("move")
        directions = self.get_directions(self.location[0], self.location[1])
        direction = directions[0]
        if direction['dir'] != self.facing:
            self.facing = direction['dir']
        self.location = direction['coord']
    def scan_north(self, x: int, y :int):
        if grid_coord_get(self.cells, x, y) & NORTH_CHECKED_MASK != NORTH_CHECKED_MASK:
            _x = x
            _y = y+1
            grid_coord_set(self.cells, x, y, grid_coord_get(self.cells, x, y) | NORTH_CHECKED_MASK)
            if grid_coord_valid(self.cells, _x, _y):
                grid_coord_set(self.cells, _x, _y, grid_coord_get(self.cells, _x, _y) | SOUTH_CHECKED_MASK)
            if grid_coord_get(MAZE, x, y) & NORTH_MASK == NORTH_MASK:
                grid_coord_set(self.cells, x, y, grid_coord_get(self.cells, x, y) | NORTH_MASK)
                if grid_coord_valid(self.cells, _x, _y):
                    grid_coord_set(self.cells, _x, _y, grid_coord_get(self.cells, _x, _y) | SOUTH_MASK)
    def scan_east(self, x: int, y: int):
        if grid_coord_get(self.cells, x, y) & EAST_CHECKED_MASK != EAST_CHECKED_MASK:
            _x = x+1
            _y = y
            grid_coord_set(self.cells, x, y, grid_coord_get(self.cells, x, y) | EAST_CHECKED_MASK)
            if grid_coord_valid(self.cells, _x, _y):
                grid_coord_set(self.cells, _x, _y, grid_coord_get(self.cells, _x, _y) | WEST_CHECKED_MASK)
            if grid_coord_get(MAZE, x, y) & EAST_MASK == EAST_MASK:
                grid_coord_set(self.cells, x, y, grid_coord_get(self.cells, x, y) | EAST_MASK)
                if grid_coord_valid(self.cells, _x, _y):
                    grid_coord_set(self.cells, _x, _y, grid_coord_get(self.cells, _x, _y) | WEST_MASK)
    def scan_south(self, x: int, y :int):
        if grid_coord_get(self.cells, x, y) & SOUTH_CHECKED_MASK != SOUTH_CHECKED_MASK:
            _x = x
            _y = y-1
            grid_coord_set(self.cells, x, y, grid_coord_get(self.cells, x, y) | SOUTH_CHECKED_MASK)
            if grid_coord_valid(self.cells, _x, _y):
                grid_coord_set(self.cells, _x, _y, grid_coord_get(self.cells, _x, _y) | NORTH_CHECKED_MASK)
            if grid_coord_get(MAZE, x, y) & SOUTH_MASK == SOUTH_MASK:
                grid_coord_set(self.cells, x, y, grid_coord_get(self.cells, x, y) | SOUTH_MASK)
                if grid_coord_valid(self.cells, _x, _y):
                    grid_coord_set(self.cells, _x, _y, grid_coord_get(self.cells, _x, _y) | NORTH_MASK)
    def scan_west(self, x: int, y: int):
        if grid_coord_get(self.cells, x, y) & WEST_CHECKED_MASK != WEST_CHECKED_MASK:
            _x = x-1
            _y = y
            grid_coord_set(self.cells, x, y, grid_coord_get(self.cells, x, y) | WEST_CHECKED_MASK)
            if grid_coord_valid(self.cells, _x, _y):
                grid_coord_set(self.cells, _x, _y, grid_coord_get(self.cells, _x, _y) | EAST_CHECKED_MASK)
            if grid_coord_get(MAZE, x, y) & WEST_MASK == WEST_MASK:
                grid_coord_set(self.cells, x, y, grid_coord_get(self.cells, x, y) | WEST_MASK)
                if grid_coord_valid(self.cells, _x, _y):
                    grid_coord_set(self.cells, _x, _y, grid_coord_get(self.cells, _x, _y) | EAST_MASK)
    def check_north(self, x: int, y: int):
        # check north
        _x = x
        _y = y+1
        if grid_coord_valid(self.cells, _x, _y) and not self.wall_north(x,y): # TODO: do we need to check walls?
            num = grid_coord_get(self.flood, _x, _y)
            return {'value': num, 'coord':(_x,_y), 'dir':NORTH_MASK}
        return None
    def check_east(self, x: int, y: int):
        # check east
        _x = x+1
        _y = y
        if grid_coord_valid(self.cells, _x, _y) and not self.wall_east(x,y): # TODO: do we need to check walls?
            num = grid_coord_get(self.flood, _x, _y)
            return {'value': num, 'coord':(_x,_y), 'dir':EAST_MASK}
        return None
    def check_south(self, x: int, y: int):
        # check south
        _x = x
        _y = y-1
        if grid_coord_valid(self.cells, _x, _y) and not self.wall_south(x,y): # TODO: do we need to check walls?
            num = grid_coord_get(self.flood, _x, _y)
            return {'value': num, 'coord':(_x,_y), 'dir':SOUTH_MASK}
        return None
    def check_west(self, x: int, y: int):
        # check west
        _x = x-1
        _y = y
        if grid_coord_valid(self.cells, _x, _y) and not self.wall_west(x,y): # TODO: do we need to check walls?
            num = grid_coord_get(self.flood, _x, _y)
            return {'value': num, 'coord':(_x,_y), 'dir':WEST_MASK}
        return None
    def wall_north(self, x, y):
        return grid_check_mask(self.cells, x, y, NORTH_MASK)
    def wall_east(self, x, y):
        return grid_check_mask(self.cells, x, y, EAST_MASK)
    def wall_south(self, x, y):
        return grid_check_mask(self.cells, x, y, SOUTH_MASK)
    def wall_west(self, x, y):
        return grid_check_mask(self.cells, x, y, WEST_MASK)

class App():
    """Runs the simulation"""
    def __init__(self):
        self._delay = 0.03

        self.mouse = Mouse()

        self._running = True
        self._display_surf = None
        self._width = CELL_SIZE * MAZE_X * SCALE
        self._height = CELL_SIZE * MAZE_Y * SCALE
        self._size = (self._width, self._height)
        self._time = time.time()
        self._counter = 0
        self._complete = False
    def on_init(self) -> bool:
        """On init"""
        pygame.init()
        pygame.display.set_caption("Title")
        self._display_surf = pygame.display.set_mode(self._size,
                                                     pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        
        font_name = pygame.font.get_default_font()
        logging.info("System font: %s", font_name)
        self.font = pygame.font.SysFont(None, 22)
        return True
    def on_event(self, event: pygame.event.Event) -> None:
        """On event."""
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 27:
                self._running = False
        else:
            logging.debug(event)
    def on_loop(self, elapsed: float) -> None:
        """On loop."""
        self._counter+=elapsed
        if self._counter > self._delay:
            logging.info("tick")
            self._counter = 0
            if self._complete is False:
                self.mouse.tick()
    def on_render(self) -> None:
        """On render."""
        self._display_surf.fill((0,0,0))
        for x in range(grid_x(MAZE)):
            for y in range(grid_y(MAZE)):
                thickness = 1

                # render physical walls
                left = x*CELL_SIZE*SCALE
                right = left + (CELL_SIZE*SCALE) - 1
                top = self._height - (y*CELL_SIZE*SCALE) - (CELL_SIZE*SCALE)
                bot = top + (CELL_SIZE*SCALE) - 1

                if (grid_coord_get(MAZE, x, y) & NORTH_MASK) == NORTH_MASK:
                    colour = (80,0,0)
                    pygame.draw.line(self._display_surf, colour, (left,top), (right,top), thickness)
                if (grid_coord_get(MAZE, x, y) & EAST_MASK) == EAST_MASK:
                    colour = (80,0,0)
                    pygame.draw.line(self._display_surf, colour, (right,top), (right,bot), thickness)
                if (grid_coord_get(MAZE, x, y) & SOUTH_MASK) == SOUTH_MASK:
                    colour = (80,0,0)
                    pygame.draw.line(self._display_surf, colour, (right,bot), (left,bot), thickness)
                if (grid_coord_get(MAZE, x, y) & WEST_MASK) == WEST_MASK:
                    colour = (80,0,0)
                    pygame.draw.line(self._display_surf, colour, (left,bot), (left,top), thickness)
                
                # render detected walls
                moffset = 1
                mleft = left+moffset
                mright = right-moffset
                mtop = top+moffset
                mbot = bot-moffset
                if (grid_coord_get(self.mouse.cells, x, y) & NORTH_MASK) == NORTH_MASK:
                    colour = (255,0,0)
                    pygame.draw.line(self._display_surf, colour, (mleft,mtop), (mright,mtop), thickness)
                if (grid_coord_get(self.mouse.cells, x, y) & EAST_MASK) == EAST_MASK:
                    colour = (255,0,0)
                    pygame.draw.line(self._display_surf, colour, (mright,mtop), (mright,mbot), thickness)
                if (grid_coord_get(self.mouse.cells, x, y) & SOUTH_MASK) == SOUTH_MASK:
                    colour = (255,0,0)
                    pygame.draw.line(self._display_surf, colour, (mright,mbot), (mleft,mbot), thickness)
                if (grid_coord_get(self.mouse.cells, x, y) & WEST_MASK) == WEST_MASK:
                    colour = (255,0,0)
                    pygame.draw.line(self._display_surf, colour, (mleft,mbot), (mleft,mtop), thickness)

        # render mouse
        cl = self.mouse.location[0] * CELL_SIZE * SCALE
        ct = self._height - (self.mouse.location[1] * CELL_SIZE * SCALE) - (CELL_SIZE*SCALE)
        cr = cl + (CELL_SIZE*SCALE)
        cb = ct + (CELL_SIZE*SCALE)
        if self.mouse.facing == NORTH_MASK:
            l = (cl) + (CELL_SIZE*SCALE/2) - (self.mouse.width*SCALE/2)
            t = (ct) + (CELL_SIZE*SCALE/2) - (self.mouse.height*SCALE/2)
            w = self.mouse.width*SCALE
            h = self.mouse.height*SCALE
            d = 5 * SCALE
            if self.mouse.state == MOUSE_STATE_SCAN:
                pygame.draw.line(self._display_surf, (255,255,255), (cl,ct), (cl+d,ct+d), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cl+(CELL_SIZE*SCALE/2),ct), (cl+(CELL_SIZE*SCALE/2),ct+d), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cr,ct), (cr-d,ct+d), 1)
        if self.mouse.facing == EAST_MASK:
            l = (cl) + (CELL_SIZE*SCALE/2) - (self.mouse.height*SCALE/2)
            t = (ct) + (CELL_SIZE*SCALE/2) - (self.mouse.width*SCALE/2)
            w = self.mouse.height*SCALE
            h = self.mouse.width*SCALE
            d = 5 * SCALE
            if self.mouse.state == MOUSE_STATE_SCAN:
                pygame.draw.line(self._display_surf, (255,255,255), (cr,ct), (cr-d,ct+d), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cr,ct+(CELL_SIZE*SCALE/2)), (cr-d,ct+(CELL_SIZE*SCALE/2)), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cr,cb), (cr-d,cb-d), 1)
        if self.mouse.facing == SOUTH_MASK:
            l = (cl) + (CELL_SIZE*SCALE/2) - (self.mouse.width*SCALE/2)
            t = (ct) + (CELL_SIZE*SCALE/2) - (self.mouse.height*SCALE/2)
            w = self.mouse.width*SCALE
            h = self.mouse.height*SCALE
            d = 5 * SCALE
            if self.mouse.state == MOUSE_STATE_SCAN:
                pygame.draw.line(self._display_surf, (255,255,255), (cl,cb), (cl+d,cb-d), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cl+(CELL_SIZE*SCALE/2),cb), (cl+(CELL_SIZE*SCALE/2),cb-d), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cr,cb), (cr-d,cb-d), 1)
        if self.mouse.facing == WEST_MASK:
            l = (cl) + (CELL_SIZE*SCALE/2) - (self.mouse.height*SCALE/2)
            t = (ct) + (CELL_SIZE*SCALE/2) - (self.mouse.width*SCALE/2)
            w = self.mouse.height*SCALE
            h = self.mouse.width*SCALE
            d = 5 * SCALE
            if self.mouse.state == MOUSE_STATE_SCAN:
                pygame.draw.line(self._display_surf, (255,255,255), (cl,ct), (cl+d,ct+d), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cl,ct+(CELL_SIZE*SCALE/2)), (cl+d,ct+(CELL_SIZE*SCALE/2)), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cl,cb), (cl+d,cb-d), 1)
        if self.mouse.state == MOUSE_STATE_SCAN:
            colour = (255,0,0)
        if self.mouse.state == MOUSE_STATE_FLOOD:
            colour = (255,255,0)
        if self.mouse.state == MOUSE_STATE_MOVE:
            colour = (0,255,0)
        pygame.draw.rect(self._display_surf, colour, pygame.Rect((l,t), (w,h)), 0)
        
        # render flood values
        for x in range(grid_x(self.mouse.flood)):
            for y in range(grid_y(self.mouse.flood)):
                num = grid_coord_get(self.mouse.flood, x, y)
                img = self.font.render(str(num), True, (80,80,80))
                self._display_surf.blit(img, (x*CELL_SIZE*SCALE, self._height-(y*CELL_SIZE*SCALE)-(CELL_SIZE*SCALE)))

        routes = self.mouse.get_routes_for_current_origin()
        for route in routes:
            _r = None
            for r in route:
                if _r:
                    a = ((_r[0]*CELL_SIZE*SCALE)+(CELL_SIZE*SCALE/2),self._height - (_r[1] * CELL_SIZE * SCALE) - (CELL_SIZE*SCALE/2))
                    b = ((r[0]*CELL_SIZE*SCALE)+(CELL_SIZE*SCALE/2),self._height - (r[1] * CELL_SIZE * SCALE) - (CELL_SIZE*SCALE/2))
                    pygame.draw.line(self._display_surf, (255,255,255), a, b)
                _r = r

        # render cell coordinates
        #for x in range(grid_x(self.mouse.flood)):
        #    for y in range(grid_y(self.mouse.flood)):
        #        img = self.font.render(f"{x},{y}", True, (100,100,100))
        #        self._display_surf.blit(img, (x*CELL_SIZE*SCALE, self._height-(y*CELL_SIZE*SCALE)-(CELL_SIZE*SCALE)))

        pygame.display.update()
    def on_cleanup(self) -> None:
        """On cleanup."""
        pygame.quit()
    def on_execute(self) -> None:
        """On execute."""
        if self.on_init() is False:
            self._running = False
        while self._running:
            current = time.time()
            elapsed = current - self._time
            self._time = current
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(elapsed)
            self.on_render()
        self.on_cleanup()

if __name__ == '__main__':
    loglevels = [
        'DEBUG',
        'INFO',
        'WARNING',
        'ERROR',
        'CRITICAL'
    ]

    parser = argparse.ArgumentParser(description='pygame template')
    parser.add_argument('-l', '--logging', type=str, required=False, default='ERROR', dest='logging', choices=loglevels)
    args = parser.parse_args()

    loglevel = getattr(logging, args.logging, None)
    logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s %(name)s %(message)s')

    a = App()
    a.on_execute()