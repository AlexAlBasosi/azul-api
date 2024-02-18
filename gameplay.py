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
    factories: list[list[Tile]] = game.initalise_factories(num_of_players = 3)

    print(f"Factories: {game.return_factories()}")
    print(f"Center: {game.return_center()}")
    print(f"Lid: {game.return_lid()}\n")

    # Factory Offer:
    ## Now, the user starts to play. They start by selecting all the red tiles from the first factory.
    returned_tiles: list[list[Tile]] = game.select_from_factory(tile_type="red", factory_index=0)
    print(f"Returned Tiles: {returned_tiles}\n")

    # The returned tiles, which include the selected and discarded tiles, are passed into this method.
    # Here, the user places the tiles onto the second pattern line.
    game.place_onto_pattern_line(tile_type="red", returned_tiles=returned_tiles, line_index=1)

    # If there are any extra tiles that need to be added to the floor line, they can be added here.
    # In this example, the user adds a red tile to the floor line.
    floor_tiles: list[Tile] = [Tile("red")]
    game.place_onto_floor_line(tiles=floor_tiles)

    # Now, the user checks the state of the game to see their next steps.
    print(f"Factories: {game.return_factories()}")
    print(f"Pattern Lines: {game.return_pattern_lines()}")
    print(f"Center of Table: {game.return_center()}")
    print(f"Floor Line: {game.return_floor_line()}\n")

    # They decide to take the black tiles from the center of the table this time.
    selected_tiles: list[Tile] = game.select_from_center(tile_type="black")
    print(f"Selected Tiles from center: {selected_tiles}")
    print(f"Center of Table: {game.return_center()}")
    print(f"Floor Line: {game.return_floor_line()}\n")

    print(f"Wall: {game.return_wall()}")

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

