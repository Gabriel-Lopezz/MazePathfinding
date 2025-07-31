import heapq
from block import Block, BlockState

def heuristic(start: tuple[int, int], goal: tuple[int, int], min_dist: int ):
    '''
    Calculate heuristic based on 4-Directional Manhattan Distance formula.
    min_dist is used to scale the heuristic. It should be the shortest path from one intersection to another.
    '''
    dx = abs(goal[0] - start[0])
    dy = abs(goal[1] - start[1])

    return min_dist * (dx + dy)

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

def a_star(maze_grid: list[list[Block]], start: tuple[int, int], end: tuple[int, int]):
    # Dictionary initializer of format: `(coord.x, coord.y): -1`
    f_scores = {(vertex.row, vertex.col): -1 for line in maze_grid for vertex in line}
    distances = f_scores.copy()
    distances[start] = 0
    
    start_h = heuristic(start=start, goal=end, min_dist=1)
    f_scores[start] = start_h

    # min heap for available routes, first element based ordering 
    frontier = [(start_h, start)]

    predecessors = {}

    while len(frontier) > 0:
        curF, curNode = heapq.heappop(frontier)

        if curNode == end: # First path to end will always be shortest; safe to break
            break

        if f_scores[curNode] != -1 and curF > f_scores[curNode]:
            continue
        
        for nDist, nNode in grid_neighbors(grid=maze_grid, source=curNode):
            if (maze_grid[nNode[0]][nNode[1]].state == BlockState.WALL):
                continue

            g = distances[curNode] + nDist
            h = heuristic(start=nNode, goal=end, min_dist=1)
            f = g + h
            
            if f_scores[nNode] == -1 or f < f_scores[nNode]:
                distances[nNode] = g
                f_scores[nNode] = f
                heapq.heappush(frontier, (f, nNode))
                predecessors[nNode] = curNode
    
    return predecessors