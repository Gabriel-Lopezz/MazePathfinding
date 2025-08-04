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

# GBFS Section
def heuristic(start: tuple[int, int], goal: tuple[int, int]):
    '''
    Calculate heuristic based on 4-Directional Manhattan Distance formula
    scale_factor is used to scale the heuristic for tie-breaking
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

def geedy_best_first_search(maze: Maze):
    start_time = time()
    
    maze_grid = maze.maze_array
    start, end = maze.start_coord, maze.end_coord

    # Dictionary initializer of format: `(coord.x, coord.y): -1`
    h_scores = {(vertex.row, vertex.col): -1 for line in maze_grid for vertex in line}
    
    # Start block parameters
    start_h = heuristic(start=start, goal=end)
    h_scores[start] = start_h

    # min heap for available routes, (heuristic, grid indices)
    frontier = [(start_h, start)]

    predecessors = {}
    explored = []

    endFound = False

    while frontier:
        cur_h, cur_node = heapq.heappop(frontier)

        # Add to the list of explored blocks
        explored.append(cur_node)

        # If this path is worse than the current best, skip it
        if h_scores[cur_node] != -1 and cur_h > h_scores[cur_node]:
            continue

        if cur_node == end: # First path to end will always be shortest; safe to break
            endFound = True
            break

        # Process neighbors
        for n_h, n_node in grid_neighbors(grid=maze_grid, source=cur_node):
            nrow, ncol = n_node
            nblock = maze_grid[nrow][ncol]

            if (nblock.state == BlockState.WALL): #ignore walls
                continue

            # calculate neighboring f score
            h = heuristic(start=n_node, goal=end)
            
            if h_scores[n_node] == -1 or h < h_scores[n_node]:
                h_scores[n_node] = h
                heapq.heappush(frontier, (h, n_node))
                predecessors[n_node] = cur_node
    
    solve_time = time() - start_time

    if not endFound:
        return explored, [], solve_time
    
    final_path = [end]

    node = end
    while node in predecessors:
        node = predecessors[node]
        final_path.append(node)
    
    return explored, list(reversed(final_path)), solve_time

# Dijkstra section

def expand_path(maze: Maze, node_a: tuple[int, int], node_b: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Expands a straight corridor between two graph points into all intermediate coordinates
    node_a, node_b are (row, col) tuples
    """
    expanded = [node_a]
    r1, c1 = node_a
    r2, c2 = node_b

    dr = 0 if r1 == r2 else (1 if r2 > r1 else -1)
    dc = 0 if c1 == c2 else (1 if c2 > c1 else -1)

    r, c = r1, c1
    while (r, c) != (r2, c2):
        r += dr
        c += dc
        if maze.maze_array[r][c].state != BlockState.WALL:
            expanded.append((r, c))
        else:
            raise RuntimeError(f"Wall encountered in expanded path at {(r, c)}")

    return expanded

def Dijkstra(maze: Maze):
    """
    Runs Dijkstra's shortest path algorithm on the maze's adjacency list,
    but expands graph edges into full maze corridors for visualization.
    Returns:
        explored: list of (row, col) coordinates visited in order
        final_path: list of (row, col) coordinates in the shortest path
        solve_time: time taken to solve
    """

    start_time = time()

    maze.create_graph()
    graph = maze.graph_points.graph
    coord_to_id = maze.graph_points.coord_to_verNum
    id_to_coord = maze.graph_points.verNum_to_coord

    start_coord = maze.start_coord
    end_coord = maze.end_coord

    start_id = coord_to_id.get(start_coord)
    end_id = coord_to_id.get(end_coord)

    if start_id is None or end_id is None:
        print("Start or end not found in graph.")
        return [], [], 0

    dist = {v: float("inf") for v in graph}
    dist[start_id] = 0
    prev = {}

    pq = [(0, start_id)]
    explored = []

    while pq:
        cur_dist, u = heapq.heappop(pq)

        if cur_dist > dist[u]:
            continue

        # Always expand path to current node
        if u in prev:
            expanded_corridor = expand_path(maze, id_to_coord[prev[u]], id_to_coord[u])
            explored.extend(expanded_corridor[1:])
        else:
            explored.append(id_to_coord[u])  # Start node

        if u == end_id:
            break  # Now we break after marking the final segment

        # Relax edges
        for neighbor, weight in graph[u]:
            new_dist = cur_dist + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = u
                heapq.heappush(pq, (new_dist, neighbor))

    solve_time = time() - start_time

    # Path reconstruction
    path_nodes = []
    cur = end_id
    while cur in prev:
        path_nodes.append(id_to_coord[cur])
        cur = prev[cur]
    path_nodes.append(start_coord)
    path_nodes.reverse()

    # Expand final path fully
    final_path = []
    for i in range(len(path_nodes) - 1):
        expanded_corridor = expand_path(maze, path_nodes[i], path_nodes[i + 1])
        if final_path:
            final_path.extend(expanded_corridor[1:])
        else:
            final_path.extend(expanded_corridor)

    return explored, final_path, solve_time
