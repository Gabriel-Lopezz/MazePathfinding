from turtledemo.penrose import start
from pygame.mixer_music import queue
from collections import deque
from maze import Maze
from block import BlockState
from time import time
import heapq

def log_time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        func(*args, **kwargs)
        exe_time = time() - start_time
    
        return exe_time
    
    return wrapper

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

# A* Section
def scaled_heuristic(start: tuple[int, int], goal: tuple[int, int], scale_factor: int):
    '''
    Calculate heuristic based on 4-Directional Manhattan Distance formula.
    scale_factor is used to scale the heuristic for tie-breaking. 
        Should be no more (1 + 1/(expected maximum path length)) for our use case
    '''

    dx = abs(goal[0] - start[0])
    dy = abs(goal[1] - start[1])

    return (dx + dy) * scale_factor

def grid_neighbors(grid: list[list], source: tuple[int, int]):
    row, col = source[0], source[1]

    nbors = []

    if row > 0:
        nbors.append((1, (row-1, col)))
    if row < len(grid) - 1:
        nbors.append((1, (row+1, col)))
    if col > 0:
        nbors.append((1, (row, col-1)))
    if col < len(grid[0]) - 1:
        nbors.append((1, (row, col+1)))

    return nbors

def a_star(maze_grid: list[list], start: tuple[int, int], end: tuple[int, int]):
    start_time = time()

    # Dictionary initializer of format: `(coord.x, coord.y): -1`
    f_scores = {(vertex.row, vertex.col): -1 for line in maze_grid for vertex in line}
    distances = f_scores.copy()
    distances[start] = 0

    # heuristic scale factor:
    h_scale_factor = len(maze_grid) * len(maze_grid[0])
    
    # Start block parameters
    start_h = scaled_heuristic(start=start, goal=end, scale_factor=h_scale_factor)
    f_scores[start] = start_h

    # min heap for available routes, first element based ordering 
    frontier = [(start_h, start)]

    predecessors = {}
    explored = []

    endFound = False

    while len(frontier) > 0 and not endFound:
        curF, curNode = heapq.heappop(frontier)

        if curNode == end: # First path to end will always be shortest; safe to break
            break

        # If this path is worse than the current best, skip it
        if f_scores[curNode] != -1 and curF > f_scores[curNode]:
            continue

        explored.append(curNode) # Add to the list of explored blocks

        # Process neighbors
        for nDist, nNode in grid_neighbors(grid=maze_grid, source=curNode):
            nrow, ncol = nNode
            nblock = maze_grid[nrow][ncol]

            if (nblock.state == BlockState.WALL): #ignore walls
                continue

            # calculate neighboring f score
            g = distances[curNode] + nDist
            h = scaled_heuristic(start=nNode, goal=end, scale_factor=h_scale_factor)
            f = g + h
            
            if f_scores[nNode] == -1 or f < f_scores[nNode]:
                distances[nNode] = g
                f_scores[nNode] = f
                heapq.heappush(frontier, (f, nNode))
                predecessors[nNode] = curNode
                
                if nNode == end:
                    endFound = True
                    break
    
    solve_time = time() - start_time

    if not endFound:
        return explored, []
    
    final_path = []

    node = end
    while node in predecessors:
        node = predecessors[node]
        final_path.append(node)
    
    return explored, list(reversed(final_path)), solve_time


