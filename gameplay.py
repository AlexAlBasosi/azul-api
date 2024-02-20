"""
This file contains the implementation that sets the game's parameters and plays the game.
"""

# This script simulates setting up the game and simulating a user's actions as they play the game.

from game import Game
from game import Tile

game: Game = Game()

try:
    # Game Setup:
    ## This phase involves setting up the game and initialising the factories. 

    players: list[int] = game.initialise_players(num_of_players = 2)
    factories: list[list[Tile]] = game.initalise_factories()

    player_1: int = players[0]
    player_2: int = players[1]

    print(f"Factories: {game.return_factories()}")
    print(f"Center: {game.return_center()}")
    print(f"Lid: {game.return_lid()}\n")

    # Factory Offer:
    ## Now, the user starts to play. They start by selecting all the red tiles from the first factory.
    print("First Turn:")
    tile_type: str = str(factories[0][0])
    returned_tiles: list[list[Tile]] = game.select_from_factory(tile_type=tile_type, factory_index=0)
    print(f"Returned Tiles: {returned_tiles}\n")
    print("\n\n")

    # The returned tiles, which include the selected and discarded tiles, are passed into this method.
    # Here, the user places the tiles onto the second pattern line.
    game.place_onto_pattern_line(tile_type=tile_type, returned_tiles=returned_tiles, player_index=0, line_index=0)

    # If there are any extra tiles that need to be added to the floor line, they can be added here.
    # In this example, the user adds a red tile to the floor line.
    # floor_tiles: list[Tile] = [Tile("red")]
    # game.place_onto_floor_line(tiles=floor_tiles)

    # Now, the user checks the state of the game to see their next steps.
    # print(f"Factories: {game.return_factories()}")
    # print(f"Pattern Lines: {game.return_pattern_lines()}")
    # print(f"Center of Table: {game.return_center()}")
    # print(f"Floor Line: {game.return_floor_line()}\n")

    # They decide to take the black tiles from the center of the table this time.
    # selected_tiles: list[Tile] = game.select_from_center(tile_type="red")
    # print(f"Selected Tiles from center: {selected_tiles}")
    # print(f"Center of Table: {game.return_center()}")
    # print(f"Floor Line: {game.return_floor_line()}\n")

    print("Second Turn:")
    tile_type = str(factories[1][0])
    returned_tiles = game.select_from_factory(tile_type=tile_type, factory_index=1)
    print(f"Returned Tiles: {returned_tiles}\n")

    print(f"Factories: {game.return_factories()}\n")
    game.place_onto_pattern_line(tile_type=tile_type, returned_tiles=returned_tiles, player_index=0, line_index=1)
    print(f"Pattern Lines: {game.return_pattern_lines(player_index=0)}")
    print("\n\n")


    print("Third Turn:")
    tile_type = str(factories[2][0])
    returned_tiles = game.select_from_factory(tile_type=tile_type, factory_index=2)
    print(f"Returned Tiles: {returned_tiles}\n")
    print(f"Factories: {game.return_factories()}\n")

    game.place_onto_pattern_line(tile_type=tile_type, returned_tiles=returned_tiles, player_index=0, line_index=2)
    print(f"Pattern Lines: {game.return_pattern_lines(player_index=0)}")
    print("\n\n")

    print("Fourth Turn:")
    tile_type = str(factories[3][0])
    returned_tiles = game.select_from_factory(tile_type=tile_type, factory_index=3)
    print(f"Returned Tiles: {returned_tiles}\n")

    print(f"Factories: {game.return_factories()}\n")
    game.place_onto_pattern_line(tile_type=tile_type, returned_tiles=returned_tiles, player_index=0, line_index=3)
    print(f"Pattern Lines: {game.return_pattern_lines(player_index=0)}")
    print("\n\n")

    print("Fifth Turn:")
    tile_type = str(factories[4][0])
    returned_tiles = game.select_from_factory(tile_type=tile_type, factory_index=4)
    print(f"Returned Tiles: {returned_tiles}\n")

    print(f"Factories: {game.return_factories()}\n")
    game.place_onto_pattern_line(tile_type=tile_type, returned_tiles=returned_tiles, player_index=0, line_index=4)
    print(f"Pattern Lines: {game.return_pattern_lines(player_index=0)}")
    print("\n\n")

    print(f"Center of Table: {game.return_center()}")

    # TODO: refactor this so that the user clears the center organically.
    game.clear_center()
    print(f"Center of Table: {game.return_center()}")
    print(f"Floor Line: {game.return_floor_line(player_index=0)}\n")
    
    print("\n\n")

    # Wall Tiling
    ## Now, the user starts to place tiles onto the wall from the pattern lines.
    print(f"Wall: {game.return_wall(player_index=0)}")
    game.place_onto_wall(line_index=0, player_index=0)
    print(f"Wall: {game.return_wall(player_index=0)}")

    #TODO: if factories are empty, refill from bag
    

    #TODO: if bag is empty, refill from lid

except ValueError as value_message:
    print(f"Value Error: {value_message}")
except IndexError as index_message:
    print(f"Index Error: {index_message}")
except TypeError as type_message:
    print(f"Type Error: {type_message}")
except OverflowError as overflow_message:
    print(f"Overflow Error: {overflow_message}")

# TODO: add logic to create multiple boards to represent players
# TODO: add test factories to simplify game script
# TODO: refactor main script into functions to simplify
    
# TODO: Add positional arguments to all public methods
# TODO: Add validation to all public methods.
# TODO: Add comments in various functions
# TODO: Refactor error message to include class and method where error was raised.