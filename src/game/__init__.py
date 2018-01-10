"""
   .. module: game
    :synopsis: Contains a variety of classes that serve as abstractions for
    storing the current game state.
"""

from . import game as gamemod
from . import player as playermod

# Allows user to instantiate a Game object by importing
# this module.
Game = gamemod.Game

# Allows uer to instantiate a Player object by importing
# this module.
Player = playermod.Player
