"""
This file contains the implementation that sets the game's parameters and plays the game.
"""

from game import Game
from game import Tile

game: Game = Game()
factories: list[list[Tile]] = game.initalise_factories(num_of_players = 3)
print(f"{factories = }")

game.test()