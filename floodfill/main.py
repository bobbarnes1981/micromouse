import argparse
import logging
import pygame
import time

NORTH_MASK = 0x01
EAST_MASK = 0x02
SOUTH_MASK = 0x04
WEST_MASK = 0x08

SCALE = 2
CELL_SIZE = 18
MAZE_X = 16
MAZE_Y = 16

MOUSE_STATE_CHECK = 1
MOUSE_STATE_UPDATE = 2
MOUSE_STATE_MOVE = 3

class Maze():
    """Represents the physical maze"""
    def __init__(self):
        self.cells = [
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
    def rows(self) -> int:
        return len(self.cells)
    def cols(self) -> int:
        return len(self.cells[0])
    def validate(self) -> bool:
        for r in range(self.rows()):
            for c in range(self.cols()):
                for y in range(-1, +2):
                    for x in range(-1, +2):
                        # TODO: validate cell walls in neighbouring cells
                        pass
        return True

class WallDetector():
    def __init__(self, maze):
        self.maze = maze
    def north(self, x, y):
        return (self.maze.cells[y][x] & NORTH_MASK) == NORTH_MASK
    def east(self, x, y):
        return (self.maze.cells[y][x] & EAST_MASK) == EAST_MASK
    def south(self, x, y):
        return (self.maze.cells[y][x] & SOUTH_MASK) == SOUTH_MASK
    def west(self, x, y):
        return (self.maze.cells[y][x] & WEST_MASK) == WEST_MASK

class Mouse():
    """Represents the micromouse"""
    def __init__(self, location, target, wall_detector):
        self.location = location
        self.target = target
        self.wall_detector = wall_detector
        self.facing = NORTH_MASK
        self.state = MOUSE_STATE_CHECK
        self.width = 8
        self.height = 10
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
        # TODO: maybe generate this using algorithm?
        self.flood = [
            [14,13,12,11,10, 9, 8, 7, 7, 8, 9,10,11,12,13,14],
            [13,12,11,10, 9, 8, 7, 6, 6, 7, 8, 9,10,11,12,13],
            [12,11,10, 9, 8, 7, 6, 5, 5, 6, 7, 8, 9,10,11,12],
            [11,10, 9, 8, 7, 6, 5, 4, 4, 5, 6, 7, 8, 9,10,11],
            [10, 9, 8, 7, 6, 5, 4, 3, 3, 4, 5, 6, 7, 8, 9,10],
            [ 9, 8, 7, 6, 5, 4, 3, 2, 2, 3, 4, 5, 6, 7, 8, 9],
            [ 8, 7, 6, 5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 6, 7, 8],
            [ 7, 6, 5, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 5, 6, 7],
            [ 7, 6, 5, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 5, 6, 7],
            [ 8, 7, 6, 5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 6, 7, 8],
            [ 9, 8, 7, 6, 5, 4, 3, 2, 2, 3, 4, 5, 6, 7, 8, 9],
            [10, 9, 8, 7, 6, 5, 4, 3, 3, 4, 5, 6, 7, 8, 9,10],
            [11,10, 9, 8, 7, 6, 5, 4, 4, 5, 6, 7, 8, 9,10,11],
            [12,11,10, 9, 8, 7, 6, 5, 5, 6, 7, 8, 9,10,11,12],
            [13,12,11,10, 9, 8, 7, 6, 6, 7, 8, 9,10,11,12,13],
            [14,13,12,11,10, 9, 8, 7, 7, 8, 9,10,11,12,13,14],
        ]
    def draw(self, surface):
        cl = self.location[0] * CELL_SIZE * SCALE
        ct = self.location[1] * CELL_SIZE * SCALE
        cr = cl + (CELL_SIZE*SCALE)
        cb = ct + (CELL_SIZE*SCALE)
        if self.facing == NORTH_MASK:
            l = (cl) + ((self.width*SCALE) / 2)
            t = (ct) + ((self.height*SCALE) / 2)
            w = self.width*SCALE
            h = self.height*SCALE
            d = 5 * SCALE
            if self.state == MOUSE_STATE_CHECK:
                pygame.draw.line(surface, (255,255,255), (cl,ct), (cl+d,ct+d), 1)
                pygame.draw.line(surface, (255,255,255), (cl+(CELL_SIZE*SCALE/2),ct), (cl+(CELL_SIZE*SCALE/2),ct+d), 1)
                pygame.draw.line(surface, (255,255,255), (cr,ct), (cr-d,ct+d), 1)
        if self.facing == EAST_MASK:
            l = (self.location[0] * CELL_SIZE * SCALE) + ((CELL_SIZE*SCALE - self.height*SCALE) / 2)
            t = (self.location[1] * CELL_SIZE * SCALE) + ((CELL_SIZE*SCALE - self.width*SCALE) / 2)
            w = self.height*SCALE
            h = self.width*SCALE
            d = 5 * SCALE
            if self.state == MOUSE_STATE_CHECK:
                pass
        if self.facing == SOUTH_MASK:
            l = (self.location[0] * CELL_SIZE * SCALE) + ((CELL_SIZE*SCALE - self.width*SCALE) / 2)
            t = (self.location[1] * CELL_SIZE * SCALE) + ((CELL_SIZE*SCALE - self.height*SCALE) / 2)
            w = self.width*SCALE
            h = self.height*SCALE
            d = 5 * SCALE
            if self.state == MOUSE_STATE_CHECK:
                pass
        if self.facing == WEST_MASK:
            l = (self.location[0] * CELL_SIZE * SCALE) + ((CELL_SIZE*SCALE - self.height*SCALE) / 2)
            t = (self.location[1] * CELL_SIZE * SCALE) + ((CELL_SIZE*SCALE - self.width*SCALE) / 2)
            w = self.height*SCALE
            h = self.width*SCALE
            d = 5 * SCALE
            if self.state == MOUSE_STATE_CHECK:
                pass
        if self.state == MOUSE_STATE_CHECK:
            colour = (255,0,0)
        if self.state == MOUSE_STATE_UPDATE:
            colour = (255,255,0)
        if self.state == MOUSE_STATE_MOVE:
            colour = (0,255,0)
        pygame.draw.rect(surface, colour, pygame.Rect((l,t), (w,h)), 0)
    def tick(self):
        logging.debug('mouse tick')
        if self.state == MOUSE_STATE_CHECK:
            self.check()
            self.state = MOUSE_STATE_UPDATE
        elif self.state == MOUSE_STATE_UPDATE:
            self.update()
            self.state = MOUSE_STATE_MOVE
        elif self.state == MOUSE_STATE_MOVE:
            self.move()
            self.state = MOUSE_STATE_CHECK
    def check(self):
        logging.debug("check for walls")
        if self.facing == NORTH_MASK:
            self.scan_west()
            self.scan_north()
            self.scan_east()
        if self.facing == EAST_MASK:
            self.scan_north()
            self.scan_east()
            self.scan_south()
        if self.facing == SOUTH_MASK:
            self.scan_east()
            self.scan_south()
            self.scan_west()
        if self.facing == WEST_MASK:
            self.scan_south()
            self.scan_west()
            self.scan_north()
    def update(self):
        logging.debug("update map")
        # do floodfill thing
        pass
    def move(self):
        logging.debug("move")
        directions = []
        if self.facing == NORTH_MASK:
            dir = self.check_west()
            if dir:
                directions.append(dir)
            dir = self.check_north()
            if dir:
                directions.append(dir)
            dir = self.check_east()
            if dir:
                directions.append(dir)
        if self.facing == EAST_MASK:
            dir = self.check_north()
            if dir:
                directions.append(dir)
            dir = self.check_east()
            if dir:
                directions.append(dir)
            dir = self.check_south()
            if dir:
                directions.append(dir)
        if self.facing == SOUTH_MASK:
            dir = self.check_east()
            if dir:
                directions.append(dir)
            dir = self.check_south()
            if dir:
                directions.append(dir)
            dir = self.check_west()
            if dir:
                directions.append(dir)
        if self.facing == WEST_MASK:
            dir = self.check_south()
            if dir:
                directions.append(dir)
            dir = self.check_west()
            if dir:
                directions.append(dir)
            dir = self.check_north()
            if dir:
                directions.append(dir)
        if len(directions) == 0:
            raise Exception("No direction")
        # TODO: if smallest number behind wall then re-flood
        directions.sort(key=lambda x: x['value'], reverse=False) # sort ascending
        direction = directions[0]
        if direction['acc'] == False:
            raise Exception("Smallest number not accessible")
        if direction['dir'] != self.facing:
            self.facing = direction['dir']
        self.location = direction['coord']
    def scan_north(self):
        if not self.detected_north():
            print('scanning north')
            self.cells[self.location[1]][self.location[0]] |= NORTH_MASK<<4
            if self.wall_detector.north(self.location[0], self.location[1]):
                self.cells[self.location[1]][self.location[0]] |= NORTH_MASK
    def scan_east(self):
        if not self.detected_east():
            print('scanning east')
            self.cells[self.location[1]][self.location[0]] |= EAST_MASK<<4
            if self.wall_detector.east(self.location[0], self.location[1]):
                self.cells[self.location[1]][self.location[0]] |= EAST_MASK
    def scan_south(self):
        if not self.detected_south():
            print('scanning south')
            self.cells[self.location[1]][self.location[0]] |= SOUTH_MASK<<4
            if self.wall_detector.south(self.location[0], self.location[1]):
                self.cells[self.location[1]][self.location[0]] |= SOUTH_MASK
    def scan_west(self):
        if not self.detected_west():
            print('scanning west')
            self.cells[self.location[1]][self.location[0]] |= WEST_MASK<<4
            if self.wall_detector.west(self.location[0], self.location[1]):
                self.cells[self.location[1]][self.location[0]] |= WEST_MASK
    def check_north(self):
        # check north
        x = self.location[0]
        y = self.location[1]-1
        #print(x,y)
        if x>=0 and x<MAZE_X and y>=0 and y<MAZE_Y:
            print("checking north")
            num = self.flood[y][x]
            print(f"north is {num}")
            return {'value': num, 'coord':(x,y), 'dir':NORTH_MASK, 'acc':not self.wall_north()}
        return None
    def check_east(self):
        # check east
        x = self.location[0]+1
        y = self.location[1]
        #print(x,y)
        if x>=0 and x<MAZE_X and y>=0 and y<MAZE_Y:
            print("checking east")
            num = self.flood[y][x]
            print(f"east is {num}")
            return {'value': num, 'coord':(x,y), 'dir':EAST_MASK, 'acc':not self.wall_east()}
        return None
    def check_south(self):
        # check south
        x = self.location[0]
        y = self.location[1]+1
        #print(x,y)
        if x>=0 and x<MAZE_X and y>=0 and y<MAZE_Y:
            print("checking south")
            num = self.flood[y][x]
            print(f"south is {num}")
            return {'value': num, 'coord':(x,y), 'dir':SOUTH_MASK, 'acc':not self.wall_south()}
        return None
    def check_west(self):
        # check west
        x = self.location[0]-1
        y = self.location[1]
        #print(x,y)
        if x>=0 and x<MAZE_X and y>=0 and y<MAZE_Y:
            print("checking west")
            num = self.flood[y][x]
            print(f"west is {num}")
            return {'value': num, 'coord':(x,y), 'dir':WEST_MASK, 'acc':not self.wall_west()}
        return None
    def detected_north(self):
        return (self.cells[self.location[1]][self.location[0]] & NORTH_MASK<<4) == NORTH_MASK<<4
    def detected_east(self):
        return (self.cells[self.location[1]][self.location[0]] & EAST_MASK<<4) == EAST_MASK<<4
    def detected_south(self):
        return (self.cells[self.location[1]][self.location[0]] & SOUTH_MASK<<4) == SOUTH_MASK<<4
    def detected_west(self):
        return (self.cells[self.location[1]][self.location[0]] & WEST_MASK<<4) == WEST_MASK<<4
    def wall_north(self):
        return (self.cells[self.location[1]][self.location[0]] & NORTH_MASK) == NORTH_MASK
    def wall_east(self):
        return (self.cells[self.location[1]][self.location[0]] & EAST_MASK) == EAST_MASK
    def wall_south(self):
        return (self.cells[self.location[1]][self.location[0]] & SOUTH_MASK) == SOUTH_MASK
    def wall_west(self):
        return (self.cells[self.location[1]][self.location[0]] & WEST_MASK) == WEST_MASK

class App():
    """Runs the simulation, curently attempt to simulate mouse maze mapping and floodfill, we are ignoring mouse navigation"""
    def __init__(self):
        self._delay = 0.3

        self.maze = Maze()
        self.maze.validate()

        self.start = (0,15)
        self.target = (8,8) # (7,7), (7,8), (8,7), (8,8)
        self.mouse = Mouse(self.start, self.target, WallDetector(self.maze))

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
            self.mouse.tick()
            if self._complete is False:
                pass
    def on_render(self) -> None:
        """On render."""
        self._display_surf.fill((0,0,0))
        for r in range(self.maze.rows()):
            for c in range(self.maze.cols()):
                left = c*CELL_SIZE*SCALE
                right = (((c*CELL_SIZE)+CELL_SIZE)*SCALE)-1
                top = r*CELL_SIZE*SCALE
                bot = (((r*CELL_SIZE)+CELL_SIZE)*SCALE)-1
                thickness = 1

                if (self.maze.cells[r][c] & NORTH_MASK) == NORTH_MASK:
                    colour = (255,0,0)
                    pygame.draw.line(self._display_surf, colour, (left,top), (right,top), thickness)
                if (self.maze.cells[r][c] & EAST_MASK) == EAST_MASK:
                    colour = (255,0,0)
                    pygame.draw.line(self._display_surf, colour, (right,top), (right,bot), thickness)
                if (self.maze.cells[r][c] & SOUTH_MASK) == SOUTH_MASK:
                    colour = (255,0,0)
                    pygame.draw.line(self._display_surf, colour, (right,bot), (left,bot), thickness)
                if (self.maze.cells[r][c] & WEST_MASK) == WEST_MASK:
                    colour = (255,0,0)
                    pygame.draw.line(self._display_surf, colour, (left,bot), (left,top), thickness)
                
                moffset = 2
                mleft = left+moffset
                mright = right-moffset
                mtop = top+moffset
                mbot = bot-moffset
                if (self.mouse.cells[r][c] & NORTH_MASK) == NORTH_MASK:
                    colour = (0,255,0)
                    pygame.draw.line(self._display_surf, colour, (mleft,mtop), (mright,mtop), thickness)
                if (self.mouse.cells[r][c] & EAST_MASK) == EAST_MASK:
                    colour = (0,255,0)
                    pygame.draw.line(self._display_surf, colour, (mright,mtop), (mright,mbot), thickness)
                if (self.mouse.cells[r][c] & SOUTH_MASK) == SOUTH_MASK:
                    colour = (0,255,0)
                    pygame.draw.line(self._display_surf, colour, (mright,mbot), (mleft,mbot), thickness)
                if (self.mouse.cells[r][c] & WEST_MASK) == WEST_MASK:
                    colour = (0,255,0)
                    pygame.draw.line(self._display_surf, colour, (mleft,mbot), (mleft,mtop), thickness)

        self.mouse.draw(self._display_surf)
        pygame.draw.circle(self._display_surf, (255,255,255), (((self.target[0]*CELL_SIZE)*SCALE)+(CELL_SIZE*SCALE)/2, ((self.target[1]*CELL_SIZE)*SCALE)+(CELL_SIZE*SCALE)/2), 5*SCALE, 1)
        
        for r in range(len(self.mouse.flood)):
            for c in range(len(self.mouse.flood[r])):
                num = self.mouse.flood[r][c]
                img = self.font.render(str(num), True, (80,80,80))
                self._display_surf.blit(img, (c*CELL_SIZE*SCALE, r*CELL_SIZE*SCALE))

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