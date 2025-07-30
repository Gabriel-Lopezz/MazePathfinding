import pygame
import tkinter
from tkinter import filedialog
import sys
from button import Button
from maze import Maze
from config import *
from block import Block, BlockState
from enum import Enum

class AppState(Enum):
    MAZE_NOT_LOADED = 0
    MAZE_LOADED = 1
    TRAVERSING = 2
    FINISHED = 3
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

def render_maze(maze: Maze, border: list[dict]):
    [pygame.draw.line(**line) for line in border]
    maze.draw()
    pygame.display.flip()
'''
    Creates buttons in bulk, can add new buttons, just make sure to add it to return statement
'''
def create_buttons(screen):

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
    
    #===Buttons outside of the Maze Window===#
    # unloads maze to show load options again
    unload_button = Button(
        screen = screen,
        bg_color = pygame.Color(RED),
        text_color = pygame.Color(WHITE),
        font_size = NUM_FONT,
        rect = pygame.Rect(BUTTONS_X, 
                           BUTTONS_Y + 3 * button_height + button_spacing,
                           button_width, 
                           button_height),
        text = "Unload Maze")


    return upload_button,preload_button,unload_button

def main():
    pygame.init()

    screen = pygame.display.set_mode((RES_WIDTH,RES_HEIGHT))
    pygame.display.set_caption("Maze Pathfinding")

    clock = pygame.time.Clock()

    running = True

    # Maze object, maze state and maze window border (as kwargs for draw function)
    maze = None
    app_state = AppState.MAZE_NOT_LOADED

    # window_border = [
    #     { "surface": screen, "color": BLACK, "start_pos": (MAZE_SIZE, 0), "end_pos": (MAZE_SIZE, MAZE_SIZE + 2), "width": 5 },
    #     { "surface": screen, "color": BLACK, "start_pos": (0, MAZE_SIZE), "end_pos": (MAZE_SIZE + 2, MAZE_SIZE), "width": 5 }
    # ]
    # re-doing UI so commenting out this part for now - Andres

    upload_button, preload_button, unload_button = create_buttons(screen)
    # Storing in arrays makes it cleaner to print all visuals for that state
    # trying to work with buttons that show at all times - Andres
    all_buttons = [upload_button, preload_button, unload_button]

    '''
    Setup GUI elements. Rendering new objects will be event-based, not per-frame
    '''

    # screen.fill(WHITE) # Background
    # # Main Menu Section:
    # for button in all_buttons:
    #     button.draw() #  pre-made maze load & user-input maze load button

    # # [pygame.draw.line(**line) for line in window_border]

    # pygame.display.flip()

    # I commented this out because it doesn't seem necessary but don't wanna delete it - Andres

    while running:
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
                        maze = Maze(maze_file=maze_file, screen=screen)
                        # screen.fill(WHITE)
                        maze.draw()
                        app_state = AppState.MAZE_LOADED

                elif preload_button.is_clicked((x, y)):
                    preload_button.clicked()
                    with open("PreMade_Mazes/10x10_Maze1.csv", "r") as maze_file:
                        maze = Maze(maze_file=maze_file, screen=screen)
                        # screen.fill(WHITE)
                        maze.draw()
                        app_state = AppState.MAZE_LOADED

                elif unload_button.is_clicked((x, y)):
                    unload_button.clicked()
                    if maze:
                        maze.clear()
                    # screen.fill(WHITE)
                    app_state = AppState.MAZE_NOT_LOADED

                # Maze interaction: box clicks
                elif maze and MAZE_PADDING_LEFT <= x <= MAZE_PADDING_LEFT + MAZE_SIZE and MAZE_PADDING_TOP <= y <= MAZE_PADDING_TOP + MAZE_SIZE:
                    maze.click_box(x, y, event.button)

        # enabling/disabling buttons based on state
        upload_button.set_enabled(app_state == AppState.MAZE_NOT_LOADED)
        preload_button.set_enabled(app_state == AppState.MAZE_NOT_LOADED)
        unload_button.set_enabled(app_state in (AppState.MAZE_LOADED, AppState.FINISHED))
        # we can add more buttons and enable/disabled them whenever

        # == Drawing ==

        screen.fill(WHITE)

        # Draw all buttons regardless of state
        for button in all_buttons: 
            button.draw()
        # if this for loop for the buttons is out after 
        # the maze.draw() the buttons start flickering - Andres

        # without the "and" statement here the "unload" button crashes due to some interaction with the maze.clear() method - Andres
        if maze and maze.maze_array is not None:
            maze.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
