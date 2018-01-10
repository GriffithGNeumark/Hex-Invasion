"""
The Cell class defines cells of the map. Each cell contains a unit, a city, some resources, or nothing.
"""

#Types of maps: hexagonal and square.
HEX_MAP_TYPE    = ["hex", "hexagonal", "hexagon"]
SQUARE_MAP_TYPE = ["square"]

# Types of units
EMPTY = 0
UNIT  = 1
TOWER = 2

# Possible colors
RED      = 1
GREEN    = 2
BLUE     = 3
YELLOW   = 4

# Corresponding RGB values
RGB_RED = (255, 0, 0)
RGB_GREEN = (0, 128, 0)
RGB_BLUE = (0, 0, 255)
RGB_YELLOW = (255, 255, 0)
RGB_WHITE = (255, 255, 255)
RGB_BLACK = (0, 0, 0)

# Strings corresponding to colors
COLOR_STRINGS = {RED: "red", GREEN: "green",
                 BLUE: "blue", YELLOW: "yellow", EMPTY: "empty"}

# Maximum possible number of players
MAX_PLAYERS = 4

# Resources claimed from tiles
TOWER_RESOURCES = 5

"""
Cell class; describes the contents of a cell of the board.
   .type: type of unit stored in this cell (including "empty")
   .color: color of the unit stored in this cell (or empty)
   .strength: strength of the unit at this cell. This value is 0 if and only if
              the cell is empty.
   .adjacent: a list of the cells adjacent to this one. Can be set using the
              "addAdjacent" function.
"""
class Cell(object):
    
    def __init__(self, color=EMPTY, strength=EMPTY, type=EMPTY,
                 resources=0, isdisabled=False, adjacent=[]):
        """Constructor for a cell object. Sets all the data fields of the cell."""
        self.color     = color
        self.strength  = strength
        self.type      = type
        self.resources = resources
        self.disabled  = isdisabled
        self.adjacent  = adjacent

def validPlayerColor(color):
    """Checks whether or not a player can take on the input color."""
    if color not in (RED, GREEN, BLUE, YELLOW):
        return False
    else:
        return True

def validColor(color):
    """Check whether or not the input color is a valid color (including EMPTY)."""
    if color not in (RED, GREEN, BLUE, YELLOW, EMPTY):
        return False
    else:
        return True

def getColorString(color):
    """Get the string corresponding to a color."""
    if type(color) is not int:
        raise TypeError("The input to getColorString is not of type int.")
    if color in COLOR_STRINGS:
        return COLOR_STRINGS[color]
    else:
        raise ValueError("Input color not found.")
