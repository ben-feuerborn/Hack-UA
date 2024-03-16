from button import *

class Character: 
    """Class with attributes letter, row, column"""
    def __init__(self, letter = "", color = "white",button = "na"):
        #d is a button object
        self._letter = letter
        self._color = color
        self.button = button

    def change_button_color(self,image, color):
        self.button.change_image(image)
        self._color = color
    
    def getButton(self):
        return self.button
    
    def GetLetter(self):
        """returns the letter"""
        return self._letter
    
    def SetLetter(self, letter):
        """sets the letter"""
        self._letter = letter

    def GetColor(self):
        """returns the color"""
        return self._color
    
    def SetColor(self, color):
        """sets the color"""
        self._color = color
    
    def __str__(self):
        return self._letter

class Board: 
    """Class with attributes size, board and category, wordNum"""
    def __init__(self, size = 0, board = [], category = "n/a", wordNum = 0):
        self._size = size
        self._board = board
        self._category = category
        self._wordNum = wordNum
    
    def GetBoard(self):
        """returns the board"""
        return self._board
    
    def GetCategory(self):
        """returns the category"""
        return self._category
    
    def GetWordNum(self):
        """returns the word number"""
        return self._wordNum
    
    def GetSize(self):
        """returns the size"""
        return self._size
    
    def SetBoard(self, board):
        """sets the board"""
        self._board = board

    def SetCategory(self, category):
        """sets the category"""
        self._category = category
    
    def SetWordNum(self, wordNum):
        """sets the word number"""
        self._wordNum = wordNum

    def SetSize(self, size):
        """sets the size"""
        self._size = size

    
