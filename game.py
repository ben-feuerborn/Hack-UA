"""Authors: Giuseppe Pongelupe Giacoia
Date: 03/17/2024
Summary: This game.py file works with the button.py and board.py files and game level desriptions in "answers.json" and "grid.json" 
to create a game where the user can select colors and letters to fill in a cell in a given grid. 
The goal to win the game is to complete the given built in levels by connecting two given cells of a certain color by a continuous path of cells of the same color, 
the path can be horizontal, vertical, and bent, but each cell only has at most 4 other adjacent cells (up, down, right and left), meaning that the path can't go diagonally. 
Once a path is made with colors, users have to also spell out a word of the given category given the starting letter and end position."""

import pygame
from button import *
from board import *
import sys
import json
import time


class Game: 

    def __init__(self): 
        pygame.init() # initializes pygame

        # Setting up 
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Word-Flow")
                
        # attributes to be used if game is paused / in order to pause the game
        self.game_paused = False
        # loading in images and initializing button objects for the paused menu
        pause_button_image = pygame.image.load("images/Menu/Pause Button Solid.png").convert_alpha()
        self.pause_button = Button(self.screen_width-70, 50, pause_button_image,0.6,self)  
        info_image = pygame.image.load("images/Menu/Info Solid.png").convert_alpha() 
        quit_image = pygame.image.load("images/Menu/Quit Solid.png").convert_alpha()
        new_game_image = pygame.image.load("images/Menu/New Game Solid.png").convert_alpha()
        self.new_game_button = Button(self.screen_width/2,self.screen_height/4, new_game_image,1,self) 
        self.info_button = Button(self.screen_width/2,(self.screen_height/4)*2,info_image,1,self)
        self.quit_button = Button(self.screen_width/2,(self.screen_height/4)*3,quit_image,1,self)

        # attributes and buttons used for the main and info menus 
        self.main_menu = True
        self.info_menu2 = False # second page of the menu
        self.info_menu = False 
        new_game_image = pygame.image.load("images/Menu/New Game Solid.png").convert_alpha() 
        self.main_new_button = Button(self.screen_width/2,self.screen_height/5 *2, new_game_image,1,self)
        self.main_info_button = Button(self.screen_width/2,(self.screen_height/5)*3,info_image,1,self)
        self.main_quit_button = Button(self.screen_width/2,(self.screen_height/5)*4,quit_image,1,self)
        self.title_image = pygame.image.load("images/Menu/Word-Flow Logo.png").convert_alpha()
        exit_image = pygame.image.load("images/Menu/Exit Button.png").convert_alpha() 
        self.exit_button = Button(self.screen_width-70, 50,exit_image, 0.6, self)
        next_image = pygame.image.load("images/Menu/Next Button.png").convert_alpha() 
        self.next_button = Button(self.screen_width-150, 50,next_image, 0.6, self)
        
        # info menu pages loaded and scaled for the given window size
        self.info_menu_page1 = pygame.image.load("images/Menu/Info Page 1.png").convert_alpha()
        self.info_menu_page2 = pygame.image.load("images/Menu/Info Page 2.png").convert_alpha()
        width = self.info_menu_page1.get_width()
        height = self.info_menu_page1.get_height()
        scale = 0.359
        self.info_menu_page1 = pygame.transform.scale(self.info_menu_page1,(int(width*scale),int(height*scale)))
        self.info_menu_page2 = pygame.transform.scale(self.info_menu_page2,(int(width*scale),int(height*scale)))

        # creating the base font for the "character" objects (AKA each cell) 
        self.base_font = pygame.font.Font(None, 32)

        # load in level information and answers
        self.current_level = 0
        self.levels = []
        json_file = "grid.json"
        self.load_levels(json_file,self.levels) # levels are stored in Board objects and all in a linear list 

        # loading answers from a local json file. 
        self.answers = []
        json_answer = "answers.json"
        self.load_levels(json_answer,self.answers) # answers are 2d lists stored in corresponding indexes in self.answers to self.levels

        # self.characters represents the current level being played 
        self.characters = self.levels[self.current_level].GetBoard()

        # Initializing buttons for color selection 
        self.colors = ["Dark Blue", "Green", "Light Blue", "Medium Blue", "Orange", "Pink", "Red", "Yellow", "Default"] # list of all the colors available
        self.color_buttons = [] 
        self.colors_index = [False, False, False, False, False, False, False, False, False] #status of each button (if a specific color of a corresponding index is currently selected)
        for color in range(len(self.colors)):
            image = pygame.image.load("Images/buttons/"+self.colors[color]+" Button.png").convert_alpha()
            button  = Button(100,80+(color*80),image,0.2,self)
            self.color_buttons.append(button)

        # initializes "check" button that players will use in order to check if their work is correct
        self.check = False
        check_image = pygame.image.load("images/Menu/Check Solid.png").convert_alpha()
        self.check_button =  Button(1000,650, check_image, 0.625, self)

        # show answers button in case the player is lost
        show_answers_image = pygame.image.load("images/Menu/Show Answers Button.png").convert_alpha()
        self.show_answers_button =  Button(1000,730, show_answers_image, 0.625, self)
        self.checked = False # if player chose to show answers, the player can no longer go into "writting" mode

        # used to see if user did all levels
        self.last_level = len(self.levels)



    def load_levels(self, json_file,lst):
        """Loads the levels from a json file and creates characters and buttons to represent a grid appropriately. 
        It then stores them in a board object and appends it to the self.levels list.
        Alternatively if lst is self.answers then it stores the answers for a given level in 
        the list"""
        with open(json_file, "r") as file: 
            data = json.load(file)
        i = 0 # i and j are used to know the spacing between cells in a grid
        j = 0

        # below are calculations to find where the center of the grid should be
        grid_cell_width = 212* 0.4
        grid_cell_height = 215* 0.4
        grid_padding = 2 #space between cells
        grid_size = len(data[0])
        grid_width = grid_size * grid_cell_width + (grid_size + 1) * grid_padding 
        grid_height = grid_size * grid_cell_height + (grid_size + 1) * grid_padding

        # Calculate the position to center the grid
        grid_y = ((self.screen_width - grid_width) // 2) * 1.3
        grid_x = ((self.screen_height - grid_height) // 2) - 20

        for grid in data:  #iterating per "level"
            character_grid = []
            i=0
            for row in grid: # iterating per column (as per the structure of the json file)
                character_row = []
                j=0
                for item in row: #iterating per object in a given column 
                    character_image = pygame.image.load("images/"+item['color']+" Key.png").convert_alpha() # starts a cell in the given color
                    image_y = (grid_x + (j * (grid_cell_width + grid_padding)) + grid_padding ) - 160
                    image_x = (grid_y + (i * (grid_cell_height + grid_padding)) + grid_padding) -40 # location of the button in the grid
                    character_button = Button(image_x,image_y,character_image,0.4,self)
                    character = Character(item['letter'], item['color'], character_button, item['has_text'], item['color_change'])
                    character_row.append(character)
                    j+=1
                character_grid.append(character_row)
                i+=1
            temp = Board(character_grid) # creates one board object per level
            lst.append(temp) 
        categories =  ["Warm Up (In At)", "Actions", "Shapes", "Colors", "Sports", "Onomatopoeia","Streaming Services" ,\
                    "Animals", "Companies", "Food", "Disney Characters" ]
        for board in range(len(lst)): 
            lst[board].SetCategory(categories[board])
            

    def run_game(self):
        """Main loop for the game. it will keep running until the game is done
        There are 5 main types of events, game is being paused (pulls up paused menu), 
        game just started or newgame button was clicked, checking answers with check button, 
         main event for game  being played, and Info screen shown. """
        
        while True:
            self.screen.fill(self.bg_color) # fill in background
            self._check_events() #checks for special keyboard events

            if self.current_level == self.last_level: # if player won the game
                font = pygame.font.Font("slkscr.ttf", 50)
                text_surface = font.render("You won!", True, (0,0,0))
                self.screen.blit(text_surface, ((self.screen_width-150)/2 - 50,(self.screen_height-50)/2))
                pygame.display.flip()
            elif self.info_menu2: # if the second page of the menu should be up
                self._info_menu2()
            elif self.info_menu: #if the info menu should be up
                self._info_menu()
            elif self.main_menu: # if main menu should be pulled up
                self._main_menu()
            elif self.game_paused: # if the paused menu should be pulled up
                self._paused()
            elif self.check:  # if the player requested to check his answers
                self._is_checked()
            else: # main event, where game is running a level
                self.draw_categories() # draw the category on the screen
                self.draw_color_buttons() # draw the color buttons on the screen

                for row in range(len(self.characters)): # draw the characters/cells on the screen
                    for character in range(len(self.characters[row])):
                        self.character_update(row,character)
                        self.draw_character_text(self.characters[row][character])
                if self.check_button.draw(): # checks if player pressed paused or check buttons
                    self.check = True
                if self.pause_button.draw(): # if game is paused
                    self.pause_button.change_image(pygame.image.load("images/Menu/Exit Button.png").convert_alpha()) # change the image of the pause button to a resume button

                    self.game_paused = True
                if self.show_answers_button.draw(): # checks if user wants to show the answers
                    self.characters = self.answers[self.current_level].GetBoard()
                    self.checked = True
            pygame.display.flip() # flip the image to show updates

    def _is_checked(self):
        """if the checked button is presed it either erases wrong entries
        or lets player move on to next round"""
        if self.check_answers(): # answer is right, moving on to next level
            self.current_level +=1
            self.checked = False # reset the checked status
            if self.current_level != self.last_level: #if game is not over
                self.characters = self.levels[self.current_level].GetBoard()[:]
                self.screen.fill(self.bg_color)     
                font = pygame.font.Font("slkscr.ttf", 50)
                text_surface = font.render(f"Moving on to Level {self.current_level+1}", True, (0,0,0)) # dislpay intermediate message 
                width, height = text_surface.get_rect().size
                self.screen.blit(text_surface, (((self.screen_width-width)/2),(self.screen_height/2)-40))
                pygame.display.flip() 
                time.sleep(1)
        self.check = False 

    # Below are all the different menu related functions 
    def _info_menu(self):
        """Displays the info menu of the game which has two pages, 
        each accessed with the next and back bottom in the bottom of the page
        the info button is exited once the exit button is clicked"""        
        self.screen.blit(self.info_menu_page1, (0,0))
        if self.exit_button.draw(): 
            self.info_menu = False
        elif self.next_button.draw():
            self.next_button.change_image(pygame.image.load("images/Menu/Back Button.png").convert_alpha()) # change the image of the pause button to a resume button
            self.info_menu2 = True  


    def _info_menu2(self):
        """Shows second page in the info menu"""
        self.screen.blit(self.info_menu_page2, (0,0))
        if self.next_button.draw(): 
            self.next_button.change_image(pygame.image.load("images/Menu/Next Button.png").convert_alpha()) # change the image of the pause button to a resume button
            self.info_menu2 = False
        elif self.exit_button.draw(): 
            self.info_menu = False
            self.info_menu2 = False
    
    def _main_menu(self): 
        """Displays the main starting menu of the game, with options to pull up instructions
        start a new game or quit"""
        image_width, image_height = self.title_image.get_rect().size 
        self.screen.blit(self.title_image, ((self.screen_width-image_width)/2, (self.screen_height-image_height)/14)) # draw logo on the screen
        if self.main_new_button.draw():  # check if new game button was selected
            self.main_menu = False
        elif self.main_info_button.draw():  # check if info button was selected to pull up the info page
            self.info_menu = True
        elif self.main_quit_button.draw():  #check if quit button was selected 
            sys.exit()
    
    def _paused(self):
        """Draw the pause screen menu and give 3 different options to the user
        to continue, quit, or start a new game"""
        if self.info_button.draw():
            self.info_menu = True
            self.game_paused = False
        elif self.quit_button.draw():
            sys.exit()
        elif self.new_game_button.draw():  # pulls up the main menu again for players to restart the game
            self.game_paused = False
            self.current_level = 0 # reset the game to level 0
            self.levels = [] # reset the levels
            self.load_levels("grid.json",self.levels)
            self.characters = self.levels[self.current_level].GetBoard()
            self.main_menu = True
        elif self.pause_button.draw(): 
            self.pause_button.change_image(pygame.image.load("images/Menu/Pause Button Solid.png").convert_alpha()) # change the image of the pause button to a resume button
            self.game_paused = False
        

    def check_answers(self): 
        """Checks to see if answers are correct, if they are returns true, if not 
        returns false and changes the color back to default and resets the character letter
        returns True if the answer is correct"""
        x = True
        for i in range(len(self.characters)):
            for j in range(len(self.characters[i])):
                if self.characters[i][j] != self.answers[self.current_level].GetBoard()[i][j]:
                    x = False
                    self.characters[i][j].SetLetter(" ")
                    if self.characters[i][j].get_color_change(): # checks if the mistaken cell is an end cell
                        new_image = pygame.image.load("Images/Default Key.png").convert_alpha() 
                        self.characters[i][j].change_button_color(new_image, "Default") # updates the buttons color
        return x
    

    def character_update(self,i, j):
        """update the character object on the screen
        drawing its button and checking if it is being clicked, 
        and if so changing the color appropriately
        
        once selected places the user in "writing mode" where they can enter
        text input for a given cell/character"""

        if self.characters[i][j].get_button().draw(): # drawing button and seeing if it is selected
            if not self.checked: # if player didn't check the answers
                self.update_character_color(i,j)                
                # checks if the button pressed has a modifiable character (isn't a given start or end, and isn't one of the color select buttons)
                if self.characters[i][j].get_has_text(): 
                    running = True
                    text = self.characters[i][j].get_letter()
                    while running: # player stuck in "writing mode" until he enters "enter" to select new character or selects a cell
                        self.screen.fill(self.bg_color)
                        self.draw_categories() # draw category in the screen
    
                        # draw up the color buttons as well so they dont get covered also kicks player out of writting mode if selected
                        running = not self.draw_color_buttons()

                        # redraw up the grid so it doesn't get covered
                        for indexi in range(len(self.characters)): 
                            for indexj in range(len(self.characters[indexi])):
                                if self.characters[indexi][indexj].get_button().draw():
                                    i=indexi
                                    j=indexj
                                    self.update_character_color(i,j)
                                    text = self.characters[i][j].get_letter()
                                self.draw_character_text(self.characters[indexi][indexj]) # draw each characters text

                        for event in pygame.event.get(): # get user input text  
                            if event.type == pygame.QUIT:
                                sys.exit()
                            # handle text input
                            if event.type == pygame.TEXTINPUT:
                                text = event.text
                            # handle special keys
                            if event.type == pygame.KEYDOWN: 
                                if event.key == pygame.K_RETURN:
                                    running = False
                                elif event.key == pygame.K_BACKSPACE:
                                    text = ""
                        self.characters[i][j].SetLetter(text) # updates the character for the given cell

                        pygame.display.flip()

    def draw_color_buttons(self):
        """draws the button indexes and checks if they were selected, if so it changes the color of the cell accordingly
        returns true if one was pressed, false if not"""
        x = False
        for button_index in range(len(self.color_buttons)): # draws color buttons
            if self.color_buttons[button_index].draw(): # checks which button was last pressed
                self.colors_index = [False, False, False, False, False, False, False, False, False]
                self.colors_index[button_index] = not self.colors_index[button_index]
                x = True
        return x
                        
    def draw_categories(self): 
        """displays the correct category,  according to whatever level it is, on the screen"""
        font = pygame.font.Font("slkscr.ttf", 40)
        text_surface = font.render(f"Category:", True, (0,0,0))
        text_surface2 = font.render(f"{self.levels[self.current_level].GetCategory()}", True, (0,0,0))
        self.screen.blit(text_surface, (200, 600))
        self.screen.blit(text_surface2, (200, 650))


    def update_character_color(self,i,j):
        """function takes in two integers representing the row and column indexes of the character
        in the self.characters grid. It then changes its color appropriately"""
        if self.characters[i][j].get_color_change(): # Checks if the character can have its color changed
            for color in range(len(self.colors_index)): 
                if self.colors_index[color]: 
                    self.characters[i][j].SetColor(self.colors_index[color]) # changes the color attribute once cell changes color
                    new_image = pygame.image.load("Images/"+self.colors[color]+" Key.png").convert_alpha() 
                    self.characters[i][j].change_button_color(new_image, self.colors[color]) # updates the buttons color with a new image


    def draw_character_text(self, character):
        """Given a character it draws on the screen its text attribute over its image"""
        text_surface = self.base_font.render(character.get_letter(), True, (0,0,0))
        self.screen.blit(text_surface, (character.get_button().rect.x + 35, character.get_button().rect.y +32))


    def _check_keydown_events(self, event):
        """Checks if user pressed special key m which pulls up the paused menu"""
        if event.key == pygame.K_m:
            if self.game_paused:
                self.game_paused = False
            else:
                self.game_paused = True
        
    def _check_events(self):
        """Checks for special events such as closing the tab and keydown events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)



x = Game() # Creates a game instance
x.run_game() # Start the game

