import csv
import pygame
import _io
from typing import Iterable
from AdjacencyList import AdjacencyList
from config import *
from collections import deque
from block import Block, BlockState
import time
import threading

class Maze:
    def __init__(self, maze_file: _io.TextIOWrapper, screen: pygame.Surface, result: list):
        '''
        Construct maze from file handle. Appends `self` to result list for threading support
        '''
        self.screen = screen
        
        # has no start or end coordinate by default
        self.start_coord = (-1,-1)
        self.end_coord = (-1,-1)
        
        # Default grid data and block length
        self.block_length = 0
        self.cols = 0
        self.rows = 0

        self.maze_array = self.maze_from_file(maze_file)
        maze_file.close()

        # Graph points include: intersections, turns, dead ends, & start/end points
        self.graph_points = AdjacencyList()

        result.append(self)

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
    
    def clear_path(self, block_inds: list[tuple[int, int]]):
        '''
        Refreshes the blocks at the given indices `block_inds`. (Returns the given blocks path back to OPEN block state)
        This also visually updates the blocks.
        '''
        for row, col in block_inds:
            cur_block = self.maze_array[row][col]
            cur_block.set_state(BlockState.OPEN)
            cur_block.draw()

    def maze_from_file(self, file: _io.TextIOWrapper) -> list[list[Block]]:
        maze = []

        lines = list(file)
        self.rows = len(lines)
        
        reader = csv.reader(lines)
        self.cols = len(next(reader))

        if self.rows < 2 or self.cols < 2 or self.rows != self.cols:
            raise Exception(f"Maze must be square, at least 2x2. This maze has rows:{self.rows} cols:{self.cols}")
        
        self.block_length = MAZE_SIZE // self.rows
        
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
    def get_adjacent(self, start_point: tuple):
        x,y = start_point
        # 0s are there so only either the x or y coordinate is changed in one loop
        dx = [1, -1, 0, 0]  # right, left
        dy = [0, 0, 1, -1]  # down, up
        adjacents = list()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            # if the "adjacent" node is out of bounds or a wall, ignore this nx, ny
            if (nx < 0 or ny < 0
                or nx >= self.cols or ny >= self.rows
                or self.maze_array[ny][nx].state == BlockState.WALL):
                continue
            adjacents.append((nx, ny))
        return adjacents

    def is_valid_graph_point(self, center: tuple, adjacents : list[tuple[int,int]]):
        '''
            a valid graph point is either a start/end point, intersection, turn, or dead-end
            # A coordinate has an intersection if it has more than 3 neighbors
            A coordinate has a turn if its only TWO neighbors have a different x and y coordinate
        '''
        x, y = center
        if self.maze_array[y][x] == BlockState.START or self.maze_array[y][x] == BlockState.END: # coordinate is a start/end point
            return True
        if len(adjacents) >= 3 or len(adjacents) == 1: # coordinate (x,y) is an intersection or a deadend
            return True
        if len(adjacents) == 2:
            adjacent1 ,adjacent2 = adjacents[0],adjacents[1]
            if adjacent1 == adjacent2: # guard against duplicate adjacent points
                return False
            ux, uy = adjacent1
            vx, vy = adjacent2
            dx1, dy1 = ux - x, uy - y # represents the change of direction from the first adjacent point
            dx2, dy2 = vx - x, vy - y # represents the change of direction from the second adjacent point
            # if at least one either of the changes of direction != 0, that means the line is not straight/ is a turn
            if dx1 + dx2 != 0 or dy1 +dy2 != 0:
                return True
        return False
    """
        After some thought, and based on what counts as graph points now, a "walk" the corridor approach seems better,
        where the algorithm will walk a path in a single direction until it reaches an valid graph point for all 4 directions
    """
    def walk_corridors(self, start_point, bfs_queue : deque[tuple], visited: set[tuple]):
        '''
            Will only walk through the corridors in all 4 directions of valid graph_points
            when it gets to a valid graph point, it will add it to the graph
        '''
        start_x, start_y = start_point
        # 0s are there so only either the x or y coordinate is changed in one loop
        dx = [1, -1, 0, 0]  # right, left
        dy = [0, 0, 1, -1]  # down, up
        for i in range(4):
            # (0,-1) up | (0, 1) down |(-1,0) left |(1,0) right |
            current_x = start_x + dx[i]
            current_y = start_y + dy[i]
            distance = 1
            # Safeguard for unwalkable coordinates
            if (current_x < 0 or current_y < 0
                    or current_x >= self.cols or current_y >= self.rows
                    or self.maze_array[current_y][current_x].state == BlockState.WALL):
                continue

            while True:
                # to check if it is a valid graph point
                current_adjacents = self.get_adjacent((current_x, current_y))
                if (self.is_valid_graph_point((current_x, current_y), current_adjacents)
                        and (current_x,current_y) not in visited ):# not visited[current_y][current_x]):
                    # For BFS traversal
                    visited.add((current_x,current_y))
                    bfs_queue.append((current_x, current_y))

                    self.graph_points.add_connection(
                        (start_x, start_y),
                        (current_x,current_y),
                        distance)
                    break

                # Moves through a corridor in the same direction
                next_x, next_y = current_x + dx[i], current_y + dy[i]
                # if the adjacent coordiante is out of bounds or a wall, break while loop
                if (next_x < 0 or next_y < 0
                        or next_x >= self.cols or next_y >= self.rows
                        or self.maze_array[next_y][next_x].state == BlockState.WALL):
                    break

                # goes onto the next block in the corridor
                current_x, current_y = next_x, next_y
                distance += 1


    def create_graph(self):
        '''
            Looks for all the intersection points of the maze to be added to the adjacency list
            Done by walking through every corridor of the maze in a singular direction until it hits an intersection
            Will use a BFS approach
        '''
        start_x, start_y = self.start_coord
        # Keeps track of Visited & ensures that each corridor is walked exaclty once
        # fixed spacing issue
        visited = set()
        visited.add((start_x,start_y))

        # stored as (x, y)
        q = deque()
        q.append((start_x,start_y))
        while q:
            # ux, uy is the "center" point, or current
            ux, uy = q.popleft()
            # BFS additional steps done in this method
            self.walk_corridors((ux,uy),q,visited)

        print("Graph created successfully")
    # == Visuals == #
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
