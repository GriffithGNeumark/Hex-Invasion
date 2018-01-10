"""
   .. module: game
      :synopsis: Game module. Contains the Game class, which allows us to control 
      the game and manipulate the map. This is the primary class from which the
      game state is changed and from which we can access the current map.
"""

import os, sys
import copy

from . import movevector
from . import player
from . import playerrotation as rotator

map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.pardir)
if map_path not in sys.path:
    sys.path.append( map_path )

import map
import map.cell as cell

# Default amount of resources required to generate a new unit
NEW_UNIT_COST = 5

# Default strength of a new unit
DEFAULT_NEW_UNIT_STRENGTH = 1

class Game(object):

    def __init__(self, map, rotation=(cell.RED,cell.GREEN,cell.BLUE,cell.YELLOW)):
        """
        Constructor for a new instance of the game class. Stores the player rotation in
        a class 
        """
        if type(rotation) not in (list,tuple):
            raise TypeError("Rotation should be of type tuple or list.")
        # Add new players of all the colors in the rotation to the game.
        self.__rotator__ = rotator.Rotator()
        for color in rotation:
            if not cell.validPlayerColor(color):
                raise ValueError( "Color (id: " + str(color) + ") is not a valid color." )
            elif self.__rotator__.hasColor(color):
                raise ValueError( "Color " + cell.getColorString(color) +
                                  " appears twice in rotation." )
            else:
                new_player = player.Player(color)
                self.__rotator__.appendPlayer(new_player)
        if map is None:
            self.map = None
        else:
            self.map = map
        self.__moved__ = set()
        self.__current_player__ = self.__rotator__.getCurrentPlayer()
        self.__stored_moves__   = []
        self.__default_map__    = copy.deepcopy(map)

    def getCurrentPlayer(self):
        """Returns the player whose turn it currently is."""
        return self.__rotator__.getCurrentPlayer()

    def getStoredMoves(self):
        """Returns a list of the stored moves."""
        return self.__stored_moves__[:]

    def clearStoredMoves(self):
        """Clears out the stored moves."""
        self.__stored_moves__ = []

    def resetGame(self):
        """Resets the game."""
        self.map = self.__default_map__
        self.__moved__ = set()
        self.__rotator__.reset()
        self.__current_player__ = self.__rotator__.getCurrentPlayer()

    def getCurrentColor(self):
        """Returns the color of the player whose turn it currently is."""
        return self.__rotator__.getCurrentColor()

    def getPlayer(self, i):
        """Returns a reference to the ith player in the game."""
        return self.__rotator__.getPlayer(i)

    def getNumPlayers(self):
        """Gets the number of players currently in the game."""
        return self.__rotator__.getNumPlayers()

    def hasMoved(self, position):
        """
        Takes (x,y) coordinates and returns whether or not the player has moved the unit
        at that position yet.
        """
        return position in self.__moved__

    def gameOver(self):
        """
        Determines whether or not the game has ended.
        """
        return self.__rotator__.getNumPlayers() <= 1

    def moveUnit(self,from_position,to_position):
        """
        Allows the user to move a unit on the board.
        """
        # Perform error checking
        if type(from_position) not in (tuple, list) or type(to_position) not in (tuple, list):
            raise TypeError( "Inputs to game.moveUnit must be of type list or tuple." )
        if len(from_position) != 2 or len(to_position) != 2:
            raise ValueError( "Each input to game.moveUnit must have length 2." )
        if self.map.getColor( from_position ) != self.getCurrentPlayer().__color__:
            raise RuntimeError( "Trying to move a piece from a different player, or an empty square." )
        elif self.map.getType( from_position ) != cell.UNIT:
            raise RuntimeError( "The piece that is attempting to be moved is not of type cell.UNIT." )
        elif from_position in self.__moved__:
            raise RuntimeError( "That piece has already moved this turn." )
        # Determine if the unit is moving to a tower
        if self.map.getType( to_position ) == cell.TOWER:
            moving_to_tower = True
            to_color = self.map.getColor( to_position )
        else:
            moving_to_tower = False
        self.map.makeMove(from_position, to_position)
        self.__moved__.add(to_position)
        # Return the player that was destroyed, if there was one.
        if moving_to_tower and self.map.getType( to_position ) != cell.TOWER:
            self.destroyPlayer( to_color )
            return to_color
        else: 
            return None

    def endTurn(self):
        """
        Ends the turn of the current player, assigning them all of the resources that they get for the
        turn and rotating to the next player who is still playing.
        """
        # Collect resources for the current player
        current_player = self.__rotator__.getCurrentPlayer()
        resources_collected = self.map.collectPlayerResources(current_player.getColor())
        current_player.changeResources(resources_collected)
        # Find the next player who is still in the game
        self.__moved__.clear()
        self.__current_player__ = self.__rotator__.rotate()

    def destroyPlayer(self, color):
        """
        Removes all of a player's units from the board and takes them out of the game.
        """
        if not self.__rotator__.hasColor(color):
            raise ValueError("Color " + str(color) + " is not in the game.")
        self.__rotator__.removePlayer(color)
        self.map.removeColor(color)
        self.__current_player__ = self.__rotator__.getCurrentPlayer()

    def makeUnit(self, location):
        """
        Create a unit in the given location.
        """
        if type(location) not in (list, tuple) or len(location) != 2:
            raise TypeError( "Input to game.makeUnit must be a list or tuple of length 2." )
        tower_pos = self.map.getTower(self.getCurrentPlayer().getColor())
        if location not in self.map.getAdjacent( tower_pos ):
            raise ValueError( "The input location is not adjacent to the current player's tower." )
        if self.map.getType( location ) != cell.EMPTY:
            raise RuntimeError( "The input location is non-empty." )
        if self.__current_player__.getResources() < NEW_UNIT_COST:
            raise RuntimeError( "The player does not have enough resources to generate a new unit." )
        # Add a new unit in the given location
        self.map.setCell(location,
                         color=self.__current_player__.getColor(),
                         strength = DEFAULT_NEW_UNIT_STRENGTH,
                         type=cell.UNIT)

    def makeMove(self, vect):
        """
        Perform a move given a MoveVector object.
        """
        if type(vect) is not movevector.MoveVector:
            raise TypeError( "Input to game.getMove must be of type MoveVector." )
        move_type = vect.getMoveType()
        contents  = vect.getMoveContents()
        # Run over different cases for the move type.
        # Note that error checking on move contents is performed in movevector.py upon
        # vector initialization.
        contents = vect.getMoveContents()
        if move_type == movevector.TYPE_MOVE_UNIT:
            self.moveUnit(contents[0], contents[1])
        elif move_type == movevector.TYPE_MAKE_UNIT:
            self.makeUnit(contents)
        elif move_type == movevector.TYPE_END_TURN:
            self.endTurn()
        else:
            raise RuntimeError( "Move type " + str(move_type) + " not identified." )
        self.__stored_moves__ += [vect]

    def queryCurrentPlayer(self):
        """
        Gets all the moves that the player wants to make.
        """
        moving_player = self.__rotator__.getCurrentPlayer()
        # Get an iterator that gives us all the moves that the player intends
        # on making.
        move_iterator = moving_player.getMove(copy.deepcopy(self.map))
        try:
            move_iterator = iter(move_iterator())
            for move in move_iterator:
                self.makeMove(move)
            # After running through the iterator, it should be the next player's turn
            if self.getCurrentPlayer().getColor() == moving_player.getColor():
                raise RuntimeError( "Finished iterating over move_iterator in getMoves() " +
                                    "before the player ended their turn with a move of type " +
                                    "movevector.END_TURN." )
        except TypeError:
            raise TypeError( "The value returned from player " + 
                             cell.getColorString(moving_player.getColor()) + "'s getMove() function " +
                             "was not iterable." )

    def getMap(self):
        """Returns a reference to the game map."""
        return self.map
