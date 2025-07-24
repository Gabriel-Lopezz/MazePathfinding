import pygame, sys
from constants import *
class Block:
    def __init__(self, state, row, col, screen):
        """Constructor for the block class"""
        """
        States:
        0 - open(.)
        1 - wall(#)
        2 - intersection (I)
        3 - start (s)
        4 - goal (g)
        5 - explored (set when it has been visited idk)
        column = x-coordinate
        row = y-coordinate
        """
        self.state = state
        self.row = row
        self.col = col
        self.screen = screen

    def set_state(self, state):
        """Setter for this block’s state"""
        self.state = state
    def draw(self):
        """
        Draws this block, based on its state.
        """
        x, y = self.col * BLOCK_SIZE, self.row * BLOCK_SIZE
        match self.state:
            case 0:
                block_color = PATH_COLOR
            case 1:
                block_color = WALL_COLOR
            case 2:
                block_color = INTERSECTION_COLOR
            case 3:
                block_color = START_COLOR
            case 4:
                block_color = GOAL_COLOR
            case 5:
                block_color = EXPLORED_COLOR
            case _: # non-existent case
                block_color = RED

        pygame.draw.rect(self.screen, block_color, pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))


# ========To Test ========#
# pygame.init()
# screen = pygame.display.set_mode((BLOCK_SIZE,BLOCK_SIZE))
# screen.fill(RED)
# block = Block(4,0,0, screen)
# block.draw()
#
# while True:
#     pygame.display.update()