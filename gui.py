import pygame
from pygame.font import Font
from constants import *

class Text:
    def __init__(self, screen: pygame.Surface, text_color: pygame.Color, font_size: int,
                 rect: pygame.Rect, text: str = "", bg_color=(WHITE), 
                 font_path=None, center_text=True):
        self.screen = screen
        self.text_color = text_color
        self.rect = rect
        self.text = text
        self.bg_color = bg_color

        if font_path:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.Font(None, font_size)

        self.center_text = center_text

        self.text_surface = self.font.render(text, True, text_color) # Render onto a surface

        if center_text:
            # storing the center
            self.text_center = self.rect.center
        else:
            self.text_center = None

    def wrap_text(self):
        """Split self.text into multiple lines that fit in self.rect width."""
        words = self.text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if self.font.size(test_line)[0] <= self.rect.width - 10:  # small padding
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def draw(self):
        """Draw the text (wrapped) inside the rect."""
        # Draw background and border
        pygame.draw.rect(self.screen, pygame.Color("gray20"), self.rect)
        pygame.draw.rect(self.screen, pygame.Color("gray20"), self.rect, 2)

        # Render wrapped lines
        lines = self.wrap_text()
        line_height = self.font.get_linesize()

        total_height = len(lines) * line_height
        y_offset = self.rect.y + ((self.rect.height - (line_height * len(lines))) // 2 if self.center_text else 5)

        for line in lines:
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect()
            text_rect.x = self.rect.x + 5
            text_rect.y = y_offset
            self.screen.blit(text_surface, text_rect)
            y_offset += line_height

    def clear(self):
        pygame.draw.rect(self.screen, self.bg_color, self.rect)

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
        ("A*", RED, 10),
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
    ERROR_X = MAZE_PADDING_LEFT + MAZE_SIZE + 20
    ERROR_Y = ERROR_PADDING_TOP

    error_rect = pygame.Rect(
        ERROR_X,
        ERROR_Y,
        ERROR_WIDTH,
        ERROR_HEIGHT
    )

    error_txt = Text(
        screen = screen,
        text_color = RED,
        font_path="fot-yuruka-std.ttf",
        font_size = NUM_FONT - 5, # Smaller than usual for space
        rect = error_rect,
        bg_color=pygame.Color(WHITE),

        text = error_message
    )

    return error_txt

def create_results(screen: pygame.Surface):
    labels = ["Algorithm", "Execution Time", "Blocks Traversed", "Final Path Distance"]
    results = []

    # Panel origin
    panel_x = MAZE_PADDING_LEFT + MAZE_SIZE
    panel_y = RESULTS_PADDING_TOP

    # Container styling
    container_margin_x = 20
    container_margin_y = 10
    container_width = BUTTON_WIDTH + 200
    container_height = (BUTTON_HEIGHT + RESULT_GAP) * len(labels) + 30 # magic number to correctly pad the height

    container_rect = pygame.Rect(
        panel_x + container_margin_x,
        panel_y - container_margin_y,
        container_width,
        container_height
    )

    pygame.draw.rect(screen, pygame.Color("gray20"), container_rect)

    for i, label in enumerate(labels):
        y_offset = panel_y + i * (BUTTON_HEIGHT + RESULT_GAP)

        label_rect = pygame.Rect(
            panel_x + 40,
            y_offset,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )

        result_rect = pygame.Rect(
            panel_x + BUTTON_WIDTH + 60,
            y_offset,
            BUTTON_WIDTH - 40,
            BUTTON_HEIGHT
        )

        label_text = Text(
            screen=screen,
            text_color=RED,
            font_path="fot-yuruka-std.ttf",
            font_size=NUM_FONT - 3,
            rect=label_rect,
            text=f"{label}:",
            center_text=False
        )
        label_text.draw()

        result_text = Text(
            screen=screen,
            text_color=RED,
            font_path="fot-yuruka-std.ttf",
            font_size=NUM_FONT - 5,
            rect=result_rect,
            text="",
            bg_color=pygame.Color("gray20"),
            center_text=False,
        )

        results.append(result_text)

    return results
