import pygame
import os
from pygame.font import Font
from constants import *

class Text:
    def __init__(self, screen: pygame.Surface, text_color: pygame.Color, font_size: int, 
                 rect: pygame.Rect, text: str = "", font_path=None, center_text = True):
        self.screen = screen
        self.text_color = text_color
        self.rect = rect
        self.text = text

        if font_path:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = Font(None, font_size)

        self.text_surface = self.font.render(text, True, text_color) # Render onto a surface

        if center_text:
            self.rect = self.text_surface.get_rect(center=self.rect.center) # Center the text

    def draw(self):
        '''
        Draw text onto rect screen using defined rect
        '''
        self.text_surface = self.font.render(self.text, True, self.text_color) # Render onto a surface
        self.screen.blit(self.text_surface, self.rect)

    def clear(self):
        '''
        Draws a white rect over the text
        '''
        pygame.draw.rect(self.screen, WHITE, self.rect)

class Button:

    def __init__(self, screen: pygame.surface, bg_color: pygame.Color, text_color: pygame.Color,
                 font_size: int, rect: pygame.Rect, text: str = "", font_path=None):
        self.screen = screen
        self.bg_color = bg_color #background color
        self.text_color = text_color
        self.rect = rect
        self.text = text

        if font_path:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = Font(None, font_size)

        self.text_surface = self.font.render(text, True, text_color, None) # Render onto a surface
        self.text_rect = self.text_surface.get_rect(center=(self.rect.centerx, self.rect.centery)) # Center the text

        self.enabled = True
        self.disabled_bg_color = bg_color - pygame.Color(80, 80, 80)

    def draw(self):
        if self.enabled:
            color = self.bg_color
        else:
            color = self.disabled_bg_color

        pygame.draw.rect(self.screen, color, self.rect)
        self.screen.blit(self.text_surface, self.text_rect)
    
    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def is_enabled(self):
        return self.enabled

    '''Makes the button color lighter for a bit, simulating a button being clicked'''
    def clicked(self):
        if not self.enabled:
            return
        
        dimmed_color = tuple(max(c-50,0) for c in self.bg_color)
        pygame.draw.rect(self.screen, dimmed_color, self.rect)
        self.screen.blit(self.text_surface, self.text_rect)
        pygame.display.flip()
        
        pygame.time.delay(100)

        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        self.screen.blit(self.text_surface, self.text_rect)

        pygame.display.flip()

    def is_clicked(self, pos):
        return self.enabled and self.rect.collidepoint(pos)
    

# Method originally from main, here to reduce clutter.

def create_buttons(screen):
    '''
    Creates buttons in bulk, can add new buttons, just make sure to add it to return statement
    '''

    # === Load custom font ===
    font_path = "fot-yuruka-std.ttf"

    # Position to the right of the maze
    panel_x = MAZE_PADDING_LEFT + MAZE_SIZE + 40
    button_width = BUTTON_WIDTH
    button_height = BUTTON_HEIGHT

    # List of buttons: (button title, background color, extra space after button)
    button_list = [
        ("Upload Maze", LIGHT_SKY_BLUE, 10),
        ("Use Pre-made", LIGHT_SKY_BLUE, 40),
        ("Draw Traversal", LIGHT_SKY_BLUE, 10),
        ("Show solution", LIGHT_SKY_BLUE, 10),
        ("Unload Maze", RED, 30),
        ("GBFS", RED, 10),
        ("Dijkstra's", RED, 0),
    ]

    # Calculate total height to center them vertically
    total_height = 0
    for item in button_list:
        label, color, gap_after = item
        total_height += button_height + gap_after
    total_height -= button_list[-1][2]  # removing last gap just in case

    # Start Y so the whole group is centered
    panel_y = (RES_HEIGHT - total_height) // 2 - 200

    # Buttons panel styling
    container_padding_x = 20
    container_padding_y = 20
    container_width = button_width + container_padding_x * 2
    container_height = total_height + container_padding_y * 2

    container_rect = pygame.Rect(
        panel_x - container_padding_x,
        panel_y - container_padding_y,
        container_width,
        container_height
    )

    pygame.draw.rect(screen, pygame.Color("gray20"), container_rect)  # filled

    # Create all buttons
    buttons = []
    current_y = panel_y
    for item in button_list:
        button_title, color, gap_after = item
        # Create the Button object with custom font path
        new_button = Button(
            screen=screen,
            bg_color=pygame.Color(color),
            text_color=pygame.Color(WHITE),
            font_size=NUM_FONT,
            rect=pygame.Rect(panel_x, current_y, button_width, button_height),
            text=button_title,
            font_path=font_path   # <-- Added custom font
        )
        buttons.append(new_button)

        # Move down for the next button
        current_y += button_height + gap_after

    return tuple(buttons)

def create_error_message(screen: pygame.Surface, error_message:str = ""):
    ERROR_X = MAZE_PADDING_LEFT + MAZE_SIZE + 125
    ERROR_Y = MAZE_PADDING_TOP + 750

    error_txt = Text(
        screen = screen,
        text_color = RED,
        font_path="fot-yuruka-std.ttf",
        font_size = NUM_FONT - 5, # Smaller than usual for space
        rect = pygame.Rect( ERROR_X,
                           ERROR_Y,
                           BUTTON_WIDTH,
                           BUTTON_HEIGHT),
        text = error_message
    )

    return error_txt

def create_results(screen: pygame.Surface):
    labels = ["Algorithm", "Execution Time", "Blocks Traversed", "Final Path Length"]

    results = []

    for i, label in enumerate(labels):
        label_txt = Text(
            screen = screen,
            text_color = RED,
            font_path="fot-yuruka-std.ttf",
            font_size = NUM_FONT - 3, # Smaller than usual for space
            rect = pygame.Rect(MAZE_PADDING_LEFT + MAZE_SIZE + 40,
                            RESULTS_TOP + (BUTTON_HEIGHT * i),
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT),
            text = label + ": ",
            center_text = False
        )

        label_txt.draw()

        result_txt = Text(
            screen = screen,
            text_color = RED,
            font_path="fot-yuruka-std.ttf",
            font_size = NUM_FONT - 5, # Smaller than usual for space
            rect = pygame.Rect(MAZE_PADDING_LEFT + MAZE_SIZE + BUTTON_WIDTH + 45,
                            RESULTS_TOP + (BUTTON_HEIGHT * i),
                            BUTTON_WIDTH,
                            BUTTON_HEIGHT),
            text = "",
            center_text = False
        )

        results.append(result_txt)

    return results