import logging

from constants import MAZE
from grid import grid_x, grid_y, grid_get, grid_set, grid_coord_valid, grid_check_mask

FLOOD_EMPTY = -1

NORTH_MASK = 0x01
EAST_MASK = 0x02
SOUTH_MASK = 0x04
WEST_MASK = 0x08

NORTH_CHECKED_MASK = 0x10
EAST_CHECKED_MASK = 0x20
SOUTH_CHECKED_MASK = 0x40
WEST_CHECKED_MASK = 0x80

MOUSE_STATE_PROCESSING = 1
MOUSE_STATE_MOVING = 2

MOUSE_MODE_SEARCH_1 = 1
MOUSE_MODE_RETURN_TO_START_1 = 2
MOUSE_MODE_SEARCH_2 = 3
MOUSE_MODE_RETURN_TO_START_2 = 4
MOUSE_MODE_FAST_RUN = 5

class Mouse():
    width = 8
    height = 10
    """Represents the micromouse"""
    def __init__(self):
        self.location = (0,0)
        self.facing = NORTH_MASK
        self.state = MOUSE_STATE_PROCESSING
        self.mode = MOUSE_MODE_SEARCH_1
        self.map = [
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
        self.routes = [] # TODO: real mouse would onylcare about the best route but simulation wants to show multiple options
    def flood_map(self, targets: list[tuple]):
        # clear
        for x in range(grid_x(self.flood)):
            for y in range(grid_y(self.flood)):
                grid_set(self.flood, x, y, FLOOD_EMPTY)
        # set target
        for target in targets:
            grid_set(self.flood, target[0], target[1], 0)
            self.queue.append(target)
        # flood
        while len(self.queue) > 0:
            coord = self.queue.pop(0)
            score = grid_get(self.flood, coord[0], coord[1])
            x = coord[0]
            y = coord[1]+1
            if grid_coord_valid(self.flood, x, y) and not self.wall_north(coord[0], coord[1]):
                if grid_get(self.flood, x, y) == FLOOD_EMPTY:
                    grid_set(self.flood, x, y, score+1)
                    self.queue.append((x, y))
            x = coord[0]+1
            y = coord[1]
            if grid_coord_valid(self.flood, x, y) and not self.wall_east(coord[0], coord[1]):
                if grid_get(self.flood, x, y) == FLOOD_EMPTY:
                    grid_set(self.flood, x, y, score+1)
                    self.queue.append((x, y))
            x = coord[0]
            y = coord[1]-1
            if grid_coord_valid(self.flood, x, y) and not self.wall_south(coord[0], coord[1]):
                if grid_get(self.flood, x, y) == FLOOD_EMPTY:
                    grid_set(self.flood, x, y, score+1)
                    self.queue.append((x, y))
            x = coord[0]-1
            y = coord[1]
            if grid_coord_valid(self.flood, x, y) and not self.wall_west(coord[0], coord[1]):
                if grid_get(self.flood, x, y) == FLOOD_EMPTY:
                    grid_set(self.flood, x, y, score+1)
                    self.queue.append((x, y))
    def tick(self):
        logging.debug('mouse tick')
        if self.state == MOUSE_STATE_PROCESSING:
            changes = self.scan()
            if changes:
                self.flood_map(self.current_targets)
                self.routes = self.generate_best_routes_for_origin()
            self.state = MOUSE_STATE_MOVING
        elif self.state == MOUSE_STATE_MOVING:
            self.move()
            self.state = MOUSE_STATE_PROCESSING

        if self.mode == MOUSE_MODE_SEARCH_1:
            logging.info('search 1')
            if grid_get(self.flood, self.location[0], self.location[1]) == 0:
                self.mode = MOUSE_MODE_RETURN_TO_START_1
                self.current_origin = self.location
                self.current_targets = [self.start_target]
                self.flood_map(self.current_targets)
        elif self.mode == MOUSE_MODE_RETURN_TO_START_1:
            logging.info('return to start 1')
            if grid_get(self.flood, self.location[0], self.location[1]) == 0:
                self.mode = MOUSE_MODE_SEARCH_2
                self.current_origin = self.start_target
                self.current_targets = self.goal_targets
                self.flood_map(self.current_targets)
        elif self.mode == MOUSE_MODE_SEARCH_2:
            logging.info('search 2')
            if grid_get(self.flood, self.location[0], self.location[1]) == 0:
                self.mode = MOUSE_MODE_RETURN_TO_START_2
                self.current_origin = self.location
                self.current_targets = [self.start_target]
                self.flood_map(self.current_targets)
        elif self.mode == MOUSE_MODE_RETURN_TO_START_2:
            logging.info('return to start 2')
            if grid_get(self.flood, self.location[0], self.location[1]) == 0:
                self.mode = MOUSE_MODE_FAST_RUN
                self.current_origin = self.start_target
                self.current_targets = self.goal_targets
                self.flood_map(self.current_targets)
        elif self.mode == MOUSE_MODE_FAST_RUN:
            logging.info('fast run')
            # TODO: should use optimal route
            pass
    def get_routes(self):
        return self.routes
    def generate_routes(self, origin, depth, limit):
        routes = []
        route = []
        current_loc = origin
        current_dir = None
        current_score = 0
        required_val = grid_get(self.flood, current_loc[0], current_loc[1])
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
                                sub_routes = self.generate_routes(direction['coord'], depth+1, limit)
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
    def generate_best_routes_for_origin(self):
        routes = self.generate_routes(self.current_origin, 0, 8)
        filtered_routes = []
        # check for completed routes
        for route in routes:
            coord = route['route'][-1]
            if grid_get(self.flood, coord[0], coord[1]) == 0:
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
    def scan(self) -> int:
        logging.debug("check for walls")
        changes = 0
        if self.facing == NORTH_MASK:
            changes += self.scan_west(self.location[0], self.location[1])
            changes += self.scan_north(self.location[0], self.location[1])
            changes += self.scan_east(self.location[0], self.location[1])
        if self.facing == EAST_MASK:
            changes += self.scan_north(self.location[0], self.location[1])
            changes += self.scan_east(self.location[0], self.location[1])
            changes += self.scan_south(self.location[0], self.location[1])
        if self.facing == SOUTH_MASK:
            changes += self.scan_east(self.location[0], self.location[1])
            changes += self.scan_south(self.location[0], self.location[1])
            changes += self.scan_west(self.location[0], self.location[1])
        if self.facing == WEST_MASK:
            changes += self.scan_south(self.location[0], self.location[1])
            changes += self.scan_west(self.location[0], self.location[1])
            changes += self.scan_north(self.location[0], self.location[1])
        return changes
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
    def scan_north(self, x: int, y :int) -> int:
        if grid_get(self.map, x, y) & NORTH_CHECKED_MASK != NORTH_CHECKED_MASK:
            _x = x
            _y = y+1
            grid_set(self.map, x, y, grid_get(self.map, x, y) | NORTH_CHECKED_MASK)
            if grid_coord_valid(self.map, _x, _y):
                grid_set(self.map, _x, _y, grid_get(self.map, _x, _y) | SOUTH_CHECKED_MASK)
            if grid_get(MAZE, x, y) & NORTH_MASK == NORTH_MASK:
                grid_set(self.map, x, y, grid_get(self.map, x, y) | NORTH_MASK)
                if grid_coord_valid(self.map, _x, _y):
                    grid_set(self.map, _x, _y, grid_get(self.map, _x, _y) | SOUTH_MASK)
                return 1
        return 0
    def scan_east(self, x: int, y: int) -> int:
        if grid_get(self.map, x, y) & EAST_CHECKED_MASK != EAST_CHECKED_MASK:
            _x = x+1
            _y = y
            grid_set(self.map, x, y, grid_get(self.map, x, y) | EAST_CHECKED_MASK)
            if grid_coord_valid(self.map, _x, _y):
                grid_set(self.map, _x, _y, grid_get(self.map, _x, _y) | WEST_CHECKED_MASK)
            if grid_get(MAZE, x, y) & EAST_MASK == EAST_MASK:
                grid_set(self.map, x, y, grid_get(self.map, x, y) | EAST_MASK)
                if grid_coord_valid(self.map, _x, _y):
                    grid_set(self.map, _x, _y, grid_get(self.map, _x, _y) | WEST_MASK)
                return 1
        return 0
    def scan_south(self, x: int, y :int) -> int:
        if grid_get(self.map, x, y) & SOUTH_CHECKED_MASK != SOUTH_CHECKED_MASK:
            _x = x
            _y = y-1
            grid_set(self.map, x, y, grid_get(self.map, x, y) | SOUTH_CHECKED_MASK)
            if grid_coord_valid(self.map, _x, _y):
                grid_set(self.map, _x, _y, grid_get(self.map, _x, _y) | NORTH_CHECKED_MASK)
            if grid_get(MAZE, x, y) & SOUTH_MASK == SOUTH_MASK:
                grid_set(self.map, x, y, grid_get(self.map, x, y) | SOUTH_MASK)
                if grid_coord_valid(self.map, _x, _y):
                    grid_set(self.map, _x, _y, grid_get(self.map, _x, _y) | NORTH_MASK)
                return 1
        return 0
    def scan_west(self, x: int, y: int) -> int:
        if grid_get(self.map, x, y) & WEST_CHECKED_MASK != WEST_CHECKED_MASK:
            _x = x-1
            _y = y
            grid_set(self.map, x, y, grid_get(self.map, x, y) | WEST_CHECKED_MASK)
            if grid_coord_valid(self.map, _x, _y):
                grid_set(self.map, _x, _y, grid_get(self.map, _x, _y) | EAST_CHECKED_MASK)
            if grid_get(MAZE, x, y) & WEST_MASK == WEST_MASK:
                grid_set(self.map, x, y, grid_get(self.map, x, y) | WEST_MASK)
                if grid_coord_valid(self.map, _x, _y):
                    grid_set(self.map, _x, _y, grid_get(self.map, _x, _y) | EAST_MASK)
                return 1
        return 0
    def check_north(self, x: int, y: int):
        # check north
        _x = x
        _y = y+1
        if grid_coord_valid(self.map, _x, _y) and not self.wall_north(x,y): # TODO: do we need to check walls?
            num = grid_get(self.flood, _x, _y)
            return {'value': num, 'coord':(_x,_y), 'dir':NORTH_MASK}
        return None
    def check_east(self, x: int, y: int):
        # check east
        _x = x+1
        _y = y
        if grid_coord_valid(self.map, _x, _y) and not self.wall_east(x,y): # TODO: do we need to check walls?
            num = grid_get(self.flood, _x, _y)
            return {'value': num, 'coord':(_x,_y), 'dir':EAST_MASK}
        return None
    def check_south(self, x: int, y: int):
        # check south
        _x = x
        _y = y-1
        if grid_coord_valid(self.map, _x, _y) and not self.wall_south(x,y): # TODO: do we need to check walls?
            num = grid_get(self.flood, _x, _y)
            return {'value': num, 'coord':(_x,_y), 'dir':SOUTH_MASK}
        return None
    def check_west(self, x: int, y: int):
        # check west
        _x = x-1
        _y = y
        if grid_coord_valid(self.map, _x, _y) and not self.wall_west(x,y): # TODO: do we need to check walls?
            num = grid_get(self.flood, _x, _y)
            return {'value': num, 'coord':(_x,_y), 'dir':WEST_MASK}
        return None
    def wall_north(self, x, y):
        return grid_check_mask(self.map, x, y, NORTH_MASK)
    def wall_east(self, x, y):
        return grid_check_mask(self.map, x, y, EAST_MASK)
    def wall_south(self, x, y):
        return grid_check_mask(self.map, x, y, SOUTH_MASK)
    def wall_west(self, x, y):
        return grid_check_mask(self.map, x, y, WEST_MASK)
