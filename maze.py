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
        Draws the maze blocks using 'dirty rectangles' technique. Adds blocks' rects to a list; the list is used to update only necessary portions of the screen.
        '''
        blocks = []

        for row in self.maze:
            for block in row:
                blocks.append(block.rect)

        pygame.display.update(blocks)

    def maze_from_file(self, file: _io.TextIOWrapper) -> list[list[Block]]:
        start = time.time()

        maze = []

        rows = sum(1 for line in file)
        file.seek(0) # Reset file handle to start
        
        reader = csv.reader(file)
        cols = len(next(reader))

        # Reset CSV reader
        file.seek(0)
        reader = csv.reader(file)

        starts = 0
        ends = 0

        row_ind = col_ind = 0

        for row in reader:
            maze_row = []

            for block_str in row:
                block_length = MAZE_SIZE / rows
                block_char = block_str.strip()
                block_state = None

                match(block_char.lower()):
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

                    case _: # non-existent case
                        raise Exception(f"Could not resolve Block character {block_char}: row {row_ind}, col {col_ind}")
                
                if (starts > 1 or ends > 1):
                    raise Exception(f"Could not resolve Maze File. More than one start/end found: row {row_ind}, col {col_ind}")

                cur_block = Block(size=block_length, state=block_state, row=row_ind, col=col_ind, screen=self.screen)
                maze_row.append(cur_block)
            
            maze.append(maze_row)
        
        file.close() # Close the file
        

        print("Time taken", time.time() - start)

        return maze