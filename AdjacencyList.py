class AdjacencyList:
    " Creates an adjacency list of all the intersections of the maze"
    def __init__(self):
        """Constructor for Adjacency List Object"""
        self.graph = {}
        "Maps the vertex(intersection) to it's coordinate from the maze"
        self.vertex2coord = {} # key: vertex #, value: coordinate (y,x)
        self.coord2vertex = {} # key: coordinate (y,x), value: vertex #
    # Getters
    def get_vertex(self, coord):
        return
    def get_vertices(self):
        """returns number of vertices"""
        return len(self.graph)
    def get_edges(self):
        return
