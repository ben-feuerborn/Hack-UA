
import pygame
from button import *
from board import *
import sys
import json


class Game: 
    def __init__(self): 
        
        # Initialize the game, and create game resources
        pygame.init()
        self.base_font = pygame.font.Font(None, 32)

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        # self.screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        #TITLE
        pygame.display.set_caption("Flow Game")
                
        #if game is paused
        self.game_paused = False
        continue_image = pygame.image.load("images/continue.png").convert_alpha()
        quit_image = pygame.image.load("images/quit.png").convert_alpha()
        new_game_image = pygame.image.load("images/newGame.png").convert_alpha()
        self.continue_button = Button(self.screen_width/2,self.screen_height/4, continue_image,1,self)
        self.new_game_button = Button(self.screen_width/2,(self.screen_height/4)*2,new_game_image,1,self)
        self.quit_button = Button(self.screen_width/2,(self.screen_height/4)*3,quit_image,1,self)

        # creating the board

        self.current_level = 0 # keeps track of which level is curren _________________________________change this with new game
        self.levels = []
        json_file = "grid.json"
        self.load_levels(json_file)
        
        #self.characters will always be the current level 
        self.characters = self.levels[0].GetBoard()

        #creating buttons for color selection
        self.colors = ["Dark Blue", "Green", "Light Blue", "Medium Blue", "Orange", "Pink", "Red", "Yellow", "Default"]
        self.color_buttons = []
        self.colors_index = [False, False, False, False, False, False, False, False, False]
        for color in range(len(self.colors)):
            image = pygame.image.load("Images/buttons/"+self.colors[color]+" Button.png").convert_alpha()
            button  = Button(100,80+(color*80),image,0.2,self)
            self.color_buttons.append(button)

    def load_levels(self, json_file):
        with open(json_file, "r") as file: 
            data = json.load(file)
        i = 0
        j = 0
        for grid in data:
            character_grid = []
            for row in grid:
                character_row = []
                j=0
                for item in row:
                    character_image = pygame.image.load("images/"+item['color']+" Key.png").convert_alpha()
                    character_button = Button(500 + (i*80),150 + (j*80),character_image,0.4,self)
                    character = Character(item['letter'], item['color'], character_button, item['has_text'], item['color_change'])
                    print(item['color_change'])
                    character_row.append(character)
                    j+=1
                character_grid.append(character_row)
                i+=1
            temp = Board(character_grid)
            self.levels.append(temp)

    def run_game(self):
        # Start the main loop for the game
        while True:
            # call a method to check to see if any keyboard events have occurred
            self.screen.fill(self.bg_color)
            self._check_events()

            if self.game_paused:
                self._paused()
            else:
                for row in range(len(self.characters)): # draw the characters on the screen
                    for character in range(len(self.characters[row])):
                        self.character_update(row,character)
                        self.draw_character_text(self.characters[row][character])
                for button_index in range(len(self.color_buttons)):
                    if self.color_buttons[button_index].draw(): #see which button color is selected and set all others to False
                        self.colors_index = [False, False, False, False, False, False, False, False, False]
                        self.colors_index[button_index] = not self.colors_index[button_index]

            pygame.display.flip()
    

    def character_update(self,i, j):
        """update the character object on the screen
        drawing its button and checking if it is being clicked, 
        and if so changing the color appropriately"""
        # i and j are 
        if self.characters[i][j].getButton().draw(): # drawing button and seeing if it is selected
            print("Hi")
            if self.characters[i][j].get_color_change(): # if button can have its color changed
                for color in range(len(self.colors_index)): 
                    if self.colors_index[color]: 
                        self.characters[i][j].SetColor(self.colors_index[color]) #changes the color attribute once cell changes color
                        new_image = pygame.image.load("Images/"+self.colors[color]+" Key.png").convert_alpha() #opens up new image of correct color
                        self.characters[i][j].change_button_color(new_image, self.colors[color]) # updates the buttons color
        
            if self.characters[i][j].get_has_text(): # checks if the button pressed has a modifiable character (isn't a given start or end, and isn't one of the color select buttons)
                text = self.characters[i][j].GetLetter()
                running = True
                while running: #player stuck in loop until he enters "enter" to select new character
                    self.screen.fill(self.bg_color)
                    # still needs to check if game is paused
                    if self.game_paused: # NEEDS TESTING _____________________________________________________________________________________________________________
                        self._paused()
                    else:
                        #draw up the grid so it doesn't get covered
                        for row in self.characters: 
                            for x in row:
                                x.getButton().draw()
                                self.draw_character_text(x)
                    
                        #draw up teh color buttons as well so they dont get covered
                        for button_index in range(len(self.color_buttons)): #WE CAN MAYBE CHANGE THIS TO IF ANOTHER COLOR IS SELECTED IT BREAKS OUT OF THIS LOOP
                            self.color_buttons[button_index].draw() 
                            
                        for event in pygame.event.get(): #get user input text 
                            #check if menu or if game ends PROBLEM: MENU CAN"T BE SELECTED WITH M SO NEEDS AN ICON BUTTON___________________________________________
                            if event.type == pygame.QUIT:
                                sys.exit()
                            #handle text input
                            if event.type == pygame.TEXTINPUT:
                                text = event.text
                            #handle special keys
                            if event.type == pygame.KEYDOWN: 
                                if event.key == pygame.K_RETURN:
                                    print(text)  # Print the input text
                                    running = False
                                elif event.key == pygame.K_BACKSPACE:
                                    text = ""
                        self.characters[i][j].SetLetter(text)
                    pygame.display.flip()


    def draw_character_text(self, character):
        text_surface = self.base_font.render(character.GetLetter(), True, (0,0,0))
        self.screen.blit(text_surface, (character.getButton().rect.x + 35, character.getButton().rect.y +32))


    def _paused(self):
        """Draw the pause screen menu and give 3 different options to the user
        to continue, quit, or start a new game"""
        self.screen.fill(self.bg_color)
        if self.continue_button.draw():
            self.game_paused = False
        if self.quit_button.draw():
            sys.exit()
        if self.new_game_button.draw(): #FIXME needs to START A NEW GAME ___________________________________________________________
            self.game_paused = False


    def _check_keydown_events(self, event):
        # Is the key the right arrow or is it the left arrow
        if event.key == pygame.K_m:
            if self.game_paused:
                self.game_paused = False
            else:
                self.game_paused = True

    def _check_keyup_events(self, event):# FIXME ___________________________________________________________ is this needed? 
        # Did the player stop holding down the arrow keys?
        pass

        
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Did the player press the right or left arrow key?
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # Did the player stop holding down the arrow key?
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def menu(self): #FIXME needs to be created__________________________________________________
        pass



x = Game()
x.run_game()

