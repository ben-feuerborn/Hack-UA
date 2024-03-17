import pygame
import sys
from pygame.locals import *


# Initialize Pygame
pygame.init()

# Create a font object
font = pygame.font.Font(None, 24)

class TextButton():
    def __init__(self, x, y, width, height):        
        self.rect = pygame.Rect(x, y, width, height)
        self.text_surface = font.render("", True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))


    def draw(self, surface):
        # Draw the button rectangle
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(surface, (245, 245, 245), self.rect)
        else:
            pygame.draw.rect(surface, (0, 0, 0), self.rect)
            pygame.draw.rect(surface, (255, 255, 255), self.rect.inflate(-2, -2))
            pygame.draw.rect(surface, (0, 0, 0), self.rect.inflate(-2, -2), 2)


        # Draw the button text
        surface.blit(self.text_surface, self.text_rect)


    def handle_click(self, text_input):
        entered_text = text_input(self.text_rect.centerx - 4, self.text_rect.centery - 8, (0, 0, 0))
        print("Button clicked, character entered! Entered text:", entered_text)
        self.text_surface = font.render(entered_text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
        
    def text_input(self,x, y, color):
        character = ""
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        character = character[:-1]
                    elif event.key == K_RETURN:
                        return character  # Return the entered text when Enter is pressed
                    else:
                        if character == '':
                            character = event.unicode


                    # Only clear the area where the text input is displayed
                    self.screen.fill((245, 245, 245), (x, y, 25, 25)) # change the color of the background of the text input before enter


                    text_surface = font.render(f"{character}", True, color)
                    self.screen.blit(text_surface, (x, y))
                    pygame.display.update()