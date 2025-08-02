import pygame
import tkinter
from tkinter import filedialog
import sys
from threading import Thread
from button import Button
from maze import Maze
from config import *
from block import Block, BlockState
from enum import Enum
import Algorithms

class AppState(Enum):
    MAZE_NOT_LOADED = 0
    MAZE_LOADED = 1
    TRAVERSING = 2
    FINISHED = 3
class Algorithm_Choice(Enum):
    NONE = 0
    A_STAR = 1
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

def create_maze(file):
    return Maze()

def render_maze(maze: Maze, speed_factor: float):
    maze.draw()
    app_state = AppState.MAZE_LOADED
    draw_speed = len(maze.maze_array) * len(maze.maze_array[0]) * .15
    pygame.display.flip()

    return app_state, draw_speed

def create_buttons(screen):
    '''
    Creates buttons in bulk, can add new buttons, just make sure to add it to return statement
    '''

    button_width = WINDOW_SIZE * 0.2
    button_height = WINDOW_SIZE * 0.06
    button_spacing = WINDOW_SIZE * 0.02

    # Values to properly center Buttons:

    # these align the buttons in line with the maze:
    BUTTONS_X = MAZE_PADDING_LEFT + MAZE_SIZE + 40
    BUTTONS_Y = MAZE_PADDING_TOP

    # ===Buttons inside of the Maze Window===#
    upload_button = Button(
        screen = screen,
        bg_color = pygame.Color(LIGHT_SKY_BLUE),
        text_color = pygame.Color(WHITE),
        font_size = NUM_FONT,
        rect = pygame.Rect(BUTTONS_X, 
                           BUTTONS_Y,
                           button_width, 
                           button_height),
        text = "Upload Maze")
    
    preload_button = Button(
        screen = screen,
        bg_color = pygame.Color(LIGHT_SKY_BLUE),
        text_color = pygame.Color(WHITE),
        font_size = NUM_FONT,
        rect = pygame.Rect(BUTTONS_X, 
                           BUTTONS_Y + button_height + button_spacing, # spacing the buttons vertically
                           button_width, 
                           button_height),
        text = "Use Pre-made")
    
    print_path_button = Button(
        screen = screen,
        bg_color = pygame.Color(LIGHT_SKY_BLUE),
        text_color = pygame.Color(WHITE),
        font_size = NUM_FONT,
        rect = pygame.Rect(BUTTONS_X, 
                           BUTTONS_Y + 2 * (button_height + button_spacing), # spacing the buttons vertically
                           button_width, 
                           button_height),
        text = "Show path taken")
    
    #===Buttons outside of the Maze Window===#
    # unloads maze to show load options again
    unload_button = Button(
        screen = screen,
        bg_color = pygame.Color(RED),
        text_color = pygame.Color(WHITE),
        font_size = NUM_FONT,
        rect = pygame.Rect(BUTTONS_X, 
                           BUTTONS_Y + 3 * (button_height + button_spacing),
                           button_width, 
                           button_height),
        text = "Unload Maze")
    
    a_star_button = Button(
        screen = screen,
        bg_color = pygame.Color(RED),
        text_color = pygame.Color(WHITE),
        font_size = NUM_FONT,
        rect = pygame.Rect(BUTTONS_X, 
                           BUTTONS_Y + 5 * (button_height + button_spacing),
                           button_width, 
                           button_height),
        text = "A*")
    
    dijkstras_star_button = Button(
        screen = screen,
        bg_color = pygame.Color(RED),
        text_color = pygame.Color(WHITE),
        font_size = NUM_FONT,
        rect = pygame.Rect(BUTTONS_X, 
                           BUTTONS_Y + 6 * (button_height + button_spacing),
                           button_width, 
                           button_height),
        text = "Dijkstra's")

    return upload_button, preload_button, print_path_button, unload_button, a_star_button, dijkstras_star_button

def visualize_algorithm(maze_grid: list[list[Block]], explored_inds: list[tuple[int, int]], path_inds: list[tuple[int, int]]):
    for row, col in explored_inds:
        block = maze_grid[row][col]
        block.set_state(BlockState.EXPLORED)
        block.draw()
        yield True
    
    for row, col in path_inds:
        block = maze_grid[row][col]
        block.set_state(BlockState.FINAL)
        block.draw()
        yield True

    yield False

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
    algorithm = Algorithm_Choice.A_STAR

    '''
    Setup GUI elements. Rendering new objects will be event-based, not per-frame
    '''

    screen.fill(WHITE)

    upload_button, preload_button, print_path_button, unload_button, a_star_button, dijkstras_button = create_buttons(screen)
    # Storing in arrays makes it cleaner to print all visuals for that state
    # trying to work with buttons that show at all times - Andres
    all_buttons = [upload_button, preload_button, print_path_button, unload_button, a_star_button, dijkstras_button]

    [button.draw() for button in all_buttons]

    pygame.display.flip()

    # Maze drawing variables
    is_maze_drawing = False
    maze_drawer = None # Generator for drawing
    draw_speed = 60 # Default tick rate

    # Loading maze thread and result
    t_load_maze = None
    t_load_maze_result = []

    while running:
        if t_load_maze and len(t_load_maze_result) > 0:
            print("GOT IT")
            maze = t_load_maze_result[0]
            app_state, draw_speed = render_maze(maze=maze, speed_factor=.15)
            
            #cleanup
            t_load_maze = None
            t_load_maze_result.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Handle button interactions if clicked and enabled
                if upload_button.is_clicked((x, y)):
                    upload_button.clicked()

                    maze_file = prompt_file()
                    if maze_file:
                        t_load_maze = Thread(target=Maze, args=(maze_file, screen, t_load_maze_result))
                        t_load_maze.start()

                elif preload_button.is_clicked((x, y)):
                    preload_button.clicked()

                    maze_file = open("PreMade_Mazes/10x10_Maze1.csv", "r")
                    t_load_maze = Thread(target=Maze, args=(maze_file, screen, t_load_maze_result))
                    t_load_maze.start()
                        

                elif unload_button.is_clicked((x, y)):
                    unload_button.clicked()
                    if maze:
                        maze.clear()

                    app_state = AppState.MAZE_NOT_LOADED
                    is_maze_drawing = False
                
                elif print_path_button.is_clicked((x,y)) and algorithm != Algorithm_Choice.NONE:
                    print_path_button.clicked()

                    if algorithm == Algorithm_Choice.A_STAR:
                        blocks_explored, final_path = Algorithms.a_star(maze_grid=maze.maze_array, start=maze.start_coord, end=maze.end_coord)
                        maze_drawer = visualize_algorithm(maze_grid=maze.maze_array, explored_inds=blocks_explored, path_inds=final_path)
                        is_maze_drawing = True
                    elif algorithm == Algorithm_Choice.DIJKSTRAS:
                        print("Testing")
                        maze.create_graph()
                        maze.graph_points.print_list()

                elif a_star_button.is_clicked((x,y)) and algorithm != Algorithm_Choice.A_STAR:
                    a_star_button.clicked()
                    algorithm = Algorithm_Choice.A_STAR
                
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
        dijkstras_button.set_enabled(algorithm == Algorithm_Choice.A_STAR)
        a_star_button.set_enabled(algorithm == Algorithm_Choice.DIJKSTRAS)
        # we can add more buttons and enable/disabled them whenever

        # == Drawing ==
        if is_maze_drawing:
            is_maze_drawing = next(maze_drawer)

        # Draw all buttons regardless of state
        for button in all_buttons: 
            button.draw()
        
        pygame.display.flip()

        clock.tick(draw_speed) # tick rate = drawing speed

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
