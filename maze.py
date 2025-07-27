import csv
import pygame
import _io
from constants import *
from block import Block, BlockState

class Maze:
    def __init__(self, maze_file: _io.TextIOWrapper, screen: pygame.Surface):
        """
        :param input_maze: a string representation of the maze 
        :param width:
        :param height:
        :param screen:
        screen is a window from PyGame.
        creates a maze from a string input space, which should be separated by \n
        """
        self.screen = screen
        self.maze = self.maze_from_file(maze_file)

    def draw(self):
        for row in self.maze:
            for block in row:
                block.draw()

    def maze_from_file(self, file: _io.TextIOWrapper) -> list[list[Block]]:
        maze = []

        reader = csv.reader(file)

        for row_ind, row in enumerate(reader):
            maze_row = []

            for col_ind, block_str in enumerate(row):
                block_length = MAZE_SIZE / len(row)
                block_char = block_str.strip()
                block_state = None

                match(block_char.lower()):
                    case ".":
                        block_state = BlockState.OPEN

                    case "#":
                        block_state = BlockState.WALL

                    case "s":
                        block_state = BlockState.START

                    case "e":
                        block_state = BlockState.END

                    case _: # non-existent case
                        raise Exception(f"Could not resolve Block character {block_char} in row {row_ind}, col {col_ind}")
                
                cur_block = Block(size=block_length, state=block_state, row=row_ind, col=col_ind, screen=self.screen)
                maze_row.append(cur_block)
            
            maze.append(maze_row)
        
        file.close() # Close the file

        return maze