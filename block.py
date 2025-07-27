import pygame
from constants import *
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

    def set_state(self, state: BlockState|int):
        self.state = state

    """
        Draws the block based on its state
    """
    def draw(self):
        x, y = self.col * self.size, self.row * self.size
        match BlockState(self.state):
            case BlockState.OPEN:
                block_color = PATH_COLOR

            case BlockState.WALL:
                block_color = WALL_COLOR

            case BlockState.INTERSECTION:
                block_color = INTERSECTION_COLOR

            case BlockState.START:
                block_color = START_COLOR

            case BlockState.END:
                block_color = END_COLOR

            case BlockState.EXPLORED:
                block_color = EXPLORED_COLOR

            case _: # non-existent case
                raise Exception(f"Could not resolve Block State {self.state}. Block: row {self.row}, col {self.col}")

        pygame.draw.rect(surface=self.screen, color=block_color, rect=pygame.Rect(x, y, self.size, self.size))


# ========To Test ========#
# pygame.init()
# screen = pygame.display.set_mode((self.size,self.size))
# screen.fill(RED)
# block = Block(4,0,0, screen)
# block.draw()
#
# while True:
#     pygame.display.update()