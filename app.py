import pygame
import tkinter
from tkinter import filedialog
import sys
from button import Button
from maze import Maze
from constants import *
from block import Block, BlockState

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

def main():
    pygame.init()

    screen = pygame.display.set_mode(size=(WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Maze Pathfinding")

    clock = pygame.time.Clock()

    running = True

    # Maze object and maze window border (as kwargs for draw function)
    maze = None
    window_border = [
        { "surface": screen, "color": BLACK, "start_pos": (MAZE_SIZE, 0), "end_pos": (MAZE_SIZE, MAZE_SIZE + 2), "width": 5 },
        { "surface": screen, "color": BLACK, "start_pos": (0, MAZE_SIZE), "end_pos": (MAZE_SIZE + 2, MAZE_SIZE), "width": 5 }
    ]

    upload_button = Button(screen, pygame.Color(LIGHT_SKY_BLUE),pygame.Color(WHITE), pygame.Rect(150, 160, 175, 50), "Upload Maze")
    preload_button = Button(screen, pygame.Color(LIGHT_SKY_BLUE),pygame.Color(WHITE), pygame.Rect(150, 240, 175, 50), "Use Pre-made")

    '''
    Setup GUI elements. Rendering new objects will be event-based, not per-frame
    '''

    screen.fill((255, 255, 255)) # Background
    # Main Menu Section:
    upload_button.draw() # maze load button
    preload_button.draw() # pre-made maze load button
    [pygame.draw.line(**line) for line in window_border]
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if upload_button.rect.collidepoint(event.pos):
                    maze_file = prompt_file()
                    if maze_file and not maze: 
                        maze = Maze(maze_file=maze_file, screen=screen)
                        render_maze(maze=maze, border=window_border)
                if preload_button.rect.collidepoint(event.pos):
                    with open("PreMade_Mazes/10x10_Maze1.csv", "r") as maze_file:
                        if maze_file and not maze:
                            maze = Maze(maze_file=maze_file, screen=screen)
                            render_maze(maze=maze, border=window_border)

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
