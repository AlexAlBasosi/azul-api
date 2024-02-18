"""
This file contains the implementation that sets the game's parameters and plays the game.
"""

from game import Game
from game import Tile

game: Game = Game()

try:
    factories: list[list[Tile]] = game.initalise_factories(num_of_players = 3)

    print(f"Factories: {game.return_factories()}")
    print(f"Center: {game.return_center()}")
    print(f"Lid: {game.return_lid()}")

    returned_tiles: list[list[Tile]] = game.select_from_factory(tile_type="red", factory_index=0)
    print(f"Returned Tiles: {returned_tiles}")

    game.place_onto_pattern_line(tile_type="red", returned_tiles=returned_tiles, line_index=1)

    game.place_onto_floor_line(tiles=[Tile("red")])
    print(f"Lid: {game.return_lid()}")
    game.place_onto_floor_line(tiles=[Tile("red"), Tile("red"), Tile("red")])
    print(f"Lid: {game.return_lid()}")
    game.place_onto_floor_line(tiles=[Tile("red"), Tile("red")])
    print(f"Lid: {game.return_lid()}")
    game.place_onto_floor_line(tiles=[Tile("red"), Tile("red")])
    print(f"Lid: {game.return_lid()}")
    game.place_onto_floor_line(tiles=[Tile("red"), Tile("red")]) 
    print(f"Lid: {game.return_lid()}")
    game.place_onto_floor_line(tiles=[Tile("red"), Tile("red")]) 
    print(f"Lid: {game.return_lid()}")

    print(f"Pattern Lines: {game.return_pattern_lines()}")
    print(f"Floor Line: {game.return_floor_line()}")

    selected_tiles: list[Tile] = game.select_from_center(tile_type="black")
    print(f"Selected Tiles from center: {selected_tiles}")
    print(f"Center of Table: {game.return_center()}")

    print(f"Wall: {game.return_wall()}")

except ValueError as value_message:
    print(f"Value Error: {value_message}")
except IndexError as index_message:
    print(f"Index Error: {index_message}")
except TypeError as type_message:
    print(f"Type Error: {type_message}")
except OverflowError as overflow_message:
    print(f"Overflow Error: {overflow_message}")

