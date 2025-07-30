import csv
import pygame
import _io
from config import *
from block import Block, BlockState
import time

class Maze:
    def __init__(self, maze_file: _io.TextIOWrapper, screen: pygame.Surface):
        self.screen = screen
        
        # has no start or end coordinate by default
        self.start_coord = (-1,-1)
        self.end_coord = (-1,-1)
        
        # Default grid data and block length
        self.block_length = 0
        self.cols = 0
        self.rows = 0

        self.maze_array = self.maze_from_file(maze_file)

        self.intersections = None

    def create_maze(maze_file: _io.TextIOWrapper, screen: pygame.Surface):
        try:
            new_maze = Maze(maze_file=maze_file, screen=screen)
        except Exception as maze_exception:
            return False, str(maze_exception)

        return True, new_maze

    def redraw_blocks(self, blocks: list[Block]):
        blocks_updating = [block.rect for block in blocks]

        pygame.display.update(blocks_updating)

    def draw(self):
        '''
        Loads all the maze blocks into the screen buffer. Renders the changes after loading all blocks
        '''
        for row in self.maze_array:
            for block in row:
                block.draw()
        
        pygame.display.flip()
    
    def clear(self):
        '''
        Clears maze data, draws a white square to cover Maze window, and updates display
        '''
        self.maze_array = None
        pygame.draw.rect(
            surface=self.screen,
            color=WHITE,
            rect=(MAZE_PADDING_LEFT, MAZE_PADDING_TOP, MAZE_SIZE, MAZE_SIZE)
        )
        pygame.display.flip()

    def maze_from_file(self, file: _io.TextIOWrapper) -> list[list[Block]]:
        maze = []

        lines = list(file)
        self.rows = len(lines)
        
        reader = csv.reader(lines)
        self.cols = len(next(reader))

        if self.rows < 2 or self.cols < 2 or self.rows != self.cols:
            raise Exception(f"Maze must be square, at least 2x2. This maze has rows:{self.rows} cols:{self.cols}")
        
        self.block_length = MAZE_SIZE / self.rows
        
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
                        self.start_coord = (row_ind,col_ind)
                        starts += 1
                        
                    case "e":
                        block_state = BlockState.END
                        self.end_coord = (row_ind, col_ind)
                        ends += 1

                    case _:
                        raise Exception(f"Unknown block char '{block_char}': row {row_ind} col {col_ind}")
                
                cur_block = Block(self.block_length, block_state, row_ind, col_ind, self.screen)
                maze_row.append(cur_block)
            
            maze.append(maze_row)
        
        if starts > 1 or ends > 1:
            raise Exception(f"No more than 1 start point or end point. This maze has starts:{starts}, ends:{ends}.")
        return maze
    # returns in (x,y) format
    def get_adjacent(self, x, y):
        dx = [1, -1, 0, 0]  # right, left
        dy = [0, 0, 1, -1]  # down, up
        adjacents = set()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if (nx < 0 or ny < 0
                or nx >= self.cols or ny >= self.rows
                or self.maze_array[ny][nx].state == BlockState.WALL):
                continue
            adjacents.add((nx, ny))
        return adjacents
    # A coordinate has a turn if its only TWO neighbors have a different x and y coordinate
    def is_turn(self,  neighbor1: tuple, neighbor2: tuple) -> bool:
        dx, dy = neighbor1
        vx, vy = neighbor2
        return (dx != vx and dy != vy)
    
    def click_box(self, x, y, event_type):
        '''event_type: 1 = left click, 3 = right click'''

        # if you load a maze, then unload it, then you click on the empty area where the maze was, 
        # the program crashes without this next if statement - Andres
        if self.maze_array is None:
            return

        # the following gives us the proper padded coordinates:
        x -= MAZE_PADDING_LEFT
        y -= MAZE_PADDING_TOP

        if not (0 <= x < self.cols * self.block_length and 
                0 <= y < self.rows * self.block_length):
            return
        
        # get the block object from the respective coordinate
        maze_x = int(x // self.block_length)
        maze_y = int(y // self.block_length)

        if not (0 <= maze_x < self.cols and 
                0 <= maze_y < self.rows):
            return

        clicked_box = self.maze_array[maze_y][maze_x]

        if clicked_box.state == BlockState.WALL:
            print("clicked on wall")
            return
        
        if event_type == 1:  # left click
            if self.start_coord != (-1, 1):
                old_y, old_x = self.start_coord
                self.maze_array[old_y][old_x].state = BlockState.OPEN
                self.maze_array[old_y][old_x].draw()
            
            clicked_box.state = BlockState.START
            clicked_box.draw()
            self.start_coord = (maze_y, maze_x)

        elif event_type == 3:  # right click
            if self.end_coord != (-1, 1):
                old_y, old_x = self.end_coord
                self.maze_array[old_y][old_x].state = BlockState.OPEN
                self.maze_array[old_y][old_x].draw()

            clicked_box.state = BlockState.END
            clicked_box.draw()
            self.end_coord = (maze_y, maze_x)
