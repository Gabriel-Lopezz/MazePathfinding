import heapq
from block import Block, BlockState

def heuristic(current: tuple[int, int], target: tuple[int, int], min_dist: int ):
    '''
    Calculate heuristic based on 4-Directional Manhattan Distance formula.
    min_dist is used to scale the heuristic. It should be the shortest path from one intersection to another.
    '''
    dx = abs(target.x - current.x)
    dy = abs(target.y - current.y)

    return min_dist * (dx + dy)

def neighbors(grid: list[list], source: tuple[int, int]):
    pass # To be implemented

def a_star(maze_grid: list[list[Block]], start: tuple[int, int], end: tuple[int, int]):
    # Dictionary initializer of format: `(coord.x, coord.y): -1`
    distances = {(vertex.row, vertex.col): -1 for line in maze_grid for vertex in line}

    endFound = False

    # min heap for available routes, first element based ordering 
    routes = [(0, start)]

    while len(routes) > 0:
        curNode, curDist = heapq.heappop(distances)

        if (curDist != 1 and curDist >= distances[curNode]):
            continue
        
        for neighbor, nDist in neighbors(grid=maze_grid, source=curNode):
            base_dist = curDist + nDist
            h = heuristic(current=curNode, target=end, min_dist=1)
            expected_dist = base_dist + h
            
            if expected_dist < distances[curNode] or distances[curNode] == -1:
                distances[curNode] = expected_dist
                heapq.heappush((base_dist + heuristic, neighbor))