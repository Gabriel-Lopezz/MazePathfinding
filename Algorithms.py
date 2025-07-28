from turtledemo.penrose import start
from pygame.mixer_music import queue
from collections import deque
from maze import Maze
from block import BlockState

# def get_adjacent(x,y,col,rows, maze_array):
#     dx = [1, -1, 0, 0] # right, left
#     dy = [0, 0, 1, -1] # down, up
#     adjacents = set()
#     for i in range(4):
#         nx = x + dx[i]
#         ny = y + dy[i]
#         if nx < 0 or ny < 0 or nx >= col or ny >= rows or maze_array[ny][nx].state == BlockState.WALL:
#           continue
#         adjacents.add((nx,ny))
#     return adjacents

def BFS_for_intersections(start_point : tuple , maze_obj : Maze):
    '''
    Looks for all the intersection points of the maze to be added to the adjacency list
    '''
    count = 0
    start_x, start_y = start_point
    columns = maze_obj.cols, rows = maze_obj.rows
    array_rep = maze_obj.maze_array

    # Keeps track of Visited
    visited = [[False for i in range(columns)] for j in range(rows)]
    visited[start_y][start_x] = True

    # stored as (x, y)
    q = deque()
    q.append((start_x,start_y))
    intersections = set()
    while q.count !=0:
        ux, uy = q.popleft()
        neighbors = deque() # empty queue
        for vx,vy in maze_obj.get_adjacent(ux,uy,columns,rows):
          if not visited[vy][vx]:
            visited[vy][vx] = True

            q.append((vx,vy))
            neighbors.append((vx,vy))
        if len(neighbors) >= 3: #intersection if it has >2 adjacent open paths
            intersections.add((ux,uy))


    return intersections


