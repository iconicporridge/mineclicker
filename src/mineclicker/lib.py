"""
Where the MineClicker class is located. This class can be used
to create minesweeper style games like:

from mineclicker.lib import MineClicker
game = MineClicker()
game.flag_tile((2,2))
etc.
"""

import numpy as np
import random as rand


class MineClicker:
    """
    A class for a minesweeper style gameboard.
    Create an instance like:
        instance = MineClicker(args)
    Attributes
    ----------
        grid : numpy.ndarray
            The state of the gameboard
        swept : numpy.ndarray
            Where the user has swept a tile
        flagged : numpy.ndarray
            Where user has flagged a tile
        won : Boolean
            Whether the user has won
        lost : Boolean
            Whether the user has lost
        quit : Boolean
            If the user would like to quit
        number_of_mines :
            The number of mines on the grid
        max_number_of_adj_mines : int
            The maximum number of adjacent mines on a 2D grid
        unexplored : int
            A number which indicates a tile on the board has not been swept
        mine : int
            A number which indicates a tile on the board is a mine
        exploded : int
            A number which indicated a detonated mine on the board
        flag : int
            A number which indicates a flag on the board
    Methods
    -------
        __init__(locations):
            Initialise the gameboard, laying down 10 random mines if locations
            is not specified
        cli_take_action():
            A built in function for taking a turn
            using a command line interface
        player_view():
            Return a suitably masked grid for the player
        parse_coords(user_string):
            Parses a user submitted string
            into a tuple that can be used to index arrays
        flag_tile(location):
            Flag a possible mine
        clear_swept_flags():
            Clear flags on swept tiles
        sweep_tile(location):
            Wweep a tile (it could be a mine!)
        sum_adjacent_mines(location):
            Return how many mines are in the 8 adjacent tiles
        valid_location(location):
            Test if a location is valid, used to sanitise inputs
        check_game_state():
            Change the won/lost flags based on the grid
        exit_game():
            Function for indicating the user wants to leave the game
    More documentation can be found in the docstring for each function and
    general advice can be found in the README.md
    """

    def __init__(self, locations=None):
        """
        Constructor for MineClicker. Sets up an 8 by 8 gameboard. If locations
        are provided, it puts mines down at those locations, otherwise 10 mines
        are randomally distributed across the board.
        Parameters
        ----------
        locations : list of tuples or None
            A list of tuples where mines should be placed, for example
            [(2, 3), (4, 5)]
        """

        self.won = False
        self.lost = False
        self.quit = False

        # setup some unique numbers to represent the game state on the grid
        # (0-8 are accounted for by being viable adjacent mine counts)
        self.max_number_of_adj_mines = 8
        self.unexplored = 9
        self.mine = 10
        self.exploded = 11
        self.flag = 12

        # numpy arrays are accessed [row, col] where [0,0] is the top left of
        # the array (when printed):
        # [[(0,0), (0,1)]
        #  [(1,0), (1,1)]]
        self.rows = 8
        self.cols = 8
        self.grid = np.zeros([self.rows, self.cols], dtype=int)
        self.grid.fill(self.unexplored)

        # arrays for flags, should be seperate from actual game state
        self.flagged = np.zeros([self.rows, self.cols], dtype=int)
        self.swept = np.zeros([self.rows, self.cols], dtype=int)

        if locations is None:
            self.number_of_mines = 10
            # it is easy to sample for locations in a range, which we then turn
            # int a grid location by incrementing left to right, top to bottom:
            # [[0, 1, 2, 3]
            #  [4, 5, 6, 7]
            mine_locations_flat = rand.sample(range(self.rows*self.cols),
                                              self.number_of_mines)
            for location in mine_locations_flat:
                location = divmod(location, self.cols)
                self.grid[location] = self.mine
        else:
            self.number_of_mines = 0
            for location in locations:
                if self.valid_location(location):
                    self.grid[location] = self.mine
                    self.number_of_mines += 1

    def cli_take_action(self):
        """
        This function included with the class makes it
        very easy to create a CLI instance of minesweeper.
        It iterates the game state of CLI mineclicker: printing the gameboard and
        useful information, prompting the user for action
        and letting them know if they have won or lost the game.
        """
        print("\n" + f"{self.player_view()}" + "\n")
        user_string = input(
            f"{np.nan}: unexplored, {self.flag}: player flag\n\n" +
            "0 0 is top left\n" +
            f"there are {self.number_of_mines} mines in the grid\n" +
            "to sweep a tile, enter the coordinates $row $col like 3 4\n" +
            "to flag/unflag a tile, enter f$row $col like f3 4\n" +
            "to quit to menu, enter q\n"
            )

        if user_string == "q":
            self.exit_game()
        else:
            location = self.parse_coords(user_string.strip("f"))
            if location is not None:
                if "f" in user_string:
                    self.flag_tile(location)
                else:
                    self.sweep_tile(location)
                self.clear_swept_flags()
            if location is None:
                print("\n!!!No action taken " +
                      "as your command was not understood!!!")
                return

        if (self.won or self.lost):
            endgame = np.zeros((self.rows, self.cols))
            endgame[:] = self.grid[:]
            endgame[np.where(endgame == self.unexplored)] = np.nan
            print(
                f"\n{endgame}\n" +
                f"{np.nan}: unexplored, " +
                f"{self.mine}: mine, {self.exploded}: detonated mine!"
                  )

    def player_view(self):
        """
        A function that returns a grid intended for the player to view -
        which means indicating flagged tiles and masking mines.
        Returns
        -------
        numpy.ndarray
            An array that represents the gameboard the player should be
            able to see.
        """
        view = np.zeros([self.rows, self.cols])
        view[:] = self.grid[:]

        mine_mask = np.where(self.grid == self.mine)
        view[mine_mask] = np.nan

        unexplored_mask = np.where(self.grid == self.unexplored)
        view[unexplored_mask] = np.nan

        flag_mask = np.where(self.flagged == 1)
        view[flag_mask] = self.flag

        return view

    def parse_coords(self, user_string):
        """
        Paramaters.
        ----------
        user_string : string
            A location in the grid formatted like "2 2"
        Returns
        -------
        tuple
            The location in a format like (2, 2)
        None
            Returns None if the location can't be parsed
        """
        parsing = user_string.split(' ')
        if len(parsing) != 2:
            return None
        try:
            row = int(parsing[0])
            col = int(parsing[1])
            location = (row, col)
            if self.valid_location(location):
                return location
            else:
                return None
        except Exception:
            return None

    def flag_tile(self, location):
        """
        Allows the user to flag a tile on the gameboard. This
        is meant to indicate that the user thinks the tile
        is a mine. Alters the flagged data strucure.
        Paramaters.
        ----------
        location : tuple
            A location in the grid formatted like (2,2)
        """
        self.flagged[location] = not self.flagged[location]

    def clear_swept_flags(self):
        """
        Remove flags from any swept locations. Useful if you don't want the
        user to be able to flag a swept location, or you want the flag
        automatically removed on sweep. Alters the flagged data structure.
        """
        self.flagged[np.where(self.swept)] = 0

    def sweep_tile(self, location):
        """
        Sweep a tile on the gameboard, this will:
            - denotate a mine
            - or if the location is not mined, ti will update the gameboard
              with the number of mines adjacent to the swept location.
        Triggers the check_game_state() function which updates the game state
        if the sweep action caused victory or defeat. Alters the swept and grid
        data structures.
        Paramaters.
        ----------
        location : tuple
            A location in the grid formatted like (2,2)
        """
        self.swept[location] = 1
        if self.grid[location] == self.mine:
            self.grid[location] = self.exploded
        else:
            self.grid[location] = self.sum_adjacent_mines(location)
        self.check_game_state()

    def sum_adjacent_mines(self, location):
        """
        Return the number of undetonated mines adjacent to a location on
        the gameboard.
        Paramaters.
        ----------
        location : tuple
            A location in the grid formatted like (2,2)
        Returns
        -------
        int
            Number of mines adjacent (inlcuding diagonals) to location
        """
        adjacent_mines = 0
        [row, col] = location
        adjacent_locations = [(row+1, col),
                              (row-1, col),
                              (row, col+1),
                              (row, col-1),
                              (row+1, col+1),
                              (row+1, col-1),
                              (row-1, col+1),
                              (row-1, col-1)]
        for location in adjacent_locations:
            if self.valid_location(location):
                if self.grid[location] == self.mine:
                    adjacent_mines += 1
        return adjacent_mines

    def valid_location(self, location):
        """
        Test if a location is not nonsense and lies within the gameboard
        boundaries.
        Paramaters.
        ----------
        location : tuple
            A location in the grid formatted like (2,2)
        Returns
        -------
        boolean
            True if location is valid and False if it is not
        """
        try:
            [row, col] = location
        except Exception:
            return False
        if ((row >= self.rows) or (row < 0) or
                (col >= self.cols) or (col < 0)):
            return False
        else:
            return True

    def check_game_state(self):
        """
        Check the game state and change the instances won and lost
        flags accordingly. The user wins if they have explored
        every tile that is not a mine. They lose if they detonate
        (sweep) a mine.
        """
        if self.exploded in self.grid:
            self.lost = True
        elif not (self.grid == self.unexplored).any():
            self.won = True

    def exit_game(self):
        """
        The function to be called when the user wants to leave
        the game board. Right now it just changes the state of
        the instances quit flag.
        """
        self.quit = True
