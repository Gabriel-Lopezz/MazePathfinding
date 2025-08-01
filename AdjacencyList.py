class AdjacencyList:
    " Creates an adjacency list of all the intersections of the maze"
    def __init__(self):
        """Constructor for Adjacency List Object"""
        '''
        each intersection will be labled based on a vertex number, or its ID
        i.e: the base graph variable has a key: vertex number, and value of (connection, distance)
        the coord_to_verNum dictionary will store the vertex # as a value, with the key being the ID
        '''

        self.graph : dict[int, list[tuple[int,int]]] = {}
        self.vertex_num : int = 0
        # "Maps the vertex(intersection) to it's coordinate from the maze"
        self.intersection_coords : set[tuple[int,int]] = set() # stores what coords have been saved
        self.coord_to_verNum : dict[tuple[int,int],int] = {} # key: coordinate (y,x), value: vertex #
        self.verNum_to_coord : dict[int,tuple[int,int]] = {} # key: vertex #, value: coordinate (y,x)
    # Getters : for debugging
    def get_vertex_number(self, coord):
        return self.coord_to_verNum.get(coord)
    def get_vertices(self):
        """returns number of vertices"""
        return len(self.graph)
    def print_list(self):
        the_graph = self.graph
        for vertexNum, pair in the_graph.items():
            print(f"{vertexNum}: ")
            for value in pair:
                connection, distance = value
                print(f"->[{connection}:{distance}]")


    def add_connection(self, _from:tuple[int,int], _to:tuple[int,int], _weight):
        # Checks if the from and to coordinates have already been added to the list
        if _from not in self.intersection_coords:
            self.intersection_coords.add(_from)
            self.coord_to_verNum[_from] = self.vertex_num
            self.verNum_to_coord[self.vertex_num] = _from
            self.graph[self.vertex_num] = []
            self.vertex_num += 1
        if _to not in self.intersection_coords:
            self.intersection_coords.add(_to)
            self.coord_to_verNum[_to] = self.vertex_num
            self.verNum_to_coord[self.vertex_num] = _to
            self.graph[self.vertex_num] = []
            self.vertex_num += 1
        from_vertex = self.coord_to_verNum[_from]
        to_vertex = self.coord_to_verNum[_to]
        self.graph[from_vertex].append((to_vertex,_weight))
        self.graph[to_vertex].append((from_vertex, _weight)) # done to make undirected graph