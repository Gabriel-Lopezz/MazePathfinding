import pygame
from pygame.font import Font
from config import *

class Text:
    def __init__(self, screen: pygame.Surface, text_color: pygame.Color, 
                 font_size: int, rect: pygame.Rect, text: str = ""):
        self.screen = screen
        self.text_color = text_color
        self.rect = rect
        self.text = text

        # Render text with default Font
        self.font = Font(None, font_size)
        self.text_surface = self.font.render(text, True, text_color) # Render onto a surface
        self.text_rect = self.text_surface.get_rect(center=self.rect.center) # Center the text

    def draw(self):
        '''
        Draw text onto rect screen using defined rect
        '''
        self.screen.blit(self.text_surface, self.text_rect)

    def clear(self):
        '''
        Draws a white rect over the text
        '''
        pygame.draw.rect(self.screen, WHITE, self.rect)

class Button:

    def __init__(self, screen: pygame.surface, bg_color: pygame.Color, text_color: pygame.Color,
                 font_size: int, rect: pygame.Rect, text: str = ""):
        self.screen = screen
        self.bg_color = bg_color #background color
        self.text_color = text_color
        self.rect = rect
        self.text = text

        # Render text with default Font
        self.font = Font(None, font_size)
        self.text_surface = self.font.render(text, True, text_color, None) # Render onto a surface
        self.text_rect = self.text_surface.get_rect(center=(self.rect.centerx, self.rect.centery)) # Center the text

        self.enabled = True
        self.disabled_bg_color = pygame.Color('gray60')
    
    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def is_enabled(self):
        return self.enabled

    def draw(self):
        if self.enabled:
            color = self.bg_color
        else:
            color = self.disabled_bg_color

        pygame.draw.rect(self.screen, color, self.rect)
        self.screen.blit(self.text_surface, self.text_rect)

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

    button_width = BUTTON_WIDTH
    button_height = BUTTON_HEIGHT
    button_spacing = BUTTON_WIDTH * 0.1

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
    
    print_finished_path_button = Button (
        screen = screen,
        bg_color = pygame.Color(LIGHT_SKY_BLUE),
        text_color = pygame.Color(WHITE),
        font_size = NUM_FONT,
        rect = pygame.Rect(BUTTONS_X,
                           BUTTONS_Y + 3 * (button_height + button_spacing),
                           button_width,
                           button_height),
        text = "Finish Immediately"

    )
    
    #===Buttons outside of the Maze Window===#
    # unloads maze to show load options again
    unload_button = Button(
        screen = screen,
        bg_color = pygame.Color(RED),
        text_color = pygame.Color(WHITE),
        font_size = NUM_FONT,
        rect = pygame.Rect(BUTTONS_X, 
                           BUTTONS_Y + 4 * (button_height + button_spacing),
                           button_width, 
                           button_height),
        text = "Unload Maze")
    
    a_star_button = Button(
        screen = screen,
        bg_color = pygame.Color(RED),
        text_color = pygame.Color(WHITE),
        font_size = NUM_FONT,
        rect = pygame.Rect(BUTTONS_X, 
                           BUTTONS_Y + 6 * (button_height + button_spacing),
                           button_width, 
                           button_height),
        text = "A*")
    
    dijkstras_star_button = Button(
        screen = screen,
        bg_color = pygame.Color(RED),
        text_color = pygame.Color(WHITE),
        font_size = NUM_FONT,
        rect = pygame.Rect(BUTTONS_X, 
                           BUTTONS_Y + 7 * (button_height + button_spacing),
                           button_width, 
                           button_height),
        text = "Dijkstra's")

    return upload_button, preload_button, print_path_button, print_finished_path_button, unload_button, a_star_button, dijkstras_star_button

def create_error_message(screen: pygame.Surface, error_message:str = ""):
    ERROR_X = MAZE_PADDING_LEFT + MAZE_SIZE + 125
    ERROR_Y = MAZE_PADDING_TOP + 750

    error_txt = Text(
        screen = screen,
        text_color = RED,
        font_size = NUM_FONT - 10, # Smaller than usual for space
        rect = pygame.Rect( ERROR_X,
                           ERROR_Y,
                           BUTTON_WIDTH,
                           BUTTON_HEIGHT),
        text = error_message
    )

    return error_txt