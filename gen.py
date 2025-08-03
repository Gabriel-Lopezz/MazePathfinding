import random

def generate_maze(width, height):
    # Initialize maze with walls
    maze = [['#' for _ in range(width)] for _ in range(height)]
    
    # Start from a position not on the border
    start_x, start_y = random.randrange(1, width-1, 2), random.randrange(1, height//8, 2)
    end_x, end_y = random.randrange(1, width-1, 2), random.randrange(height*7//8, height-1, 2)
    
    # Mark start and remember its position
    maze[start_y][start_x] = 's'
    
    # Stack for backtracking
    stack = [(start_x, start_y)]
    visited = {(start_x, start_y)}
    path_cells = [(start_x, start_y)]
    
    # Use depth-first search to carve paths
    while stack:
        x, y = stack[-1]
        
        # Define possible directions: right, down, left, up
        directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
        random.shuffle(directions)
        
        found_next = False
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check if neighbor is within bounds and not visited
            if 0 < nx < width-1 and 0 < ny < height-1 and (nx, ny) not in visited:
                # Carve path between current cell and neighbor
                maze[y + dy//2][x + dx//2] = '.'
                maze[ny][nx] = '.'
                
                # Add new cell to stack and mark as visited
                stack.append((nx, ny))
                visited.add((nx, ny))
                path_cells.append((nx, ny))
                
                found_next = True
                break
        
        if not found_next:
            stack.pop()
    
    # Place end point at a distant location from start
    path_cells.sort(key=lambda pos: (pos[1], pos[0]))  # Sort by y then x
    if len(path_cells) > 1:
        end_cell = path_cells[-1]
        maze[end_cell[1]][end_cell[0]] = 'e'
    
    return maze

def save_maze_to_csv(maze, filename):
    with open(filename, 'w') as f:
        for row in maze:
            f.write(','.join(row) + '\n')

if __name__ == "__main__":
    width, height = 1000, 1000  # 1000x1000 maze
    maze = generate_maze(width, height)
    save_maze_to_csv(maze, "maze_1000x100.csv")
    print(f"Maze generated and saved to maze_1000x100.csv")