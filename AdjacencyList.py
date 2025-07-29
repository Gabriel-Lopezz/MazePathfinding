class AdjacencyList:
    " Creates an adjacency list of all the intersections of the maze"
    def __init__(self):
        """Constructor for Adjacency List Object"""
        '''
        each intersection will be labled based on a vertex number, or its ID
        the coord_to_verNum dictionary will store the vertex # as a value, with the key being the ID
        '''
        self.graph = dict(list[int])
        self.vertex_num = 0
        # "Maps the vertex(intersection) to it's coordinate from the maze"
        self.intersection_coords = set() # stores what coords have been saved
        self.coord_to_verNum = dict(tuple) # key: coordinate (y,x), value: vertex #
    # Getters
    def get_vertex(self, coord):
        x, y = coord
        return self.coord_to_verNum.get((x, y))
    def get_vertices(self):
        """returns number of vertices"""
        return len(self.graph)
    def add_vertex(self, _from:tuple, _to:tuple, _weight):
        # Checks if the from and to coordinates have already been added to the list
        if _from not in self.intersection_coords:
            self.intersection_coords.add(_from)
            self.coord_to_verNum[_from] = self.vertex_num
            self.graph[self.vertex_num] = []
            self.vertex_num += 1
        if _to not in self.intersection_coords:
            self.intersection_coords.add(_to)
            self.coord_to_verNum[_to] = self.vertex_num
            self.graph[self.vertex_num] = []
            self.vertex_num += 1
        from_vertex = self.coord_to_verNum[_from]
        to_vertex = self.coord_to_verNum[_to]
        self.graph[from_vertex].append((to_vertex,_weight))
        self.graph[to_vertex].append((from_vertex, _weight)) # done to make undirected graph