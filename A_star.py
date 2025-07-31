import heapq
from block import Block, BlockState

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

def a_star(maze_grid: list[list[Block]], start: tuple[int, int], end: tuple[int, int]):
    # Dictionary initializer of format: `(coord.x, coord.y): -1`
    f_scores = {(vertex.row, vertex.col): -1 for line in maze_grid for vertex in line}
    distances = f_scores.copy()
    distances[start] = 0

    h_scale_factor = len(maze_grid) * len(maze_grid[0])

    step_cost = 1
    
    start_h = scaled_heuristic(start=start, goal=end, scale_factor=h_scale_factor)
    f_scores[start] = start_h

    # min heap for available routes, first element based ordering 
    frontier = [(start_h, start)]

    predecessors = {}

    endFound = False

    while len(frontier) > 0 and not endFound:
        curF, curNode = heapq.heappop(frontier)

        if curNode == end: # First path to end will always be shortest; safe to break
            break

        if f_scores[curNode] != -1 and curF > f_scores[curNode]:
            continue
        
        for nDist, nNode in grid_neighbors(grid=maze_grid, source=curNode):
            nrow, ncol = nNode
            nblock = maze_grid[nrow][ncol]

            if (nblock.state == BlockState.WALL):
                continue

            g = distances[curNode] + nDist
            h = scaled_heuristic(start=nNode, goal=end, scale_factor=h_scale_factor)
            scaled_h = h
            f = g + scaled_h
            
            if f_scores[nNode] == -1 or f < f_scores[nNode]:
                distances[nNode] = g
                f_scores[nNode] = f
                heapq.heappush(frontier, (f, nNode))
                predecessors[nNode] = curNode
                nblock.set_state(BlockState.EXPLORED)
                nblock.draw()
                
                if nNode == end:
                    endFound = True
                    break
    
    final_path = []
    node = end
    while node in predecessors:
        block = maze_grid[node[0]][node[1]]
        block.set_state(BlockState.FINAL)
        block.draw()
        node = predecessors[node]

    
    return list(reversed(final_path))


    return predecessors