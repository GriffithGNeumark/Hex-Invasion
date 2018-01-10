"""
   .. module: _map_getters_setters
     :synopsis: Getter and setter functions for the Map class. All of
     these functions are stored as methods of the map class in map.py.
"""

from . import cell
import itertools
import numpy as np

# Dictionary that stores the RGB values corresponding to a given color.
RGB_DICT = {cell.EMPTY:  cell.RGB_WHITE,
            cell.RED:    cell.RGB_RED,
            cell.GREEN:  cell.RGB_GREEN,
            cell.BLUE:   cell.RGB_BLUE,
            cell.YELLOW: cell.RGB_YELLOW}

def setCell(self, pos, color=None, type=None, strength=None, 
            resources=None, isdisabled=None):
    """
    Sets a different property of cell (i,j) for each keyword parameter
    that isn't None.
    """
    self.setColor(     pos, color      )
    self.setType(      pos, type       )
    self.setStrength(  pos, strength   )
    self.setResources( pos, resources  )
    self.setDisabled(  pos, isdisabled )

def setColor(self, pos, color):
    """Sets the color of cell (i,j)."""
    self.__checkIndices__(pos)
    # Do nothing if color is None
    if color is None: return
    elif type(color) is not int:
        raise TypeError("setColor received a non-integer value.")
    elif not cell.validColor(color):
        raise ValueError("setColor received an invalid color.")
    else:
        self.__colors__[pos[0]][pos[1]] = color

def setType(self, pos, cell_type):
    """Sets the type of cell (i,j); possible types are EMPTY, UNIT, and TOWER."""
    i, j = pos
    self.__checkIndices__(pos)
    # Do nothing if color is None
    if cell_type is None: return
    elif type(cell_type) is not int:
        raise TypeError("setType received a non-integer value.")
    elif cell_type not in (cell.EMPTY, cell.UNIT, cell.TOWER):
        raise ValueError("setType received an invalid unit ID.")
    else:
        # If the type of the cell that is being set is currently TOWER, we
        # have to remove it from the set of tower indices.
        if self.__types__[i][j] == cell.TOWER:
            self.__towerIndices__.remove( pos )
        self.__types__[i][j] = cell_type
        # If the type is tower, add the indices to the list of tower units
        if cell_type == cell.TOWER:
            self.__towerIndices__.add( pos )

def setStrength(self, pos, strength):
    """Sets the strength of cell (i,j)."""
    self.__checkIndices__(pos)
    # Do nothing if strength is None
    if strength is None: return
    elif type(strength) is not int:
        raise TypeError("setStrength received a non-integer value.")
    elif strength < 0:
        raise ValueError("setStrength received a negative value.")
    else: self.__strengths__[ pos[0] ][ pos[1] ] = strength

def setResources(self, pos, resources):
    """Sets the resources of cell (i,j)."""
    self.__checkIndices__( pos )
    # Do nothing if resources is None
    if resources is None: return
    elif type(resources) is not int:
        raise TypeError( "setResources received a non-integer value." )
    elif resources < 0:
        raise ValueError( "setResources received a negative value." )
    else: self.__resources__[ pos[0] ][ pos[1] ] = resources

def setDisabled(self, pos, isdisabled):
    """Toggle the enabled/disabled status of an input cell."""
    i, j = pos
    self.__checkIndices__( pos )
    # Do nothing if isdisabled is None
    if isdisabled is None: return
    if type( isdisabled ) is not bool:
        raise TypeError( "setDisabled received a non-boolean value." )
    if isdisabled:
        self.__isdisabled__[i][j] = True
        for cell in self.__adjacent__[i][j]:
            self.__setAdjacent__( cell )
    else:
        self.__isdisabled__[i][j] = False
        # Reset all adjacencies of this cell
        self.__setAdjacent__( pos )
        for cell in self.getAdjacent( pos ):
            self.__setAdjacent__( cell )

def getCellDict(self, pos):
    """
    Gets a dictionary representing the cell in the ith row and jth column.
    Keywords: "color", "strength", "resources", "type", "isdisabled", "adjacent"
    """
    self.__checkIndices__(pos)
    i, j = pos; celldict = {}
    celldict['color']      = self.__colors__[i][j]
    celldict['strength']   = self.__strengths__[i][j]
    celldict['resources']  = self.__resources__[i][j]
    celldict['type']       = self.__types__[i][j]
    celldict['isdisabled'] = self.__isdisabled__[i][j]
    celldict['adjacent']   = self.__adjacent__[i][j]
    return celldict

def getCell(self, pos):
    """Gets a Cell object representing the cell in the ith row and jth column."""
    i, j = pos
    self.__checkIndices__(pos)
    color      = self.__colors__[i][j]
    strength   = self.__strengths__[i][j]
    resources  = self.__resources__[i][j]
    type       = self.__types__[i][j]
    isdisabled = self.__isdisabled[i][j]
    adjacent   = self.__adjacent__[i][j]
    return Cell(color=color, strength=strength, resources=resources, type=type, 
                isdisabled=isdisabled, adjacent=adjacent)

def getDimensions(self):
    """Gets the number of rows and columns of the map"""
    return (self.__numrows__, self.__numcols__)
    
def getColor(self, pos):
    """Get the color of cell (i,j)"""
    self.__checkIndices__(pos)
    return self.__colors__[pos[0]][pos[1]]

def getType(self, pos):
    """Get the type of whatever is occupying cell (i,j)."""
    self.__checkIndices__(pos)
    return self.__types__[pos[0]][pos[1]]

def getStrength(self, pos):
    """Get the strength of cell (i,j)."""
    self.__checkIndices__(pos)
    return self.__strengths__[pos[0]][pos[1]]

def getResources(self, pos):
    """Get the resource generation rate in cell (i,j)."""
    self.__checkIndices__(pos)
    return self.__resources__[pos[0]][pos[1]]

def getDisabled(self, pos):
    """Get a boolean representing whether or not cell (i,j) is disabled."""
    self.__checkIndices__(pos)
    return self.__isdisabled__[pos[0]][pos[1]]

def getAdjacent(self, pos):
    """Get all cells adjacent to cell (i,j)"""
    self.__checkIndices__(pos)
    return self.__adjacent__[ pos[0] ][ pos[1] ]

def getRGB(self, pos):
    """Get the RGB value corresponding to a given cell."""
    self.__checkIndices__(pos)
    if self.__isdisabled__[ pos[0] ][ pos[1] ]: return cell.RGB_BLACK
    else: return RGB_DICT[ self.__colors__[ pos[0] ][ pos[1] ] ]

def getAdjacent(self, pos):
    """Get all cells adjacent to the cell at the input indices."""
    self.__checkIndices__( pos )
    return self.__adjacent__[ pos[0] ][ pos[1] ]

def getTower(self, color):
    """Gets the player tower that has the input color."""
    if not cell.validPlayerColor(color):
        raise ValueError( "The input color (id:" + str(color) + ") is not a valid player color." )
    for (i,j) in self.__towerIndices__:
        if self.__types__[i][j] != cell.TOWER:
            raise RuntimeError( "Indices (" + str(i) + "," + str(j) + ") in "
                                + "__towerIndices__, but cell does not contain a tower." )
        elif self.__colors__[i][j] == color:
            return (i,j)
    raise RuntimeError( "No tower found for color " + cell.COLOR_STRINGS[color] )

def getUnits(self, color):
    """Get all units of a given color."""
    if not cell.validPlayerColor(color):
        raise ValueError("The input to getUnits was not a valid player color.")
    # Find all indices with the input color and with type unit
    indices = np.unravel_index(np.where( (self.__colors__.ravel()==color) &
                                         (self.__types__.ravel()==color) ), self.__colors__.shape)
    # We concatenate the indices vertically and take the transpose so that every
    # row of the array contains a pair of indices into the map. We then convert this
    # to a list and then a tuple.
    return tuple(map(tuple,
                     np.concatenate((indices[0],indices[1]),axis=0).transpose().tolist()))
