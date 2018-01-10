"""
   .. module: _map_private
    :synopsis: Hidden functions for the map class. The functions in this
    file are stored as methods in the Map class; see map.py.
"""

from . import cell

def __setAllAdjacencies__(self):
    """
    Get an m x n array where entry (i,j) is a list of tuples (k,l) representing the indices of
    a cell adjacent to (i,j).
    This function loops over all of the cells in the map and uses the __setAdjacent__ function
    to find adjacent cells.
    There are two types of grids: hexagonal and square.
    """
    self.__adjacent__ = []
    for i in range(0,self.__numrows__):
        self.__adjacent__ += [[]]
        for j in range(0,self.__numcols__):
            self.__adjacent__[i] += [[]]
    # Set grid for hexagonal maps
    if self.__grid__ in cell.HEX_MAP_TYPE:
        for i in range(0,self.__numrows__):
            for j in range(0,self.__numcols__):
                self.__setAdjacent_hex__( (i,j) )
    # Set grid for square maps
    elif self.__grid__ in cell.SQUARE_MAP_TYPE:
        for i in range(0,self.__numrows__):
            for j in range(0,self.__numcols__):
                self.__setAdjacent_square__( (i,j) )
    else:
        raise ValueError( "Grid type not found." )

def __setAdjacent__(self, pos):
    """
    Generalized setAdjacent function. Sets the adjacencies based on the type of
    grid that we are using.
    """
    if type(pos) not in (list, tuple):
        raise TypeError( "The input to __setAdjacent__ must be of type list or tuple." )
    elif len(pos) != 2:
        raise ValueError( "The input to __setAdjacent__ must have length 2." )
    if self.__grid__ in cell.HEX_MAP_TYPE:
        self.__setAdjacent_hex__( pos )
    elif self.__grid__ in cell.SQUARE_MAP_TYPE:
        self.__setAdjacent_square__( pos )
    else:
        raise ValueError( "The grid type was not recognized." )

def __setAdjacent_hex__(self, pos):
    """
    Get all the cells that are adjacent to the cell with the input row and column. Sets
    entry (i,j) to be equal to the list of adjacent cells in self.adjacent. Used for
    hexagonal grids.
    """
    self.__checkIndices__(pos)
    i, j = pos; adjacent = []
    # Create a function that will take a list of cells that are possible adjacent
    # to cell (i,j) and filters out the ones that are disabled or lay outside
    # of the map.
    def filterfn(p):
        do_not_filter = 0 <= p[0] < self.__numrows__ and 0 <= p[1] < self.__numcols__
        return do_not_filter and not self.__isdisabled__[p[0]][p[1]]
    possibly_adjacent = [(i-1,j),(i+1,j),(i,j+1),(i,j-1)]
    if i % 2 == 0:
        possibly_adjacent += [(i-1,j-1),(i+1,j-1)]
    else:
        possibly_adjacent += [(i-1,j+1),(i+1,j+1)]
    for cell in filter(filterfn, possibly_adjacent):
        adjacent += [cell]
    self.__adjacent__[i][j] = adjacent

def __setAdjacent_square__(self, pos):
    """
    Sets all adjacencies in the map for a map with square tiles.
    """
    self.__checkIndices__(pos)
    i, j = pos; adjacent = []
    # Function to filter out nonexistent cells.
    def filterfn(p):
        do_not_filter = 0 <= p[0] < self.__numrows__ and 0 <= p[1] < self.__numcols__
        return do_not_filter and not self.__isdisabled__[p[0]][p[1]]
    for cell in filter(filterfn, ( (i+1,j), (i-1,j), (i,j+1), (i,j-1) )):
        adjacent += [cell]
    self.__adjacent__[i][j] = adjacent

def __checkIndices__(self,pos):
    """
    Check whether indices i, j are valid indices for a given map. Raise an exception if
    they are not.
    """
    i, j = pos
    if type(i) is not int or type(j) is not int:
        raise TypeError( "Indices are not integers." )
    elif i < 0 or j < 0:
        raise ValueError( "Received a negative index." )
    elif i >= self.__numrows__ or j >= self.__numcols__:
        raise IndexError( "Index out of bounds." )

def __checkAdjacent__(self,from_position,to_position):
    """
    Raise an exception if cells (from_x,from_y) and (to_x,to_y) are not adjacent.
    Takes two tuples with two values, representing the x and y coordinates of the
    positions on the map.
    """
    from_x, from_y = from_position[0], from_position[1]
    self.__checkIndices__( from_position )
    self.__checkIndices__( to_position )
    if to_position not in self.__adjacent__[from_x][from_y]:
        raise RuntimeError("Cells " + str( from_position ) + " and " + str( to_position ) 
                           + " are not adjacent.")
