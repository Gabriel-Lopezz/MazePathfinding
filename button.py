import pygame
from pygame.font import Font

class Button:

    def __init__(self, screen: pygame.surface, bg_color: pygame.Color, text_color: pygame.Color, font_size: int, rect: pygame.Rect, text: str = ""):
        self.screen = screen
        self.bg_color = bg_color #background color
        self.text_color = text_color
        self.rect = rect
        self.text = text
        self.font = Font(None, font_size)
        self.text_surface = self.font.render(text, True, text_color, None)
        self.text_rect = self.text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
    
    def draw(self):
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        
        self.screen.blit(self.text_surface, self.text_rect)
    '''Makes the button color lighter for a bit, simulating a button being clicked'''
    def clicked(self):
        dimmed_color = tuple(max(c-50,0) for c in self.bg_color)
        pygame.draw.rect(self.screen, dimmed_color, self.rect)
        self.screen.blit(self.text_surface, self.text_rect)
        pygame.time.delay(100)
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        self.screen.blit(self.text_surface, self.text_rect)