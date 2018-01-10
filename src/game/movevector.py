"""
   ..module: movevector
   :synopsis: A class to store the contents of a move that a player
   wants to make.
"""

# Types of moves that the player is able to make
TYPE_END_TURN  = 0
TYPE_MOVE_UNIT = 1
TYPE_MAKE_UNIT = 2

END_TURN_ERROR = "No move contents should be supplied for a move of type TYPE_END_TURN."

MOVE_UNIT_ERROR =  "Move contents for a move of type TYPE_MOVE_UNIT must be a tuple or list "
MOVE_UNIT_ERROR += "containing two (i,j) pairs."

MAKE_UNIT_ERROR = "Move contents for a move of type TYPE_MAKE_UNIT should be a single (i,j) pair."

"""
Used to communicate between Players and Games.
"""
class MoveVector(object):

    def __init__(self, move_type=None, move_contents=None):
        """Constructor for a MoveVector object."""
        # Error checking on move contents
        if move_type == TYPE_MOVE_UNIT:
            if type(move_contents) not in (tuple,list):
                raise Exception(MOVE_UNIT_ERROR)
            elif type(move_contents[0]) not in (tuple,list) or type(move_contents[1]) not in (tuple,list):
                raise Exception(MOVE_UNIT_ERROR)
            elif len(move_contents[0]) != 2 or len(move_contents[1]) != 2:
                raise Exception(MOVE_UNIT_ERROR)
        elif move_type == TYPE_MAKE_UNIT:
            if type(move_contents) not in (tuple,list) or len(move_contents) != 2:
                raise Exception(MAKE_UNIT_ERROR)
        elif move_type == TYPE_END_TURN:
            if move_contents is not None:
                raise Exception(END_TURN_ERROR)
        else:
            raise Exception("Move type not identified.")
        # Set elements of move vector
        self.__move_type__     = move_type
        self.__move_contents__ = move_contents

    def getMoveType(self):
        """Getter for move type."""
        return self.__move_type__

    def getMoveContents(self):
        """Getter for move contents."""
        return self.__move_contents__
