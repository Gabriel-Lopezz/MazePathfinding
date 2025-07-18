import pygame
import tkinter
from tkinter import filedialog
import sys
from button import Button

def prompt_file():
    tk_widget = tkinter.Tk()
    tk_widget.withdraw() # Makes the Tkinter window invisible

    # Open's the OS dialog box for file selection
    file_info = filedialog.askopenfile(title="Select CSV to Load", filetypes=[("CSV File", "*.csv")])

    if (file_info and file_info.name[-4:] != ".csv"): # Need to validate that file was indeed CSV
        file_info = None

    tk_widget.destroy() # Delete widget after user is done selecting

    return file_info


def main():
    pygame.init()

    screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Maze Pathfinding")

    clock = pygame.time.Clock()

    running = True

    load_button = Button(screen, pygame.Color(200, 200, 200), pygame.Rect(200, 200, 100, 50), "Test Text")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if load_button.rect.collidepoint(event.pos):
                    prompt_file()

        

        screen.fill((255, 255, 255))
        load_button.draw()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
