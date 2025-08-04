import pygame
import tkinter
from tkinter import filedialog
import sys
from threading import Thread
import gui
from maze import Maze
from constants import *
from block import Block, BlockState
from enum import Enum
import Algorithms
from typing import Generator, Callable

class AppState(Enum):
    MAZE_NOT_LOADED = 0
    MAZE_LOADED = 1
    TRAVERSING = 2
    FINISHED = 3
class Algorithm_Choice(Enum):
    NONE = 0
    GBFS = 1
    DIJKSTRAS = 2
class Traversal_Method(Enum):
    NONE = 0
    INSTANT = 1
    PROCEDUAL = 2
'''
    Prompts the user's file system dialog box and returns the file data
'''
def prompt_file():
    tk_widget = tkinter.Tk()
    tk_widget.withdraw() # Makes the Tkinter window invisible

    # Open's the OS dialog box for file selection
    file_info = filedialog.askopenfile(title="Select CSV to Load", filetypes=[("CSV File", "*.csv")])

    if (file_info and file_info.name[-4:] != ".csv"): # Need to validate that file was indeed CSV
        file_info = None

    tk_widget.destroy() # Delete widget after user is done selecting

    return file_info


# render_maze logic:
# sets the max frame rate given the dimensions of our maze (rowsxcols),
# multiplies a speed factor to better control drawing speed.

def render_maze(maze: Maze):
    maze.draw()
    app_state = AppState.MAZE_LOADED
    max_frame_rate = len(maze.maze_array) * len(maze.maze_array[0]) * SPEED_FACTOR
    pygame.display.flip()

    return app_state, max_frame_rate

def execute_and_display_stats(maze: Maze, algorithm: Callable, exec_time_value: gui.Text, blocks_traversed_value: gui.Text, optimal_path_length_value: gui.Text):
    explored_inds, optimal_path_inds, solve_time = algorithm(maze = maze)

    exec_time_value.text = "<0.0001s" if round(solve_time, 4) == 0.0 else str(round(solve_time, 4))
    blocks_traversed_value.text = str(len(explored_inds))
    optimal_path_length_value.text = str(len(optimal_path_inds))
    return explored_inds,optimal_path_inds

def visualize_progressively(maze: Maze, explored_inds: list[tuple[int, int]], path_inds: list[tuple[int, int]]):
    maze_grid = maze.maze_array

    blocks_per_frame = 1

    # We will draw a ratio `percent_blocks_drawn` of the explored_inds path per frame
    # For small graphs, this will be lower than 1. We need at least one block drawn per frame
    percent_blocks_drawn = 0.0005
    blocks_per_frame = max(int(len(explored_inds) * percent_blocks_drawn), 1)

    # Logic for drawing mazes, yields if we are still drawing (draws between start and end)
    for i in range(1, len(explored_inds) - 1, blocks_per_frame):
        for j in range(blocks_per_frame):
            ind = i + j
            if ind >= len(explored_inds) - 1:
                break

            row, col = explored_inds[ind]
            block = maze_grid[row][col]
            block.set_state(BlockState.EXPLORED)
            block.draw()
        
        yield True
    
    for i in range(1, len(path_inds) - 1, blocks_per_frame):
        for j in range(blocks_per_frame):
            ind = i + j
            if ind >= len(path_inds) - 1:
                break

            row, col = path_inds[ind]
            block = maze_grid[row][col]
            block.set_state(BlockState.FINAL)
            block.draw()

        yield True

    yield False

def visualize_instantly(maze: Maze, explored_inds: list[tuple[int, int]], path_inds: list[tuple[int, int]]):
    for i in range(1, len(path_inds) - 1):
        row, col = path_inds[i]
        block = maze.maze_array[row][col]
        block.set_state(BlockState.FINAL)
        block.draw()

    pygame.display.flip()
    

def main():
    pygame.init()

    screen = pygame.display.set_mode((RES_WIDTH,RES_HEIGHT))
    pygame.display.set_caption("Maze Pathfinding")

    clock = pygame.time.Clock()

    running = True

    # Maze object, maze state and maze window border (as kwargs for draw function)
    maze = None
    app_state = AppState.MAZE_NOT_LOADED
    # will change based on the algorithm/traversal user chooses
    algorithm = Algorithm_Choice.NONE
    traversal = Traversal_Method.NONE
    algorithm = Algorithm_Choice.GBFS

    '''
    Setup GUI elements
    '''
    screen.fill(WHITE)

    upload_button, preload_button, draw_progressively_button, draw_solution_instantly_button, unload_button, gbfs, dijkstras_button = gui.create_buttons(screen)
    exec_time_value, blocks_traversed_value, optimal_path_length_value = gui.create_results(screen=screen)
    # Storing in arrays makes it cleaner to print all visuals for that state
    all_buttons = [upload_button, preload_button, draw_progressively_button, draw_solution_instantly_button, unload_button, gbfs, dijkstras_button]
    all_stats_values: list[gui.Text] = [exec_time_value, blocks_traversed_value, optimal_path_length_value]

    error_message: gui.Text = None

    pygame.display.flip()

    '''
    Algorithm traversal path outputs
    '''

    explored_inds = []
    optimal_path_inds = []

    '''
    Maze drawing variables
    '''
    is_maze_drawing = False
    maze_animator: Generator[bool] = None # Generator for drawing
    target_frame_rate = 60 # Default frame rate; frame rate ~ animation speed

    '''
    Loading maze thread and result (array because it is easiest way to deal with returning value from thread)
    '''
    thread_load_maze: Thread  = None # Thread used for loading maze in background
    load_maze_result: list[tuple[bool, Maze|str]] = [] # Will hold maze object when thread is done

    while running:
        # If we are loading the maze, and have gotten a result, handle the result
        if thread_load_maze and len(load_maze_result) > 0:
            load_status, maze_output = load_maze_result[0]
            print("Finished loading, STATUS:", load_status)

            if load_status: # If successful
                maze = maze_output
                app_state, target_frame_rate = render_maze(maze=maze)
            else:
                err_msg = "ERROR: " + maze_output
                error_txt = gui.create_error_message(screen=screen, error_message=err_msg)
                error_txt.draw()
            
            # Clean up thread variables
            thread_load_maze = None
            load_maze_result.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Flags if the path drawing buttons were clicked
                draw_progressively_clicked = draw_progressively_button.is_clicked((x,y))
                draw_solution_instantly_clicked = draw_solution_instantly_button.is_clicked((x,y))

                # Handle button interactions if clicked and enabled
                if upload_button.is_clicked((x, y)):
                    upload_button.clicked()

                    maze_file = prompt_file()

                    if maze_file:
                        thread_load_maze = Thread(target=Maze.create_maze, args=(maze_file, screen, load_maze_result))
                        thread_load_maze.start()

                elif preload_button.is_clicked((x, y)):
                    preload_button.clicked()

                    maze_file = open("PreMade_Mazes/10x10_Maze1.csv", "r")
                    thread_load_maze = Thread(target=Maze.create_maze, args=(maze_file, screen, load_maze_result))
                    thread_load_maze.start()
                        
                elif unload_button.is_clicked((x, y)):
                    unload_button.clicked()

                    # Clear maze of its data and visually remove 
                    if maze:
                        maze.clear()

                    # Empty algorithm path outputs
                    explored_inds = []
                    optimal_path_inds = []
                    
                    # Clear the text from our result stats
                    for stat in all_stats_values:
                        stat.text = ""

                    app_state = AppState.MAZE_NOT_LOADED
                    is_maze_drawing = False
                
                elif (draw_progressively_clicked or draw_solution_instantly_clicked) and algorithm != Algorithm_Choice.NONE and app_state != AppState.MAZE_NOT_LOADED:
                    if draw_progressively_clicked:
                        draw_progressively_button.clicked()
                    else:
                        draw_solution_instantly_button.clicked()

                    algorithm_selected = Algorithms.geedy_best_first_search if algorithm == Algorithm_Choice.GBFS else Algorithms.Dijkstra

                    # Clear any previous error message if there was one
                    if error_message:
                        error_message.clear()
                        error_message = None
                    
                    # If an start or end is missing, display error and skip to next iteration
                    if maze.start_coord == (-1, -1):
                        error_message = gui.create_error_message(screen=screen, error_message="No start position in maze. Please left-click an open block.")
                        continue
                    
                    elif maze.end_coord == (-1, -1):
                        error_message = gui.create_error_message(screen=screen, error_message="No end position in maze. Please right-click an open block.")
                        continue
                    
                    app_state = AppState.FINISHED
                    is_maze_drawing = False # Interrupt any current drawing
                    maze.clear_path(explored_inds[1:]) # Remove any paths marked except start block

                    explored_inds, optimal_path_inds = execute_and_display_stats(maze=maze, algorithm=algorithm_selected, exec_time_value=exec_time_value, 
                                                                                    blocks_traversed_value=blocks_traversed_value, optimal_path_length_value=optimal_path_length_value)

                    if draw_progressively_clicked:
                        maze_animator = visualize_progressively(maze=maze, explored_inds=explored_inds, path_inds=optimal_path_inds)
                        is_maze_drawing = True
                    else:
                        visualize_instantly(maze=maze, explored_inds=explored_inds, path_inds=optimal_path_inds)

                elif gbfs.is_clicked((x,y)) and algorithm != Algorithm_Choice.GBFS:
                    gbfs.clicked()
                    algorithm = Algorithm_Choice.GBFS
                
                elif dijkstras_button.is_clicked((x,y)) and algorithm != Algorithm_Choice.DIJKSTRAS:
                    dijkstras_button.clicked()
                    algorithm = Algorithm_Choice.DIJKSTRAS

                # Maze interaction: box clicks
                elif maze and MAZE_PADDING_LEFT <= x <= MAZE_PADDING_LEFT + MAZE_SIZE and MAZE_PADDING_TOP <= y <= MAZE_PADDING_TOP + MAZE_SIZE\
                        and app_state != AppState.FINISHED:
                    maze.click_box(x, y, event.button)

        # enabling/disabling buttons based on state
        upload_button.set_enabled(app_state == AppState.MAZE_NOT_LOADED)
        preload_button.set_enabled(app_state == AppState.MAZE_NOT_LOADED)
        unload_button.set_enabled(app_state in (AppState.MAZE_LOADED, AppState.FINISHED))
        draw_progressively_button.set_enabled(app_state != AppState.MAZE_NOT_LOADED)
        draw_solution_instantly_button.set_enabled(app_state != AppState.MAZE_NOT_LOADED)
        dijkstras_button.set_enabled(algorithm == Algorithm_Choice.GBFS and app_state != AppState.MAZE_NOT_LOADED)
        gbfs.set_enabled(algorithm == Algorithm_Choice.DIJKSTRAS and app_state != AppState.MAZE_NOT_LOADED)
        # we can add more buttons and enable/disabled them whenever

        # maze_drawer is the generator called from visualize_progressively
        if is_maze_drawing:
            is_maze_drawing = next(maze_animator)

        # Draw all buttons regardless of state
        for button in all_buttons: 
            button.draw()
        
        for stat_values in all_stats_values:
            stat_values.clear()
            stat_values.draw()

        if error_message:
            error_message.draw()

        clock.tick(target_frame_rate)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
