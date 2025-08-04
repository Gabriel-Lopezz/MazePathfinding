from maze import Maze
from block import BlockState
from time import time
import heapq

# A* Section
def heuristic(source: tuple[int, int], goal: tuple[int, int]):
    '''
    Calculate heuristic based on 4-Directional Manhattan Distance formula
    '''

    dx = abs(goal[0] - source[0])
    dy = abs(goal[1] - source[1])

    return (dx + dy)

def grid_neighbors(grid: list[list], source: tuple[int, int]):
    '''
    Get the 4-directional neighbors of the given `source` node.
    Returns (heuristic, (row, col))
    '''
    row, col = source[0], source[1]

    above = (row-1, col)
    below = (row+1, col)
    left = (row, col-1)
    right = (row, col+1)

    nbors = []

    if row > 0:
        nbors.append(above)
    if row < len(grid) - 1:
        nbors.append(below)
    if col > 0:
        nbors.append(left)
    if col < len(grid[0]) - 1:
        nbors.append(right)

    return nbors

def a_star(maze: Maze):
    start_time = time()
    
    maze_grid = maze.maze_array
    start, end = maze.start_coord, maze.end_coord

    # Dictionary initializer of format: `(coord.x, coord.y): -1`
    g_scores = {(vertex.row, vertex.col): float('inf') for line in maze_grid for vertex in line}
    g_scores[start] = 0
    
    # Start block parameters
    start_h = heuristic(source=start, goal=end)

    # min heap for available routes, (heuristic, grid indices)
    frontier = [(start_h, start)]

    predecessors = {}
    explored = []

    endFound = False

    while frontier:
        cur_f, cur_node = heapq.heappop(frontier)

        # Add to the list of explored blocks
        explored.append(cur_node)

        # First path to end will always be shortest; safe to break
        if cur_node == end:
            endFound = True
            break

        # If this path is worse than the current best, skip it
        prev_f = g_scores[cur_node] + heuristic(source=cur_node, goal=end)
        if cur_f > prev_f:
            continue


        # Relax neighbors
        for n_node in grid_neighbors(grid=maze_grid, source=cur_node):
            nrow, ncol = n_node
            nblock = maze_grid[nrow][ncol]

            if (nblock.state == BlockState.WALL): # Ignore walls
                continue

            n_g = g_scores[cur_node] + 1
            if n_g < g_scores[n_node]:
                g_scores[n_node] = n_g
                n_f = n_g + heuristic(source=n_node,goal=end)
                heapq.heappush(frontier, (n_f, n_node))
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
