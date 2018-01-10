"""
   .. module: map
    :synopsis: This module primarily contains the Map class and the Cell module.
    The Map class keeps track of the current board state, while the Cell module
    contains a large variety of useful functions and constants dealing with
    player color and board state.
"""

from . import cell as cellmod
from . import map  as mapmod

import re, sys, os

Map = mapmod.Map
Cell = cellmod.Cell

