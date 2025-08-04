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

# GBFS Section
def heuristic(start: tuple[int, int], goal: tuple[int, int]):
    '''
    Calculate heuristic based on 4-Directional Manhattan Distance formula.
    scale_factor is used to scale the heuristic for tie-breaking. 
        Should be no more (1 + 1/(expected maximum path length)) for our use case
    '''

    dx = abs(goal[0] - start[0])
    dy = abs(goal[1] - start[1])

    return (dx + dy)

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

def geedy_best_first_search(maze_grid: list[list], start: tuple[int, int], end: tuple[int, int]):
    start_time = time()

    # Dictionary initializer of format: `(coord.x, coord.y): -1`
    h_scores = {(vertex.row, vertex.col): -1 for line in maze_grid for vertex in line}
    
    # Start block parameters
    start_h = heuristic(start=start, goal=end)
    h_scores[start] = start_h

    # min heap for available routes, first element based ordering 
    frontier = [(start_h, start)]

    predecessors = {}
    explored = []

    endFound = False

    while len(frontier) > 0 and not endFound:
        curH, curNode = heapq.heappop(frontier)

        # Add to the list of explored blocks
        explored.append(curNode)

        # If this path is worse than the current best, skip it
        if h_scores[curNode] != -1 and curH > h_scores[curNode]:
            continue

        if curNode == end: # First path to end will always be shortest; safe to break
            endFound = True
            break

        # Process neighbors
        for nDist, nNode in grid_neighbors(grid=maze_grid, source=curNode):
            nrow, ncol = nNode
            nblock = maze_grid[nrow][ncol]

            if (nblock.state == BlockState.WALL): #ignore walls
                continue

            # calculate neighboring f score
            h = heuristic(start=nNode, goal=end)
            
            if h_scores[nNode] == -1 or h < h_scores[nNode]:
                h_scores[nNode] = h
                heapq.heappush(frontier, (h, nNode))
                predecessors[nNode] = curNode
    
    solve_time = time() - start_time

    if not endFound:
        return explored, []
    
    final_path = [end]

    node = end
    while node in predecessors:
        node = predecessors[node]
        final_path.append(node)
    
    return explored, list(reversed(final_path)), solve_time

def Dijkstra(maze: Maze):
    """
    Runs Dijkstra's shortest path algorithm on the maze's adjacency list.
    Returns:
        explored: list of (row, col) coordinates visited in order
        final_path: list of (row, col) coordinates in the shortest path
    """
    # Build the adjacency list from the maze layout
    maze.create_graph()
    graph = maze.graph_points.graph
    coord_to_id = maze.graph_points.coord_to_verNum
    id_to_coord = maze.graph_points.verNum_to_coord

    start_coord = maze.start_coord
    end_coord = maze.end_coord

    # Convert coordinates to vertex IDs
    start_id = coord_to_id.get(start_coord)
    end_id = coord_to_id.get(end_coord)

    if start_id is None or end_id is None:
        print("Start or end not found in graph.")
        return [], []

    # Distance to each vertex (default = infinity)
    dist = {v: float("inf") for v in graph}
    dist[start_id] = 0

    # Predecessors for path reconstruction
    prev = {}

    # Priority queue: (distance_from_start, vertex_id)
    pq = [(0, start_id)]
    explored = []

    while pq:
        cur_dist, u = heapq.heappop(pq)

        # If we've reached the end, stop early
        if u == end_id:
            break

        # Skip if we've already found a shorter path
        if cur_dist > dist[u]:
            continue

        # Mark as explored
        explored.append(id_to_coord[u])

        # Relax edges
        for neighbor, weight in graph[u]:
            new_dist = cur_dist + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = u
                heapq.heappush(pq, (new_dist, neighbor))

    # --- Path reconstruction ---
    final_path = []
    cur = end_id
    while cur in prev:
        final_path.append(id_to_coord[cur])
        cur = prev[cur]
    final_path.append(start_coord)  # include the start
    final_path.reverse()

    return explored, final_path
