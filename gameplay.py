"""
This file contains the implementation that sets the game's parameters and plays the game.
"""

from game import Game
from game import Tile

game: Game = Game()
factories: list[list[Tile]] = game.initalise_factories(num_of_players = 3)

print(game.return_factories())
print(game.return_center())
print(game.return_lid())

returned_tiles: list[list[Tile]] = game.select_from_factory(tile_type="red", factory_index=0)
print(f"{returned_tiles = }")
game.place_onto_pattern_line(tile_type="red", returned_tiles=returned_tiles, line_index=0)