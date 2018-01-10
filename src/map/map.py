"""
   .. module: map
    :synopsis: Defines the Map class, storing all the basic information
   contained within the current map.
"""

from . import cell
from . import _map_logic, _map_getters_setters, _map_private
from numpy import zeros

"""
Used to store the current state of the game.
"""
class Map(object):

    def __init__(self, m, n, grid="hex"):
        """Initialize the map's data fields."""
        # Create an m x n grid
        if type(grid) is not str:
            raise TypeError( "The grid keywork input must be of type string." )
        elif grid not in cell.HEX_MAP_TYPE + cell.SQUARE_MAP_TYPE:
            raise ValueError( "Grid type not found." )
        self.__colors__       = zeros((m,n), dtype=int)
        self.__strengths__    = zeros((m,n), dtype=int)
        self.__resources__    = zeros((m,n), dtype=int)
        self.__types__        = zeros((m,n), dtype=int)
        self.__isdisabled__   = zeros((m,n), dtype=int) != 0
        self.__numrows__      = m
        self.__numcols__      = n
        self.__grid__         = grid
        self.__towerIndices__ = set()
        self.__setAllAdjacencies__()

    setCell      = _map_getters_setters.setCell
    setColor     = _map_getters_setters.setColor
    setType      = _map_getters_setters.setType
    setStrength  = _map_getters_setters.setStrength
    setResources = _map_getters_setters.setResources
    setDisabled  = _map_getters_setters.setDisabled

    getCellDict   = _map_getters_setters.getCellDict
    getCell       = _map_getters_setters.getCell
    getDimensions = _map_getters_setters.getDimensions
    getColor      = _map_getters_setters.getColor
    getType       = _map_getters_setters.getType
    getStrength   = _map_getters_setters.getStrength
    getResources  = _map_getters_setters.getResources
    getDisabled   = _map_getters_setters.getDisabled
    getAdjacent   = _map_getters_setters.getAdjacent
    getRGB        = _map_getters_setters.getRGB
    getAdjacent   = _map_getters_setters.getAdjacent
    getTower      = _map_getters_setters.getTower
    getUnits      = _map_getters_setters.getUnits

    collectResources = _map_logic.collectResources
    collectPlayerResources = _map_logic.collectPlayerResources
    makeMove = _map_logic.makeMove
    removeColor = _map_logic.removeColor
    
    __setAllAdjacencies__   = _map_private.__setAllAdjacencies__
    __setAdjacent__         = _map_private.__setAdjacent__
    __setAdjacent_hex__     = _map_private.__setAdjacent_hex__
    __setAdjacent_square__  = _map_private.__setAdjacent_square__
    __checkIndices__        = _map_private.__checkIndices__
    __checkAdjacent__       = _map_private.__checkAdjacent__
