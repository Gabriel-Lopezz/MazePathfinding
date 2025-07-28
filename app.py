import pygame
import tkinter
from tkinter import filedialog
import sys
from button import Button
from maze import Maze
from constants import *
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
    # Values to properly center Buttons
    maze_window_center = MAZE_SIZE // 2 - button_width // 2

    # ===Buttons inside of the Maze Window===#
    upload_button = Button(
        screen = screen,
        bg_color = pygame.Color(LIGHT_SKY_BLUE),
        text_color = pygame.Color(WHITE),
        font_size = NUM_FONT,
        rect = pygame.Rect(maze_window_center, MAZE_SIZE*0.2, button_width, button_height),
        text = "Upload Maze")
    preload_button = Button(
        screen = screen,
        bg_color = pygame.Color(LIGHT_SKY_BLUE),
        text_color = pygame.Color(WHITE),
        font_size = NUM_FONT,
        rect = pygame.Rect(maze_window_center, (MAZE_SIZE*0.2) + button_height + button_spacing, button_width, button_height),
        text = "Use Pre-made")
    #===Buttons outside of the Maze Window===#
    # unloads maze to show load options again
    unload_button = Button(
        screen = screen,
        bg_color = pygame.Color(RED),
        text_color = pygame.Color(WHITE),
        font_size = NUM_FONT,
        rect = pygame.Rect(MAZE_SIZE, MAZE_SIZE, button_width, button_height),
        text = "Unload Maze")


    return upload_button,preload_button,unload_button
def main():
    pygame.init()

    screen = pygame.display.set_mode(size=(WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Maze Pathfinding")

    clock = pygame.time.Clock()

    running = True

    # Maze object, maze state and maze window border (as kwargs for draw function)
    maze = None
    app_state = AppState.MAZE_NOT_LOADED

    window_border = [
        { "surface": screen, "color": BLACK, "start_pos": (MAZE_SIZE, 0), "end_pos": (MAZE_SIZE, MAZE_SIZE + 2), "width": 5 },
        { "surface": screen, "color": BLACK, "start_pos": (0, MAZE_SIZE), "end_pos": (MAZE_SIZE + 2, MAZE_SIZE), "width": 5 }
    ]

    upload_button, preload_button, unload_button = create_buttons(screen)
    '''
    Setup GUI elements. Rendering new objects will be event-based, not per-frame
    '''

    screen.fill((255, 255, 255)) # Background
    # Main Menu Section:
    upload_button.draw() # maze load button
    preload_button.draw() # pre-made maze load button
    unload_button.draw()
    [pygame.draw.line(**line) for line in window_border]
    pygame.display.flip()

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if app_state == AppState.MAZE_NOT_LOADED:
                    # Initial state of the program, load buttons are in maze area
                    if upload_button.rect.collidepoint(event.pos):
                        maze_file = prompt_file()
                        if maze_file:
                            maze = Maze(maze_file=maze_file, screen=screen)
                            render_maze(maze=maze, border=window_border)
                            app_state = AppState.MAZE_LOADED

                    elif preload_button.rect.collidepoint(event.pos):
                        with open("PreMade_Mazes/10x10_Maze1.csv", "r") as maze_file:
                            if maze_file:
                                maze = Maze(maze_file=maze_file, screen=screen)
                                render_maze(maze=maze, border=window_border)
                                app_state = AppState.MAZE_LOADED
                
                elif app_state == AppState.MAZE_LOADED:
                    if unload_button.rect.collidepoint(event.pos):
                        maze.clear()
                        [pygame.draw.line(**line) for line in window_border]
                        pygame.display.flip()

                elif app_state == AppState.MAZE_LOADED:
                    continue
                
                elif app_state == AppState.FINISHED:
                    if preload_button.rect.collidepoint(event.pos):
                        maze = None
                        app_state = AppState.MAZE_NOT_LOADED

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
