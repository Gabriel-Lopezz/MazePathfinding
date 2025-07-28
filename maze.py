import csv
import pygame
import _io
from constants import *
from block import Block, BlockState
import time

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
            

    def create_maze(maze_file: _io.TextIOWrapper, screen: pygame.Surface):
        try:
            new_maze = Maze(maze_file=maze_file, screen=screen)
        except Exception as maze_exception:
            return False, str(maze_exception)

        return True, new_maze

    def draw(self):
        '''
        Loads all the maze blocks into the screen buffer. Renders the changes after loading all blocks
        '''
        for row in self.maze:
            for block in row:
                block.draw()
        
        pygame.display.flip()
    
    def clear(self):
        '''
        Clears maze data, draws a white square to cover Maze window, and updates display
        '''
        self.maze = None
        pygame.draw.rect(surface=self.screen, color=WHITE, rect=(0, 0, MAZE_SIZE, MAZE_SIZE))
        pygame.display.flip()

    def maze_from_file(self, file: _io.TextIOWrapper) -> list[list[Block]]:
        maze = []

        lines = list(file)
        rows = len(lines)
        
        reader = csv.reader(lines)
        cols = len(next(reader))

        if rows < 2 or cols < 2 or rows != cols:
            raise Exception("Maze must be square, at least 2x2. This maze has rows:{rows} cols:{cols}")
        
        block_length = MAZE_SIZE / rows
        
        starts = 0
        ends = 0
        
        for row_ind, row in enumerate(csv.reader(lines)):
            maze_row = []

            for col_ind, block_str in enumerate(row):
                block_char = block_str.strip().lower()

                match (block_char):
                    case ".":
                        block_state = BlockState.OPEN

                    case "#":
                        block_state = BlockState.WALL

                    case "s":
                        block_state = BlockState.START
                        starts += 1
                        
                    case "e":
                        block_state = BlockState.END
                        ends += 1

                    case _:
                        raise Exception(f"Unknown block char '{block_char}': row {row_ind} col {col_ind}")
                
                cur_block = Block(block_length, block_state, row_ind, col_ind, self.screen)
                maze_row.append(cur_block)
            
            maze.append(maze_row)
        
        if starts != 1 or ends != 1:
            raise Exception(f"Exactly one start and end required. This maze has starts:{starts}, ends:{ends}.")

        return maze


# ========To Test (Idk how to make it work)========#
# pygame.init()
# screen = pygame.display.set_mode((MAZE_SIZE,MAZE_SIZE))
# screen.fill(RED)
# with open("PreMade_Mazes/10x10_Maze1.csv", "r") as f:
#     maze = Maze(f, screen)
# maze.draw()
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()
#     pygame.display.update()