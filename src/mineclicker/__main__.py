"""
A main function for the mineclicker module which launches a CLI game
when invoked like: python -m mineclicker
"""

from .lib import MineClicker
import sys


def check_yes(user_string):
    """
    A function to test user meaning when they are asked to return a
    Y/N style input
    Paramaters
    ----------
    user_string : string
        The user input, hopefully something like "yes" or "no"
    Returns
    -------
    boolean
        True for "yes" style answers and False for "no" style answers
    """
    answers = {"Yes": True, "yes": True, "Y": True, "y": True,
               "No": False, "no": False, "N": False, "n": False}
    if user_string in answers:
        return answers[user_string]
    else:
        return None


def run_cli_game(locations=None):
    """
    Logic to launch the user into a (quittable) cli game of mineclicker,
    if locations are provided then mines are placed at them otherwise the
    MineClicker class will randomally allocate mines on the board.
    Parameters
    ----------
    locations : list of tuples or None
     A list of tuples where mines should be placed, for example
            [(2, 3), (4, 5)]
    """
    while True:
        quit = False
        game = MineClicker(locations)
        print("\nStarting game!")
        finished = False
        while finished is False:
            game.cli_take_action()
            if (game.lost or game.won or game.quit):
                finished = True
                if game.won:
                    continue_string = input(
                        "\nYou won!!! would you like to try again? (Yes/No)\n")
                if game.lost:
                    continue_string = input(
                        "\nYou lost :( Would you like to try again?" +
                        " (Yes/No)\n")
                if game.quit:
                    continue_string = input(
                        "\nYou quit, would you like to setup a new game?" +
                        " (Yes/No)\n"
                        )
                if check_yes(continue_string) is None:
                    clear_answer = False
                    while clear_answer is False:
                        continue_string = input(
                            "\nYour answer was not clear, " +
                            "would you like to start a new game? (Yes/No)\n"
                            )
                        if check_yes(continue_string) is not None:
                            clear_answer = True
                if not check_yes(continue_string):
                    quit = True
        if quit is True:
            print("\nThanks for playing :)\n")
            break


if __name__ == "__main__":
    """
    If the user runs this file as main then launch a game
    """
    if len(sys.argv) > 1:
        try:
            locations = []
            strings = sys.argv[1:]
            for string in strings:
                string = string.split(',')
                locations.append((int(string[0]), int(string[1])))
        except Exception:
            print("\n!Something about your list of mine locations " +
                  "wasn't right, launching a random game!")
            locations = None
    else:
        locations = None
    run_cli_game(locations)
