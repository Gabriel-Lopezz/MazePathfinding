import pygame, sys
class Maze:
    def __init__(self, input_maze, width, height, screen):
        """
        :param input_maze: a string representation of the maze 
        :param width:
        :param height:
        :param screen:
        screen is a window from PyGame.
        creates a maze from a string input space, which should be separated by \n
        """
        self.maze = [list(row) for row in input_maze.strip().split('\n')]
        self.width = width
        self.height = height
        self.screen = screen
    def print_maze(self):
        for row in self.maze:
            print(row)
