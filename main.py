
from board import *
import json


def print_grid(grid):
    """Prints a grid"""
    for i in grid:
        for j in i:
            print(j, end = " ")
        print()

def main():
    make_grid(5)

def make_grid(grid_size):
    # Create a grid of character objects

    grid = [[Character(letter=" ", color="Default", button = "na", has_text = True, color_change = True) for j in range(grid_size)] for i in range(grid_size)]
    # beginning cells
    #indexes are flipped idk why
    grid [0][0]._letter = "N"
    grid [0][0]._has_text = False # text can't be changed
    grid [0][0]._color = "Red"
    grid[0][0]._color_change = False

    grid[3][0]._letter = "A"
    grid [3][0]._has_text = False
    grid [3][0]._color = "Yellow"
    grid[3][0]._color_change = False


    grid[4][0]._letter = "P"
    grid[4][0]._has_text = False
    grid[4][0]._color = "Orange"
    grid[4][0]._color_change = False


    grid[2][3]._letter = "A"
    grid [2][3]._has_text = False
    grid [2][3]._color = "Pink"
    grid[2][3]._color_change = False

    #end cells
    grid [2][4]._color = "Red"
    grid[2][4]._color_change = False

    grid [1][3]._color = "Yellow"
    grid[1][3]._color_change = False

    grid [4][2]._color = "Orange"
    grid[4][2]._color_change = False

    grid [3][4]._color = "Pink"
    grid[3][4]._color_change = False
    
    # Serialize the grid to JSON
    serialized_grid = [[{"letter": char._letter, "color": char._color, "button": char._button, "has_text": char._has_text, "color_change" :char._color_change} for char in row] for row in grid]
    levels = []
    levels.append(serialized_grid)
    # Write JSON data to a file
    
    with open("grid.json", "w") as json_file:
        json.dump(levels, json_file, indent=5) 

main()
