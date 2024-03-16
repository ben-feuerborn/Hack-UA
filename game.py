
import pygame
from button import *
from board import *
import json
import sys


class Game: 
    def __init__(self): 
        
        # Initialize the game, and create game resources
        pygame.init()
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

        self.characters = []

        for i in range(5):
            row = []
            for j in range(5):
                character_image = pygame.image.load("images/Default Key.png").convert_alpha()
                character_button = Button(500 + (i*80),150 + (j*80),character_image,0.4,self)
                character = Character("",  "white", character_button)
                row.append(character)
            self.characters.append(row)

        #creating buttons for color selection
        self.colors = ["Dark Blue", "Green", "Light Blue", "Medium Blue", "Orange", "Pink", "Red", "Yellow", "Default"]
        self.color_buttons = []
        self.colors_index = [False, False, False, False, False, False, False, False, False]
        for color in range(len(self.colors)):
            image = pygame.image.load("Images/buttons/"+self.colors[color]+" Button.png").convert_alpha()
            button  = Button(100,80+(color*80),image,0.2,self)
            self.color_buttons.append(button)

    def run_game(self):
        # Start the main loop for the game
        while True:
            # call a method to check to see if any keyboard events have occurred
            self.screen.fill(self.bg_color)
            self._check_events()

            if self.game_paused:
                self._paused()
            else:
                for row in self.characters: # draw the characters on the screen
                    for character in row:
                        self.character_update(character)
                for button_index in range(len(self.color_buttons)):
                    if self.color_buttons[button_index].draw(): #see which button color is selected and set all others to False
                        self.colors_index = [False, False, False, False, False, False, False, False, False]
                        self.colors_index[button_index] = not self.colors_index[button_index]

            pygame.display.flip()

    def character_update(self,character):
        """update the character object on the screen
        drawing its button and checking if it is being clicked, 
        and if so changing the color appropriately"""
        if character.getButton().draw(): 
            for color in range(len(self.colors_index)):
                if self.colors_index[color]: 
                    new_image = pygame.image.load("Images/"+self.colors[color]+" Key.png").convert_alpha() #opens up new image of correct color
                    character.change_button_color(new_image, self.colors[color]) # updates the buttons color

    def _paused(self):
        """Draw the pause screen menu and give 3 different options to the user
        to continue, quit, or start a new game"""
        self.screen.fill(self.bg_color)
        if self.continue_button.draw():
            self.game_paused = False
        if self.quit_button.draw():
            sys.exit()
        if self.new_game_button.draw(): #FIXME needs to START A NEW GAME
            self.game_paused = False


    def _check_keydown_events(self, event):
        # Is the key the right arrow or is it the left arrow
        if event.key == pygame.K_m:
            if self.game_paused:
                self.game_paused = False
            else:
                self.game_paused = True

    def _check_keyup_events(self, event):
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

    def menu(self): #FIXME needs to be created
        pass



x = Game()
x.run_game()

