
from board import *
import json

"""
def print_grid(grid):
    ""Prints a grid""
    for i in grid:
        for j in i:
            print(j, end = " ")
        print()

def main():
    pass

def make_grid(gird_size):
    # Create a grid of character objects
    grid = [[Character(letter="a", row=i, column=j, color="red") for j in range(grid_size)] for i in range(grid_size)]

    # Serialize the grid to JSON
    serialized_grid = [[{"letter": char._letter, "row": char._row, "column": char._column, "color": char._color} for char in row] for row in grid]

    # Write JSON data to a file
    with open("grid.json", "w") as json_file:
        json.dump(serialized_grid, json_file, indent=4) 


main()
"""

import pygame
import sys

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

class Button:
    def __init__(self, x, y, width, height, text="", text_color=BLACK, button_color=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.font = pygame.font.Font(None, 36)
        self._render_text()

    def _render_text(self):
        self.rendered_text = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.rendered_text.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.button_color, self.rect)
        screen.blit(self.rendered_text, self.text_rect)

    def set_text(self, text):
        self.text = text
        self._render_text()

def main():
    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Button with Changeable Text")

    # Create a button
    button = Button(150, 100, 100, 50, "Click Me")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.rect.collidepoint(event.pos):
                    # Change the text of the button when clicked
                    button.set_text("Clicked!")

        screen.fill(WHITE)
        button.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
