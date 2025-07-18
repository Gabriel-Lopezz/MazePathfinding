import pygame
from pygame.font import Font

class Button:

    def __init__(self, screen: pygame.surface, color: pygame.Color, rect: pygame.Rect, text: str = ""):
        self.screen = screen
        self.color = color
        self.rect = rect
        
        self.text = text
        self.font = Font(None, 36)
        self.text_surface = self.font.render("TEST", True, (0,0,0), None)
        self.text_rect = self.text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
    
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        
        self.screen.blit(self.text_surface, self.text_rect)