import pygame
from config import *
from enum import Enum

class BlockState(Enum):
    OPEN = 0            # Denotes traversable block
    WALL = 1            # Denotes non-traversable block
    INTERSECTION = 2    # Denotes traversable block with divergent paths
    START = 3           # Denotes the starting (source) block
    END = 4            # Denotes the end (target) block
    EXPLORED = 5        # Denotes whether the block has been explored

class Block:
    def __init__(self, size: int, state: BlockState|int, row: int, col: int, screen: pygame.Surface):
        self.state = state
        self.size = size
        self.row = row
        self.col = col
        self.screen = screen

        self.x = MAZE_PADDING_LEFT + self.col * self.size
        self.y = MAZE_PADDING_TOP + self.row * self.size
        self.set_color(state=state)
        
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)


    def set_color(self, state: BlockState|int):
        match BlockState(self.state):
            case BlockState.OPEN:
                self.color = PATH_COLOR

            case BlockState.WALL:
                self.color = WALL_COLOR

            case BlockState.INTERSECTION:
                self.color = INTERSECTION_COLOR

            case BlockState.START:
                self.color = START_COLOR

            case BlockState.END:
                self.color = END_COLOR

            case BlockState.EXPLORED:
                self.color = EXPLORED_COLOR

            case _: # non-existent case
                raise Exception(f"Could not resolve Block State {self.state}. Block: row {self.row}, col {self.col}")

    """
        Draws the block based on its state
    """
    def draw(self):
        self.set_color(self.state)
        pygame.draw.rect(surface=self.screen, color=self.color, rect=self.rect)


# ========To Test ========#
# pygame.init()
# screen = pygame.display.set_mode((self.size,self.size))
# screen.fill(RED)
# block = Block(4,0,0, screen)
# block.draw()
#
# while True:
#     pygame.display.update()