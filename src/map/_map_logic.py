"""
  .. module: _map_logic
    :synopsis: Defines functions used in the Map class involving the game 
    state; for instance, collecting resources and making a move. All of
    these functions are stored as methods for the Map class (see map.py).
"""

from . import cell
import numpy as np

def collectResources(self):
    """
    Creates a dictionary that records the amount of resources each player can claim at the
    start of their round.
    """
    resource_dict = {cell.RED: 0, cell.GREEN: 0, cell.BLUE: 0, cell.YELLOW: 0}
    for color in resource_dict:
        resource_dict[color] = self.collectPlayerResources(color)
    return resource_dict

def collectPlayerResources(self, color):
    """
    Returns the number of resources a single player can claim at the end of a round.
    """
    if type(color) is not int:
        raise TypeError( "Input to this function should be a valid color (see cell.py) of type int." )
    if not cell.validColor(color):
        raise ValueError( "Input color not recognized (received: " + str(color) + ")" )
    # Get all the indices on the map where the color of a cell is equal to <color>
    color_indices = np.unravel_index(np.where(self.__colors__.ravel()==color),self.__colors__.shape)
    tower_resources = cell.TOWER_RESOURCES * np.sum(self.__types__[color_indices] == cell.TOWER)
    return int(np.round(np.sum(self.__resources__[color_indices]) + tower_resources))

def makeMove(self, from_position, to_position):
    """
    Moves the unit in cell (from_x,from_y) to (to_x,to_y).
    """
    from_x, from_y = from_position[0], from_position[1]
    to_x, to_y     = to_position[0], to_position[1]
    self.__checkAdjacent__(from_position, to_position)
    if self.__isdisabled__[ to_x ][ to_y ]:
        raise RuntimeError( "Cannot move a unit into a disabled cell." )
    if self.__types__[ from_x ][ from_y ] != cell.UNIT:
        raise RuntimeError( "Only units can be moved." )
    start_color    = self.__colors__[ from_x ][ from_y ]
    end_color      = self.__colors__[ to_x ][ to_y ]
    start_strength = self.__strengths__[ from_x ][ from_y ]
    # Deal with two cases:
    #    1. The colors of the start and end tiles are the same
    #    2. The colors of the start and end tiles are different.
    if start_color == end_color:
        if self.__types__[ to_x ][ to_y ] == cell.TOWER:
            raise RuntimeError( "Moving unit into its own tower." )
        # We combine the strengths of units if they have the same color
        self.__strengths__[to_x][to_y] += start_strength
    else:
        final_strength = self.__strengths__[to_x][to_y] - start_strength
        # We take abs(strength of #1 - strength of #2) and set the color
        # of the end square to be that of the stronger unit.
        if final_strength > 0:
            self.__strengths__[ to_x ][ to_y ] = final_strength
            self.__types__[ to_x ][ to_y ]     = cell.UNIT
        elif final_strength < 0:
            self.__strengths__[ to_x ][ to_y ] = -final_strength
            self.__colors__[ to_x ][ to_y ]    = start_color
            self.__types__[ to_x ][ to_y ]     = cell.UNIT
        else:
            self.__colors__[ to_x ][ to_y ] = cell.EMPTY
            self.__types__[ to_x ][ to_y ]  = cell.EMPTY
    # Make the starting cell empty
    self.__colors__[ from_x ][ from_y ]    = cell.EMPTY
    self.__types__[ from_x ][ from_y ]     = cell.EMPTY
    self.__strengths__[ from_x ][ from_y ] = cell.EMPTY
    


        
    
    
"""
Remove all units of a specified color from the board. Also removes indices of towers
from map's __towerIndices__ field.
"""

def removeColor(self, color):
    """
    Remove all units of a specified color from the board. Also removes indices of towers
    from map's __towerIndices__ field.
    """
    self.__towerIndices__ = set([pos for pos in self.__towerIndices__ if
                                 self.__colors__[pos[0]][pos[1]] != color])
    is_destroyed_color = self.__colors__ == color
    for i in range(self.__numrows__):
        for j in range(self.__numcols__):
            if is_destroyed_color[i][j]:
                self.__colors__[i][j] = cell.EMPTY
                self.__types__[i][j] = cell.EMPTY
                self.__strengths__[i][j] = cell.EMPTY
