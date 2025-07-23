class maze:
    def __init__(self, columns, rows):
        "creates a maze with all open spaces"
        "maybe it can take in a string and then just initialises it with that info"
        self.maze = [['.' for _ in range(columns)] for _ in range(rows)]
