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
        If this cell has a nonzero value, that value is displayed.
        Otherwise, no value is displayed in the cell.
        The cell is outlined red if it is currently selected.
        """
        x, y = self.col * BLOCK_SIZE, self.row * BLOCK_SIZE

        if self.is_selected:
            pygame.draw.rect(self.screen, RED_OUTLINE, pygame.Rect(x,y, BLOCK_SIZE,BLOCK_SIZE), 5)
        else:
            pygame.draw.rect(self.screen, SMALL_BOX_COLOR, pygame.Rect(x,y, BLOCK_SIZE,BLOCK_SIZE), 3)


        if self.value != 0:
            text = num_font.render(str(self.value), 0, "black")
            text_rect = text.get_rect(
                center = ( x  + BLOCK_SIZE / 2, y + BLOCK_SIZE / 2)
            )
            self.screen.blit(text,text_rect)
        elif self.sketched_value != 0:
            text = num_font.render(str(self.sketched_value), 0, SKETCHED_COLOR)
            text_rect = text.get_rect(
                center=(x + 20,y + 30)
            )
            self.screen.blit(text, text_rect)