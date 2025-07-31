from turtledemo.penrose import start
from pygame.mixer_music import queue
from collections import deque
from maze import Maze
from block import BlockState


# def BFS_for_intersections(start_point : tuple , maze_obj : Maze):
#     '''
#     Looks for all the intersection points of the maze to be added to the adjacency list
#     '''
#     start_x, start_y = start_point
#     columns , rows = maze_obj.cols, maze_obj.rows
#     array_rep = maze_obj.maze_array
#     maze_graph = maze_obj.graph_points
#     # keeps track of the distance between each maze coord that would go in the graph
#     distance = [[-1 for i in range(columns)] for j in range(rows)]
#     distance[start_y][start_x] = 0
#     # Keeps track of Visited
#     visited = [[False for i in range(columns)] for j in range(rows)]
#     visited[start_y][start_x] = True
#
#     # stored as (x, y)
#     q = deque()
#     q.append((start_x,start_y))
#     from_point = start_x,start_y
#     while q:
#         # ux, uy is the "center" point, or current
#         ux, uy = q.popleft()
#         adjacents = array_rep.get_adjacent(ux,uy)
#         for vx,vy in adjacents:
#           if not visited[vy][vx]:
#             visited[vy][vx] = True
#             distance[vy][vx] = distance[uy][ux] + 1
#             curr_distance = distance[vy][vx]
#             q.append((vx,vy))
#         if maze_obj.is_valid_graph_point((ux,uy),adjacents): #a valid graph point is either a start/end point, intersection, turn, or dead-end
#             maze_graph.add_connection(from_point,(ux,uy),curr_distance)
#
#
#     return True


