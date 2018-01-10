"""
Base class for Game AI. Defines various methods that are used by or implemented
in the AI players.
"""

import os, sys

cell_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.pardir)
if cell_path not in sys.path:
    sys.path.append( cell_path )

import game
import map
import game.movevector as movevector

"""
Parent AI class. Inherits from the generic Player class.
"""
class Agent(game.Player):

    """
    Class constructor.
    """
    def __init__(self):
        # Set contains the indices of all units that have moved this
        # turn (contains the indices of the final position of the unit).
        self.__moved_units__ = set()

    """
    Policy that is implemented by the AI. Takes a Map and a position of a unit
    to move. Should be implemented in child classes. Returns a MoveVector object.
    """
    def policy(self, map, pos):
        pass

    """
    Policy for making new units. Always occurs at the start of the turn.
    """
    def makeUnitPolicy(self, map):
        pass

    """
    Partially implements the makeMove method in the Player class.
    The generic policy for an AI goes as follows:

       1. Make units
       2. Loop over all cells and move units.
       3. End turn.

    The same game state can be reached at the end of every turn regardless of
    the order in which we move the units; therefore, we simply loop over them
    as is convenient.

    This function is a generator, so that the game can loop over the moves in
    this 
    """
    def makeMove(self, game_map):
        # Clear the __moved_units__ set
        self.__moved_units__ = set
        # Get all indices containing a unit of this player
        units = game_map.getUnits(self.__color__)
        # Make all units at the start of the turn
        for move in self.makeUnitPolicy(game_map):
            if type(move) is not movevector.MoveVector or move.getType() != movevector.TYPE_MAKE_UNIT:
                raise TypeError( "The return value from makeUnitPolicy should be a " +
                                 "MoveVector of type TYPE_MAKE_UNIT." )
            else:
                # Place position of made unit in __moved_units__
                pos = move.getContents()
                self.__moved_units__.add(pos)
        for unit in units:
            # Skip over moved units, esp. units that have been combined with units
            # that were moved earlier.
            if unit in self.__moved_units__:
                continue
            else:
                move = self.policy(game_map, unit)
                if type(move) is not movevector.MoveVector or move.getType() != movevector.TYPE_MOVE_UNIT:
                    raise TypeError("The return value from the policy() function should " +
                                    "be a MoveVector of type TYPE_MOVE_UNIT.")
                else:
                    # Place final position of unit in __moved_units__
                    _, final_position = move.getContents()
                    self.__moved_units__.add(final_position)
        yield movevector.MoveVector(move_type=movevector.TYPE_END_TURN)
