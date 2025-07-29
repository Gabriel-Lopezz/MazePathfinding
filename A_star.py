import heapq
from adjacencyList import AdjacencyList
from block import Block

def heuristic(current: tuple[int, int], target: tuple[int, int], min_dist: int ):
    '''
    Calculate heuristic based on 4-Directional Manhattan Distance formula.
    min_dist is used to scale the heuristic. It should be the shortest path from one intersection to another.
    '''
    dx = abs(target.x - current.x)
    dy = abs(target.y - current.y)

    return min_dist * (dx + dy)

def a_star(adj_list: AdjacencyList):
    visited = {}
    distances = []

    for intersection in adj_list.graph.keys:
        pass #Continue logic