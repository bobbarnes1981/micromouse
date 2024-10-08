import logging

from grid import grid_x, grid_y, grid_get, grid_set, grid_coord_valid, grid_get_mask, grid_set_mask

FLOOD_EMPTY = -1

NORTH_MASK = 0x01
EAST_MASK = 0x02
SOUTH_MASK = 0x04
WEST_MASK = 0x08

DIRECTION_F = 1
DIRECTION_R = 2
DIRECTION_B = 4
DIRECTION_L = 8

def decode_direction(direction: int) -> str:
    if direction == DIRECTION_F:
        return "F"
    if direction == DIRECTION_R:
        return "R"
    if direction == DIRECTION_B:
        return "B"
    if direction == DIRECTION_L:
        return "L"

NORTH_CHECKED_MASK = 0x10
EAST_CHECKED_MASK = 0x20
SOUTH_CHECKED_MASK = 0x40
WEST_CHECKED_MASK = 0x80

MOUSE_STATE_PROCESSING = 1
MOUSE_STATE_MOVING = 2
MOUSE_STATE_DONE = 3

MOUSE_MODE_SEARCH_1 = 1
MOUSE_MODE_RETURN_TO_START_1 = 2
MOUSE_MODE_SEARCH_2 = 3
MOUSE_MODE_RETURN_TO_START_2 = 4
MOUSE_MODE_FAST_RUN = 5
MOUSE_MODE_DONE = 6

class Mouse():
    width = 8
    height = 10
    """Represents the micromouse"""
    def __init__(self, maze):
        # Real mouse would not have direct access to maze but we need it for simulation
        self.maze = maze
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
        self.route_step = 0
        self.queue = []
        self.routes = [] # TODO: real mouse would only care about the best route but simulation wants to show multiple options
        self.start_target = (0,0)
        self.goal_targets = [(7,7),(7,8),(8,7),(8,8)]
        self.current_origin = None
        self.current_targets = None
        self.set_origin_and_targets(self.start_target, self.goal_targets)

    def set_origin_and_targets(self, origin: tuple, targets: list[tuple]):
        """Set the current origin and targets, used for route planning"""
        self.current_origin = origin
        self.current_targets = targets
        self.flood_map(self.current_targets)
        self.routes = self.generate_best_routes_for_origin()

    def flood_map(self, targets: list[tuple]):
        """Flood the map"""
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
            if grid_coord_valid(self.flood, x, y) and not self.get_wall(coord, NORTH_MASK):
                if grid_get(self.flood, x, y) == FLOOD_EMPTY:
                    grid_set(self.flood, x, y, score+1)
                    self.queue.append((x, y))
            x = coord[0]+1
            y = coord[1]
            if grid_coord_valid(self.flood, x, y) and not self.get_wall(coord, EAST_MASK):
                if grid_get(self.flood, x, y) == FLOOD_EMPTY:
                    grid_set(self.flood, x, y, score+1)
                    self.queue.append((x, y))
            x = coord[0]
            y = coord[1]-1
            if grid_coord_valid(self.flood, x, y) and not self.get_wall(coord, SOUTH_MASK):
                if grid_get(self.flood, x, y) == FLOOD_EMPTY:
                    grid_set(self.flood, x, y, score+1)
                    self.queue.append((x, y))
            x = coord[0]-1
            y = coord[1]
            if grid_coord_valid(self.flood, x, y) and not self.get_wall(coord, WEST_MASK):
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
            if self.mode == MOUSE_MODE_FAST_RUN:
                self.move_fast()
            else:
                self.move_scanning()
                self.state = MOUSE_STATE_PROCESSING
        elif self.state == MOUSE_STATE_DONE:
            pass

        if self.mode == MOUSE_MODE_SEARCH_1:
            # starting in (0,0) initial search for goal
            logging.info('search 1')
            if grid_get(self.flood, self.location[0], self.location[1]) == 0:
                # reached the goal, navigate back to start
                self.mode = MOUSE_MODE_RETURN_TO_START_1
                self.set_origin_and_targets(self.location, [self.start_target])
        elif self.mode == MOUSE_MODE_RETURN_TO_START_1:
            # starting at goal now navigating back to start
            logging.info('return to start 1')
            if grid_get(self.flood, self.location[0], self.location[1]) == 0:
                # reached start, navigate to goal again
                self.mode = MOUSE_MODE_SEARCH_2
                self.set_origin_and_targets(self.start_target, self.goal_targets)
        elif self.mode == MOUSE_MODE_SEARCH_2:
            # starting in (0,0) second search for goal
            logging.info('search 2')
            if grid_get(self.flood, self.location[0], self.location[1]) == 0:
                # reached the goal, navigate back to start
                self.mode = MOUSE_MODE_RETURN_TO_START_2
                self.set_origin_and_targets(self.location, [self.start_target])
        elif self.mode == MOUSE_MODE_RETURN_TO_START_2:
            # starting at goal now navigate back to the start
            logging.info('return to start 2')
            if grid_get(self.flood, self.location[0], self.location[1]) == 0:
                # reached the start, fast navigate to the goal
                self.mode = MOUSE_MODE_FAST_RUN
                self.set_origin_and_targets(self.start_target, self.goal_targets)
                # we will need to turn around as we enter the cell facing the wrong way
                self.turn_back()
        elif self.mode == MOUSE_MODE_FAST_RUN:
            # fast navigate to the goal
            logging.info('fast run')
            if grid_get(self.flood, self.location[0], self.location[1]) == 0:
                # reached the goal, done
                self.mode = MOUSE_MODE_DONE
                self.state = MOUSE_STATE_DONE
        elif self.mode == MOUSE_MODE_DONE:
            pass

    def get_routes(self):
        """Get the generated route(s)"""
        return self.routes
    def generate_routes(self, origin, abs_dir, rel_dir, depth, limit):
        """Generate routes to the goal. If there are multiple choices limit branching depth"""
        routes = []
        route = []
        current_location = {'value':None, 'coord':origin, 'abs_dir':abs_dir, 'rel_dir':rel_dir}
        current_score = 0
        required_val = grid_get(self.flood, current_location['coord'][0], current_location['coord'][1])
        while current_location:
            route.append(current_location)
            directions = self.get_directions(current_location['coord'][0], current_location['coord'][1], current_location['abs_dir'])
            required_val = required_val - 1
            if len(directions) == 0:
                # no directions
                current_location = None
                routes.append({'score':current_score,'route':route})
            elif len(directions) == 1:
                # single direction
                if directions[0]['value'] == required_val:
                    # correct value
                    if current_location['abs_dir'] != directions[0]['abs_dir']:
                        # increase score if we make a turn, lowest score is best
                        current_score += 1
                    current_location = directions[0]
                else:
                    # wrong value
                    current_location = None
                    routes.append({'score':current_score,'route':route})
            else:
                # multiple directions
                if directions[0]['value'] == directions[1]['value']:
                    # multiple routes
                    if depth < limit and directions[0]['value'] == required_val:
                        current_location = None
                        # correct value
                        for direction in directions:
                            if directions[0]['value'] == direction['value']:
                                sub_routes = self.generate_routes(direction['coord'], direction['abs_dir'], direction['rel_dir'], depth+1, limit)
                                for sub_route in sub_routes:
                                    routes.append({'score':current_score+sub_route['score'],'route':route+sub_route['route']})
                    else:
                        # wrong value
                        current_location = None
                        routes.append({'score':current_score,'route':route})
                else:
                    # single route
                    if directions[0]['value'] == required_val:
                        # correct value
                        if current_location['abs_dir'] != directions[0]['abs_dir']:
                            # increase score if we make a turn, lowest score is best
                            current_score+=1
                        current_location = directions[0]
                    else:
                        # wrong value
                        current_location = None
                        routes.append({'score':current_score,'route':route})
        return routes

    def generate_best_routes_for_origin(self):
        """Generate routes and select the best"""
        routes = self.generate_routes(self.current_origin, NORTH_MASK, None, 0, 8)
        successful_routes = []
        # check for routes that reach the goal
        for route_info in routes:
            step_info = route_info['route'][-1]
            if grid_get(self.flood, step_info['coord'][0], step_info['coord'][1]) == 0:
                successful_routes.append(route_info)
        if len(successful_routes) == 0:
            # no completed routes, return all routes
            return [r['route'] for r in routes]
        elif len(successful_routes) == 1:
            # single complete route, return it
            return [r['route'] for r in successful_routes]
        else:
            # multiple complete routes, return best score
            successful_routes.sort(key=lambda x: x['score'], reverse=False) # sort ascending
            return [successful_routes[0]['route']]

    def scan(self) -> int:
        """Scan for walls"""
        logging.debug("check for walls")
        changes = 0
        changes += self.scan_left()
        changes += self.scan_front()
        changes += self.scan_right()
        return changes
    def scan_left(self) -> int:
        changes = 0
        if self.facing == NORTH_MASK:
            changes += self.scan_direction(self.read_left_sensor, WEST_CHECKED_MASK, WEST_MASK, EAST_CHECKED_MASK, EAST_MASK)
        if self.facing == EAST_MASK:
            changes += self.scan_direction(self.read_left_sensor, NORTH_CHECKED_MASK, NORTH_MASK, SOUTH_CHECKED_MASK, SOUTH_MASK)
        if self.facing == SOUTH_MASK:
            changes += self.scan_direction(self.read_left_sensor, EAST_CHECKED_MASK, EAST_MASK, WEST_CHECKED_MASK, WEST_MASK)
        if self.facing == WEST_MASK:
            changes += self.scan_direction(self.read_left_sensor, SOUTH_CHECKED_MASK, SOUTH_MASK, NORTH_CHECKED_MASK, NORTH_MASK)
        return changes
    def scan_front(self) -> int:
        changes = 0
        if self.facing == NORTH_MASK:
            changes += self.scan_direction(self.read_front_sensor, NORTH_CHECKED_MASK, NORTH_MASK, SOUTH_CHECKED_MASK, SOUTH_MASK)
        if self.facing == EAST_MASK:
            changes += self.scan_direction(self.read_front_sensor, EAST_CHECKED_MASK, EAST_MASK, WEST_CHECKED_MASK, WEST_MASK)
        if self.facing == SOUTH_MASK:
            changes += self.scan_direction(self.read_front_sensor, SOUTH_CHECKED_MASK, SOUTH_MASK, NORTH_CHECKED_MASK, NORTH_MASK)
        if self.facing == WEST_MASK:
            changes += self.scan_direction(self.read_front_sensor, WEST_CHECKED_MASK, WEST_MASK, EAST_CHECKED_MASK, EAST_MASK)
        return changes
    def scan_right(self) -> int:
        changes = 0
        if self.facing == NORTH_MASK:
            changes += self.scan_direction(self.read_right_sensor, EAST_CHECKED_MASK, EAST_MASK, WEST_CHECKED_MASK, WEST_MASK)
        if self.facing == EAST_MASK:
            changes += self.scan_direction(self.read_right_sensor, SOUTH_CHECKED_MASK, SOUTH_MASK, NORTH_CHECKED_MASK, NORTH_MASK)
        if self.facing == SOUTH_MASK:
            changes += self.scan_direction(self.read_right_sensor, WEST_CHECKED_MASK, WEST_MASK, EAST_CHECKED_MASK, EAST_MASK)
        if self.facing == WEST_MASK:
            changes += self.scan_direction(self.read_right_sensor, NORTH_CHECKED_MASK, NORTH_MASK, SOUTH_CHECKED_MASK, SOUTH_MASK)
        return changes

    def get_directions(self, x: int, y: int, facing: int) -> list[dict]:
        directions = []
        dir = self.get_accessible_value(x, y, NORTH_MASK, facing)
        if dir:
            directions.append(dir)
        dir = self.get_accessible_value(x, y, EAST_MASK, facing)
        if dir:
            directions.append(dir)
        dir = self.get_accessible_value(x, y, SOUTH_MASK, facing)
        if dir:
            directions.append(dir)
        dir = self.get_accessible_value(x, y, WEST_MASK, facing)
        if dir:
            directions.append(dir)
        if len(directions) == 0:
            raise Exception("No direction")
        directions.sort(key=lambda x: x['value'], reverse=False) # sort ascending
        return directions

    def move_fast(self) -> bool:
        # assuming there is one generated optimal route
        if self.route_step < len(self.routes[0]):
            self.move_relative(self.routes[0][self.route_step]['rel_dir'])
            self.route_step += 1
    def move_scanning(self):
        logging.debug("move")
        directions = self.get_directions(self.location[0], self.location[1], self.facing)
        self.move_relative(directions[0]['rel_dir'])

    # TODO: maybe simulate pixel level movement

    def move_relative(self, relative_direction) -> None:
        if relative_direction == DIRECTION_F:
            self.move_forward()
        elif relative_direction == DIRECTION_R:
            self.turn_right()
            self.move_forward()
        elif relative_direction == DIRECTION_B:
            self.turn_back()
            self.move_forward()
        elif relative_direction == DIRECTION_L:
            self.turn_left()
            self.move_forward()

    def scan_direction(self, scanner: callable, direction_checked_mask, direction_mask, _direction_checked_mask, _direction_mask) -> int:
        if self.need_to_scan(self.location, direction_checked_mask):
            self.set_scanned(self.location, direction_checked_mask)
            neighbour = self.get_neighbour(self.location, direction_mask)
            if neighbour:
                self.set_scanned(neighbour, _direction_checked_mask)
            if scanner():
                self.set_wall(self.location, direction_mask)
                if neighbour:
                    self.set_wall(neighbour, _direction_mask)
                return 1
        return 0

    def need_to_scan(self, location, direction_checked_mask) -> bool:
        return not grid_get_mask(self.map, location[0], location[1], direction_checked_mask)
    
    def set_scanned(self, location, direction_checked_mask) -> None:
        grid_set_mask(self.map, location[0], location[1], direction_checked_mask)

    def get_neighbour(self, location, direction_mask) -> tuple:
        if direction_mask == NORTH_MASK:
            neighbour = (location[0], location[1]+1)
        elif direction_mask == EAST_MASK:
            neighbour = (location[0]+1, location[1])
        elif direction_mask == SOUTH_MASK:
            neighbour = (location[0], location[1]-1)
        elif direction_mask == WEST_MASK:
            neighbour = (location[0]-1, location[1])
        if grid_coord_valid(self.map, neighbour[0], neighbour[1]):
            return neighbour
        return None

    def set_wall(self, location, direction_mask) -> None:
        grid_set_mask(self.map, location[0], location[1], direction_mask)

    def get_wall(self, location, direction_mask) -> bool:
        return grid_get_mask(self.map, location[0], location[1], direction_mask)

    def get_accessible_value(self, x: int, y: int, direction_mask: int, facing_mask: int) -> dict:
        neighbour = self.get_neighbour((x, y), direction_mask)
        if neighbour:
            if not self.get_wall((x,y),direction_mask):
                num = grid_get(self.flood, neighbour[0], neighbour[1])
                return {'value': num, 'coord':neighbour, 'abs_dir':direction_mask, 'rel_dir':self.get_rel_dir(direction_mask, facing_mask)}
        return None
    
    def get_rel_dir(self, direction_mask: int, facing_mask: int) -> int:
        if facing_mask == NORTH_MASK:
            if direction_mask == NORTH_MASK:
                return DIRECTION_F
            elif direction_mask == EAST_MASK:
                return DIRECTION_R
            elif direction_mask == SOUTH_MASK:
                return DIRECTION_B
            elif direction_mask == WEST_MASK:
                return DIRECTION_L
        if facing_mask == EAST_MASK:
            if direction_mask == NORTH_MASK:
                return DIRECTION_L
            elif direction_mask == EAST_MASK:
                return DIRECTION_F
            elif direction_mask == SOUTH_MASK:
                return DIRECTION_R
            elif direction_mask == WEST_MASK:
                return DIRECTION_B
        if facing_mask == SOUTH_MASK:
            if direction_mask == NORTH_MASK:
                return DIRECTION_B
            elif direction_mask == EAST_MASK:
                return DIRECTION_L
            elif direction_mask == SOUTH_MASK:
                return DIRECTION_F
            elif direction_mask == WEST_MASK:
                return DIRECTION_R
        if facing_mask == WEST_MASK:
            if direction_mask == NORTH_MASK:
                return DIRECTION_R
            elif direction_mask == EAST_MASK:
                return DIRECTION_B
            elif direction_mask == SOUTH_MASK:
                return DIRECTION_L
            elif direction_mask == WEST_MASK:
                return DIRECTION_F
        raise Exception(f"Unhandled mask {direction_mask} {facing_mask}")

    # TODO: use bitwise rotate on direction masks

    def read_left_sensor(self) -> bool:
        """Abstraction for reading left sensor"""
        x = self.location[0]
        y = self.location[1]
        if self.facing == NORTH_MASK:
            return grid_get_mask(self.maze, x, y, WEST_MASK)
        if self.facing == EAST_MASK:
            return grid_get_mask(self.maze, x, y, NORTH_MASK)
        if self.facing == SOUTH_MASK:
            return grid_get_mask(self.maze, x, y, EAST_MASK)
        if self.facing == WEST_MASK:
            return grid_get_mask(self.maze, x, y, SOUTH_MASK)
    def read_front_sensor(self) -> bool:
        """Abstraction for reading front sensor"""
        x = self.location[0]
        y = self.location[1]
        if self.facing == NORTH_MASK:
            return grid_get_mask(self.maze, x, y, NORTH_MASK)
        if self.facing == EAST_MASK:
            return grid_get_mask(self.maze, x, y, EAST_MASK)
        if self.facing == SOUTH_MASK:
            return grid_get_mask(self.maze, x, y, SOUTH_MASK)
        if self.facing == WEST_MASK:
            return grid_get_mask(self.maze, x, y, WEST_MASK)
    def read_right_sensor(self) -> bool:
        """Abstraction for reading right sensor"""
        x = self.location[0]
        y = self.location[1]
        if self.facing == NORTH_MASK:
            return grid_get_mask(self.maze, x, y, EAST_MASK)
        if self.facing == EAST_MASK:
            return grid_get_mask(self.maze, x, y, SOUTH_MASK)
        if self.facing == SOUTH_MASK:
            return grid_get_mask(self.maze, x, y, WEST_MASK)
        if self.facing == WEST_MASK:
            return grid_get_mask(self.maze, x, y, NORTH_MASK)

    def move_forward(self) -> None:
        """Abstraction for moving forward one cell"""
        if self.facing == NORTH_MASK:
            self.location = self.get_neighbour(self.location, NORTH_MASK)
        elif self.facing == EAST_MASK:
            self.location = self.get_neighbour(self.location, EAST_MASK)
        elif self.facing == SOUTH_MASK:
            self.location = self.get_neighbour(self.location, SOUTH_MASK)
        elif self.facing == WEST_MASK:
            self.location = self.get_neighbour(self.location, WEST_MASK)
    def turn_back(self) -> None:
        """Abstraction for turning back"""
        if self.facing == NORTH_MASK:
            self.facing = SOUTH_MASK
        elif self.facing == EAST_MASK:
            self.facing = WEST_MASK
        elif self.facing == SOUTH_MASK:
            self.facing = NORTH_MASK
        elif self.facing == WEST_MASK:
            self.facing = EAST_MASK
    def turn_left(self) -> None:
        """Abstraction for turning left"""
        if self.facing == NORTH_MASK:
            self.facing = WEST_MASK
        elif self.facing == EAST_MASK:
            self.facing = NORTH_MASK
        elif self.facing == SOUTH_MASK:
            self.facing = EAST_MASK
        elif self.facing == WEST_MASK:
            self.facing = SOUTH_MASK
    def turn_right(self) -> None:
        """Abstraction for turning right"""
        if self.facing == NORTH_MASK:
            self.facing = EAST_MASK
        elif self.facing == EAST_MASK:
            self.facing = SOUTH_MASK
        elif self.facing == SOUTH_MASK:
            self.facing = WEST_MASK
        elif self.facing == WEST_MASK:
            self.facing = NORTH_MASK