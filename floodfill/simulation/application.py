import logging
import pygame
import time
import micromouse

from constants import MAZE, MAZE_X, MAZE_Y
from grid import grid_check_mask, grid_x, grid_y, grid_get

SCALE = 2

CELL_SIZE = 18

class App():
    """Runs the simulation"""
    def __init__(self):
        self._delay = 0.03

        self.mouse = micromouse.Mouse()

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

                colour = (80,0,0)
                if grid_check_mask(MAZE, x, y, micromouse.NORTH_MASK):
                    pygame.draw.line(self._display_surf, colour, (left,top), (right,top), thickness)
                if grid_check_mask(MAZE, x, y, micromouse.EAST_MASK):
                    pygame.draw.line(self._display_surf, colour, (right,top), (right,bot), thickness)
                if grid_check_mask(MAZE, x, y, micromouse.SOUTH_MASK):
                    pygame.draw.line(self._display_surf, colour, (right,bot), (left,bot), thickness)
                if grid_check_mask(MAZE, x, y, micromouse.WEST_MASK):
                    pygame.draw.line(self._display_surf, colour, (left,bot), (left,top), thickness)
                
                # render detected walls
                moffset = 1
                mleft = left+moffset
                mright = right-moffset
                mtop = top+moffset
                mbot = bot-moffset
                if grid_check_mask(self.mouse.map, x, y, micromouse.NORTH_MASK):
                    colour = (255,0,0)
                    pygame.draw.line(self._display_surf, colour, (mleft,mtop), (mright,mtop), thickness)
                if grid_check_mask(self.mouse.map, x, y, micromouse.EAST_MASK):
                    colour = (255,0,0)
                    pygame.draw.line(self._display_surf, colour, (mright,mtop), (mright,mbot), thickness)
                if grid_check_mask(self.mouse.map, x, y, micromouse.SOUTH_MASK):
                    colour = (255,0,0)
                    pygame.draw.line(self._display_surf, colour, (mright,mbot), (mleft,mbot), thickness)
                if grid_check_mask(self.mouse.map, x, y, micromouse.WEST_MASK):
                    colour = (255,0,0)
                    pygame.draw.line(self._display_surf, colour, (mleft,mbot), (mleft,mtop), thickness)

        # render mouse
        cl = self.mouse.location[0] * CELL_SIZE * SCALE
        ct = self._height - (self.mouse.location[1] * CELL_SIZE * SCALE) - (CELL_SIZE*SCALE)
        cr = cl + (CELL_SIZE*SCALE)
        cb = ct + (CELL_SIZE*SCALE)
        if self.mouse.facing == micromouse.NORTH_MASK:
            l = (cl) + (CELL_SIZE*SCALE/2) - (self.mouse.width*SCALE/2)
            t = (ct) + (CELL_SIZE*SCALE/2) - (self.mouse.height*SCALE/2)
            w = self.mouse.width*SCALE
            h = self.mouse.height*SCALE
            d = 5 * SCALE
            if self.mouse.state == micromouse.MOUSE_STATE_PROCESSING:
                pygame.draw.line(self._display_surf, (255,255,255), (cl,ct), (cl+d,ct+d), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cl+(CELL_SIZE*SCALE/2),ct), (cl+(CELL_SIZE*SCALE/2),ct+d), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cr,ct), (cr-d,ct+d), 1)
        if self.mouse.facing == micromouse.EAST_MASK:
            l = (cl) + (CELL_SIZE*SCALE/2) - (self.mouse.height*SCALE/2)
            t = (ct) + (CELL_SIZE*SCALE/2) - (self.mouse.width*SCALE/2)
            w = self.mouse.height*SCALE
            h = self.mouse.width*SCALE
            d = 5 * SCALE
            if self.mouse.state == micromouse.MOUSE_STATE_PROCESSING:
                pygame.draw.line(self._display_surf, (255,255,255), (cr,ct), (cr-d,ct+d), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cr,ct+(CELL_SIZE*SCALE/2)), (cr-d,ct+(CELL_SIZE*SCALE/2)), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cr,cb), (cr-d,cb-d), 1)
        if self.mouse.facing == micromouse.SOUTH_MASK:
            l = (cl) + (CELL_SIZE*SCALE/2) - (self.mouse.width*SCALE/2)
            t = (ct) + (CELL_SIZE*SCALE/2) - (self.mouse.height*SCALE/2)
            w = self.mouse.width*SCALE
            h = self.mouse.height*SCALE
            d = 5 * SCALE
            if self.mouse.state == micromouse.MOUSE_STATE_PROCESSING:
                pygame.draw.line(self._display_surf, (255,255,255), (cl,cb), (cl+d,cb-d), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cl+(CELL_SIZE*SCALE/2),cb), (cl+(CELL_SIZE*SCALE/2),cb-d), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cr,cb), (cr-d,cb-d), 1)
        if self.mouse.facing == micromouse.WEST_MASK:
            l = (cl) + (CELL_SIZE*SCALE/2) - (self.mouse.height*SCALE/2)
            t = (ct) + (CELL_SIZE*SCALE/2) - (self.mouse.width*SCALE/2)
            w = self.mouse.height*SCALE
            h = self.mouse.width*SCALE
            d = 5 * SCALE
            if self.mouse.state == micromouse.MOUSE_STATE_PROCESSING:
                pygame.draw.line(self._display_surf, (255,255,255), (cl,ct), (cl+d,ct+d), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cl,ct+(CELL_SIZE*SCALE/2)), (cl+d,ct+(CELL_SIZE*SCALE/2)), 1)
                pygame.draw.line(self._display_surf, (255,255,255), (cl,cb), (cl+d,cb-d), 1)
        if self.mouse.state == micromouse.MOUSE_STATE_PROCESSING:
            colour = (255,0,0)
        if self.mouse.state == micromouse.MOUSE_STATE_MOVING:
            colour = (0,255,0)
        pygame.draw.rect(self._display_surf, colour, pygame.Rect((l,t), (w,h)), 0)
        
        # render flood values
        for x in range(grid_x(self.mouse.flood)):
            for y in range(grid_y(self.mouse.flood)):
                num = grid_get(self.mouse.flood, x, y)
                img = self.font.render(str(num), True, (80,80,80))
                self._display_surf.blit(img, (x*CELL_SIZE*SCALE, self._height-(y*CELL_SIZE*SCALE)-(CELL_SIZE*SCALE)))

        routes = self.mouse.get_routes()
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