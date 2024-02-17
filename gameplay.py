"""
This file contains the implementation that sets the game's parameters and plays the game.
"""

from game import Game
from game import Tile

game: Game = Game()

try:
    factories: list[list[Tile]] = game.initalise_factories(num_of_players = 3)

    print(game.return_factories())
    print(game.return_center())
    print(game.return_lid())

    returned_tiles: list[list[Tile]] = game.select_from_factory(tile_type="red", factory_index=0)
    print(f"{returned_tiles = }")

    game.place_onto_pattern_line(tile_type="red", returned_tiles=returned_tiles, line_index=0)

    game.place_onto_floor_line(tiles=[Tile("red")])
    print(f"{game.return_lid() = }")
    game.place_onto_floor_line(tiles=[Tile("red"), Tile("red"), Tile("red")])
    print(f"{game.return_lid() = }")
    game.place_onto_floor_line(tiles=[Tile("red"), Tile("red")])
    print(f"{game.return_lid() = }")
    game.place_onto_floor_line(tiles=[Tile("red"), Tile("red")])
    print(f"{game.return_lid() = }")
    game.place_onto_floor_line(tiles=[Tile("red"), Tile("red")]) 
    print(f"{game.return_lid() = }")
    game.place_onto_floor_line(tiles=[Tile("red"), Tile("red")]) 
    print(f"{game.return_lid() = }")
    
except ValueError as value_message:
    print(f"Value Error: {value_message}")
except IndexError as index_message:
    print(f"Index Error: {index_message}")
except TypeError as type_message:
    print(f"Type Error: {type_message}")
except OverflowError as overflow_message:
    print(f"Overflow Error: {overflow_message}")

