import pygame as pg
from random import choice
import copy

# Define constants
SCREEN_WIDTH = SCREEN_HEIGHT = 720
BLOCK_SIZE = 30
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 85, 85)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 170, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)

# Block shapes
SHAPES = {
    "I": [(0, i) for i in range(-1, 3)],
    "J": [(-1, -1), (-1, 0), (0, 0), (1, 0)],
    "L": [(1, -1), (-1, 0), (0, 0), (1, 0)],
    "O": [(i, j) for i in [-1, 0] for j in [-1, 0]],
    "S": [(j, i) for i in [-1, 0] for j in [0, 1]],
    "T": [(k, l) for k in [-1, 0, 1] for l in [-1, 0]],
    "Z": [(j, i) for i in [0, 1] for j in [-1, 0]],
}

# Initialize screen
pg.display.set_caption("PyGame-based Tetris Clone")
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pg.time.Clock()
font = pg.sysfont.Font('freesansbold.ttf', BLOCK_SIZE // 2)

# Game settings
GRID_COLS = int(SCREEN_WIDTH / BLOCK_SIZE)
GRID_ROWS = int(SCREEN_HEIGHT / BLOCK_SIZE)
DROP_DELAY = 90   # Frames between auto-dropped blocks
PREVIEW_COLUMNS = 4     # Columns dedicated to showing upcoming moves


def draw_block(color, xy):
    """Draw a single square block."""
    rect = pg.Rect(*xy, BLOCK_SIZE, BLOCK_SIZE)
    pg.draw.rect(screen, color, rect)


class Grid:
    def __init__(self):
        self.grid = [[None] * (GRID_COLS + PREVIEW_COLUMNS) for _ in range(GRID_ROWS)]
        
    def clear_rows(self):
        """Remove completed rows from the top of the grid."""
        new_grid = [[None] * (GRID_COLS + PREVIEW_COLUMNS) for _ in range(GRID_ROWS)]
        rowidx = GRID_ROWS - 1
        for oldrow in reversed(self.grid):
            if None in oldrow:
                new_grid[rowidx] = oldrow
                rowidx -= 1
        self.grid = new_grid

    def get_preview_columns(self):
        """Return only the main playing area excluding the preview columns."""
        return self.grid[:, :-PREVIEW_COLUMNS]

    def set_preview_column(self, column, values):
        """Set the contents of one or multiple preview columns."""
        assert len(values) <= PREVIEW_COLUMNS
        self.grid[:, -(PREVIEW_COLUMNS - len(values)):] = values

    def render(self):
        """Render the entire grid onto the screen."""
        for y, row in enumerate(self.get_preview_columns()):
            for x, value in enumerate(row):
                if value is not None:
                    draw_block(value['color'], (x*BLOCK_SIZE, y*BLOCK_SIZE))

    def is_occupied(self, coords):
        """Check whether any given coordinate pair is occupied by another block."""
        for x, y in coords:
            if y >= 0 and self.grid[y][x]:
                return True
        return False

    def highlight_landing_position(self, shape):
        """Highlight the potential landing position of a falling shape."""
        temp_grid = copy.deepcopy(self.grid)
        for coord in shape.coords:
            temp_grid[coord[1]][coord[0]] = {'color': 'highlighted'}
            
        self.set_preview_column(temp_grid[-PREVIEW_COLUMNS:])

    def reset_preview_column(self):
        """Clear out the preview column used for highlighting potential landing positions."""
        self.set_preview_column([[None]*len(self.grid) for _ in range(PREVIEW_COLUMNS)])


class Shape:
    def __init__(self, name=''):
        self.name = name
        self.coords = SHAPES[name].copy()
        self.center = (int(sum(c[0] for c in self.coords)/len(self.coords)),
                       min(c[1] for c in self.coords))
        self.rotation = 0
        self.color = COLORS[choice(list(COLORS))]

    def translate(self, dx=0, dy=0):
        """Move this shape horizontally/vertically by the specified amount."""
        self.coords = [(x+dx, y+dy) for x, y in self.coords]
        self.center = (self.center[0]+dx, self.center[1]+dy)

    def rotate(self, clockwise=True):
        """Rotate this shape around its center point."""
        rotation = 1 if clockwise else -1
        pivot = self.center
        self.coords = [(pivot[0]-(x-pivot[0]), pivot[1]-(y-pivot[1])) for x, y in self.coords]
        self.rotation += rotation

    def next_move(self, dx, dy):
        """Calculate the resulting coordinates of a hypothetical movement."""
        result = []
        for coord in self.coords:
            nx, ny = coord[0] + dx, coord[1] + dy
            if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS:
                result.append((nx, ny))
        return result


def spawn():
    """Create a randomly selected shape at the top of the grid."""
    return Shape(choice(list(SHAPES)))


def run_game():
    global DROP_DELAY
    running = True
    paused = False
    framecount = 0
    score = 0
    dropdelay = DROP_DELAY
    active_shape = spawn()
    grid = Grid()

    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    if not grid.is_occupied(active_shape.next_move(-1, 0)):
                        active_shape.translate(-1, 0)
                elif event.key == K_RIGHT:
                    if not grid.is_occupied(active_shape.next_move(1, 0)):
                        active_shape.translate(1, 0)
                elif event.key == K_SPACE:
                    while not grid.is_occupied(active_shape.next_move(0, -1)):
                        active_shape.translate(0, -1)
                elif event.key == K_r:
                    active_shape.rotate()
                elif event.key == K_a
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                    if player.x - PLAYER_SPEED > 0:
                        player.x -= PLAYER_SPEED