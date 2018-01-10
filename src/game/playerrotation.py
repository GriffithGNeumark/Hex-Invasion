"""
   ..module: playerrotation
    :synopsis: Contains a data structure that acts as a circular doubly
    linked list. The nodes in the list give the players in the game. We
    can query the list for the next player in the game.
"""

import os, sys
from . import player

map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.pardir)
if map_path not in sys.path:
    sys.path.append( map_path )

import map.cell as cell

"""
Nodes of the linked list. Contain references to the current player in the game.
"""
class __rotationnode__(object):

    def __init__(self, player_ref):
        """
        Class constructor. Requires user to pass a reference to a Player
        object as input.
        """
        self.changePlayer(player_ref)
        # Create the links of the node, forwards and backwards
        self.__next__ = None
        self.__prev__ = None

    def changePlayer(self, player_ref):
        """Change the player that is being used by this node"""
        if type(player_ref) is not player.Player:
            raise TypeError("The type of the input passed to a new __rotationnode__ " +
                            "object must be of type Player.")
        else:
            self.__player__ = player_ref

    def getPlayer(self):
        """Get a reference to the Player object that is stored at this node."""
        return self.__player__

    def connectForward(self, node):
        """Change the node that this node links to in the forward direction."""
        if type(node) not in (__rotationnode__, None):
            raise TypeError("__rotationnode__ must be connected to another __rotationnode__ " +
                            "or to None.")
        else:
            self.__next__ = node

    def connectBackward(self, node):
        """Change the node that this node links to in the backward direction."""
        if type(node) not in (__rotationnode__, None):
            raise TypeError("__rotationnode__ must be connected to another __rotationnode__ " +
                            "or to None.")
        else:
            self.__previous__ = node

    def getNext(self):
        """Get the node that is in front of this node."""
        return self.__next__

    def getPrevious(self):
        """Get the node that is behind this node."""
        return self.__previous__


"""
Class that rotates between players. This is a doubly-linked list where the final node
is always connected to the first node.
"""
class Rotator(object):

    def __init__(self):
        """Creates the rotator. Initializes the linked list to have no nodes."""
        self.__currentnode__ = None
        self.__colordict__   = {}

    def appendPlayer(self, new_player):
        """Adds a node containing a player to the end of the list."""
        if type(new_player) is not player.Player:
            raise TypeError("Can only append objects of type Player.")
        # Insert the player with the input color into __colordict__
        color = new_player.getColor()
        if color in self.__colordict__:
            raise IndexError("The color of the appended player (" + cell.getColorString(color) +
                             ") is already in the Rotator.")
        newnode = __rotationnode__(new_player)
        self.__colordict__[color] = newnode
        # Link the node
        if self.__currentnode__ is None:
            self.__currentnode__ = newnode
            newnode.connectForward(newnode)
            newnode.connectBackward(newnode)
            self.__initial_color__ = new_player.getColor()
        else:
            former_prevnode = self.__currentnode__.getPrevious()
            newnode.connectForward(self.__currentnode__)
            newnode.connectBackward(former_prevnode)
            self.__currentnode__.connectBackward(newnode)
            former_prevnode.connectForward(newnode)

    def removePlayer(self, color):
        """Remove the player of a given color from the list"""
        if type(color) not in (player.Player, int):
            raise TypeError("Input to removePlayer must be of type int or Player.")
        if type(color) is player.Player:
            color = color.getColor()
        if color not in self.__colordict__:
            raise IndexError("The input color/player was not found in the Rotator.")
        # Empty the Rotator if this is the last node
        if len(self.__colordict__.keys()) <= 1:
            self.__colordict__   = {}
            self.__currentnode__ = None
            return
        if self.__currentnode__.getPlayer().getColor() == color:
            self.__currentnode__ = self.__currentnode__.getNext()
        node_to_remove = self.__colordict__[color]
        # Connect the previous node to the next node
        previous_node = node_to_remove.getPrevious()
        next_node     = node_to_remove.getNext()
        previous_node.connectForward(next_node)
        next_node.connectBackward(previous_node)
        self.__colordict__.pop(color, None)

    def insertPlayer(self, player_to_insert, index):
        """
        Inserts a player at a given index of the linked list. Index based on the current
        node in the rotator.
        """
        if type(player_to_insert) is not player.Player:
            raise TypeError("The first input to insertPlayer must be of type Player.")
        elif player_to_insert.getColor() in self.__colordict__:
            raise ValueError("The player to insert has color " + 
                             cell.getColorString(player_to_insert.getColor()) + "; Rotator already " +
                             "contains a player of this color.")
        elif type(index) is not int:
            raise TypeError("The second input to insertPlayer must be of type int.")
        elif index < 0 or index > len(self.__colordict__.keys()):
            raise ValueError("The index to insertPlayer was less than 0 or greater than " +
                             "the number of players currently in the Rotator.")
        # Append the node if the current length of the list is 0
        if self.getNumPlayers() == 0:
            self.appendPlayer(player_to_insert)
        else:
            node_i = self.__currentnode__
            for i in range(index):
                node_i = node_i.getNext()
            # Link the node
            new_node = __rotationnode__(player_to_insert)
            previous_node = node_i.getPrevious()
            node_i.connectBackward(new_node)
            new_node.connectForward(node_i)
            previous_node.connectForward(new_node)
            new_node.connectBackward(previous_node)
            # Add the player to the dictionary
            self.__colordict__[player_to_insert.getColor()] = new_node
            # Set the initial color if index == 0
            if index == 0:
                self.__initial_color__ = player_to_insert.getColor()
                self.__currentnode__   = new_node

    def getCurrentPlayer(self):
        """Return a reference to the current player."""
        if self.__currentnode__ is None:
            return None
        else:
            return self.__currentnode__.getPlayer()

    def getPlayer(self, index):
        """Gets the ith player in the rotation."""
        if type(index) is not int:
            raise TypeError("The index passed to getPlayer must be of type int.")
        elif index < 0 or index >= len(self.__colordict__.keys()):
            raise IndexError("Index less than 0 or greater than or equal to the number of " +
                             "players in the game.")
        node_i = self.__currentnode__
        for i in range(index):
            node_i = node_i.getNext()
        return node_i.getPlayer()

    def getCurrentColor(self):
        """Return the color of the current player."""
        if self.__currentnode__ is None:
            return None
        else:
            return self.__currentnode__.getPlayer().getColor()

    def rotate(self):
        """
        Sets the current node to be the next node in the rotator; returns a reference
        to the next player in the game.
        """
        self.__currentnode__ = self.__currentnode__.getNext()
        return self.__currentnode__.getPlayer()

    def rotateBack(self):
        """Rotates the circular list backwards."""
        self.__currentnode__ = self.__currentnode__.getPrevious()
        return self.__currentnode__.getPlayer()

    def getNumPlayers(self):
        """Get the number of players that are currently in the game."""
        return len(self.__colordict__.keys())

    def hasColor(self, color):
        """Determines whether or not the rotation contains the input color."""
        if type(color) is not int:
            raise TypeError( "Color must be of type int." )
        else:
            return color in self.__colordict__

    def reset(self):
        """Returns to the initial player."""
        while self.getCurrentColor() != self.__initial_color__:
            self.rotate()
    
    def getInitialPlayer(self):
        """Get the initial player in the rotation."""
        return self.__colordict__[self.__initial_color__]

    def getInitialColor(self):
        """Get the color of the initial player in the rotation."""
        return self.__initial_color__
