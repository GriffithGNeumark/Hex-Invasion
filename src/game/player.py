"""
Class and corresponding methods for a player.
"""

import os, sys

cell_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.pardir,"map")
if cell_path not in sys.path:
    sys.path.append( cell_path )

import cell

"""
PLAYER CLASS
"""
class Player(object):

    """
    Constructor for the player object. Sets the player's color and resources.
    """
    def __init__(self, color, resources=0):
        if not cell.validColor(color):
            raise Exception( "The input color is invalid." )
        elif type(resources) is not int or resources < 0:
            raise Exception( "Resources must be a non-negative integer." )
        else:
            self.__color__ = color
            self.__resources__ = resources
        # We store the units that the player has in a set
        self.__units__ = set()

    """
    Accessor for the resources data field.
    """
    def getResources(self):
        return self.__resources__

    """
    Accessor for the units data field.
    """
    def getUnits(self):
        return self.__units__

    """
    Give the player an additional unit.
    """
    def addUnit(self, pos):
        self.__units__.add(pos)

    """
    Remove one of the player's units
    """
    def removeUnit(self, pos):
        self.__units__.add(pos)

    """
    Accessor for the color data field.
    """
    def getColor(self):
        return self.__color__

    """
    Adjust the number of resources that this player has. The resources field
    can only take on an integral value.
    """
    def changeResources(self, change):
        if type(change) is not int:
            raise TypeError( "Change in resources must be an integer." )
        initial_value = self.__resources__
        self.__resources__ += change
        if self.__resources__ < 0:
            self.__resources__ = initial_value
            raise ValueError( "Player has a negative amount of resources " +
                              "after this operation." )

    """
    Set the number of resources that this player has to zero.
    """
    def resetResources(self):
        self.__resources__ = 0

    """
    Takes a copy of a map and returns the move that the player will make.
    This method must be implemented in classes that inherit from Player.
    """
    def makeMove(self,game_map):
        pass
