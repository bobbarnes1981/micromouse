import argparse
import logging
import pygame
import time

NORTH_MASK = 0x01
EAST_MASK = 0x02
SOUTH_MASK = 0x04
WEST_MASK = 0x08
CELL_SIZE = 18
MAZE_X = 16
MAZE_Y = 16

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

class Mouse():
    """Represetns the micromouse"""
    def __init__(self, location, target):
        self.location = location
        self.target = target
        self.facing = NORTH_MASK
        self.width = 8
        self.height = 10
    def draw(self, surface):
        if self.facing == NORTH_MASK:
            l = (self.location[0] * CELL_SIZE) + ((CELL_SIZE - self.width) / 2)
            t = (self.location[1] * CELL_SIZE) + ((CELL_SIZE - self.height) / 2)
            w = self.width
            h = self.height
        if self.facing == EAST_MASK:
            pass
        if self.facing == SOUTH_MASK:
            pass
        if self.facing == WEST_MASK:
            pass
        pygame.draw.rect(surface, (255,255,255), pygame.Rect((l,t), (w,h)), 0)

class App():
    """Runs the simulation, curently attempt to simulate mouse maze mapping and floodfill, we are ignoring mouse navigation"""
    def __init__(self):
        self._delay = 1

        self.start = (0,15)
        self.target = (8,8) # (7,7), (7,8), (8,7), (8,8)
        self.mouse = Mouse(self.start, self.target)

        self._running = True
        self._display_surf = None
        self._width = CELL_SIZE * MAZE_X
        self._height = CELL_SIZE * MAZE_Y
        self._size = (self._width, self._height)
        self._time = time.time()
        self._counter = 0
        self._complete = False
        self.font = None

        self.maze = Maze()
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
                pass
    def on_render(self) -> None:
        """On render."""
        self._display_surf.fill((0,0,0))
        for r in range(0, len(self.maze.cells)):
            for c in range(0, len(self.maze.cells[r])):
                left = c*CELL_SIZE
                right = ((c*CELL_SIZE)+CELL_SIZE)-1
                top = r*CELL_SIZE
                bot = ((r*CELL_SIZE)+CELL_SIZE)-1
                thickness = 1

                if (self.maze.cells[r][c] & NORTH_MASK) == NORTH_MASK:
                    colour = (255,0,0)
                    pygame.draw.line(self._display_surf, colour, (left,top), (right,top), thickness)
                if (self.maze.cells[r][c] & EAST_MASK) == EAST_MASK:
                    colour = (255,255,0)
                    pygame.draw.line(self._display_surf, colour, (right,top), (right,bot), thickness)
                if (self.maze.cells[r][c] & SOUTH_MASK) == SOUTH_MASK:
                    colour = (0,255,0)
                    pygame.draw.line(self._display_surf, colour, (right,bot), (left,bot), thickness)
                if (self.maze.cells[r][c] & WEST_MASK) == WEST_MASK:
                    colour = (0,0,255)
                    pygame.draw.line(self._display_surf, colour, (left,bot), (left,top), thickness)
        self.mouse.draw(self._display_surf)
        pygame.draw.circle(self._display_surf, (255,255,255), ((self.target[0]*CELL_SIZE)+CELL_SIZE/2, (self.target[1]*CELL_SIZE)+CELL_SIZE/2), 5, 1)

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