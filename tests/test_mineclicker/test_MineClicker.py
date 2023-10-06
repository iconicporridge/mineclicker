import pytest
import numpy as np


from mineclicker.lib import MineClicker


def test_setup_default_game():
    """
    This test checks the MineClicker __init__ function when it is
    passed no arguments by checking the gameboard has some expected
    default behaviours
    """
    game = MineClicker()
    no_of_mines = np.sum(game.grid == game.mine, axis=(0, 1))
    assert no_of_mines == 10
    assert game.number_of_mines == no_of_mines


def test_setup_game_with_mines():
    """
    This test checks the MineClicker __init__ function when it
    is passed a list of mine locations by looking at the state
    of the resulting gameboard
    """
    locations = [(0, 1),
                 (4, 5),
                 (6, 2),
                 (0, 4),
                 (-1, -1),
                 "waffles"]
    game = MineClicker(locations)
    assert game.grid.shape == (8, 8)
    no_of_mines = np.sum(game.grid == game.mine, axis=(0, 1))
    assert no_of_mines == 4  # only 4 of the locations are valid
    assert game.number_of_mines == no_of_mines
    for location in locations[:-1]:
        if location != (-1, -1):
            assert game.grid[location] == game.mine


testdata = [("1 1", (1, 1)),
            ("7 4", (7, 4)),
            ("-1 0", None),
            ("0 -1", None),
            ("0 9", None),
            ("9 0", None),
            ("90", None),
            ("fsdaf", None),
            ("1 2 3", None)]
@pytest.mark.parametrize("coord, expected", testdata)
def test_parse_coords(coord, expected):
    """
    This test checks that only valid coordinates are returned
    by parse_coords by submitting a set of representative inputs
    """
    game = MineClicker()
    assert game.parse_coords(coord) == expected

testdata = [((1, 1), True),
            ((7, 4), True),
            ((0, 9), False),
            ((9, 0), False),
            ((-1, 0), False),
            ((0, -1), False),
            (90, False),
            ("fsdaf", False),
            ("1 2", False)]
@pytest.mark.parametrize("location, expected", testdata)
def test_valid_location(location, expected):
    """
    This tests the valid_location function against a
    set of known valid and invalid locations
    """
    game = MineClicker()
    assert game.valid_location(location) is expected


# flag_tile and clear_swept_flags
def test_flagging():
    """
    This test tests the flag_tile and clear_swept_flags
    functions by simulating some possible game scenarios
    """
    game = MineClicker()

    location = (1, 2)
    game.flag_tile(location)
    game.clear_swept_flags()
    assert game.flagged[location] == 1
    assert np.sum(game.flagged, axis=(0, 1)) == 1

    game.flag_tile(location)
    assert game.flagged[location] == 0
    assert np.sum(game.flagged, axis=(0, 1)) == 0

    game.sweep_tile(location)
    game.flag_tile(location)
    game.clear_swept_flags()
    assert game.flagged[location] == 0

    location = (2, 1)
    game.flag_tile(location)
    game.sweep_tile(location)
    game.clear_swept_flags()
    assert game.flagged[location] == 0

    with pytest.raises(Exception):
        game.flag_tile((8, 8))


def test_player_view():
    """
    This test checks that the player_view function returns
    a view suitable for the player by simulating a possible
    scenario and testing that the player can see their flags
    and can't see unexploded mines!"""
    game = MineClicker([(7, 7)])
    assert game.grid[(7, 7)] == game.mine

    game.flag_tile((0, 0))
    view = game.player_view()
    assert view[(0, 0)] == game.flag
    assert np.isnan(view[(7, 7)])

    game.flag_tile((7, 7))
    view = game.player_view()
    assert view[(7, 7)] == game.flag

    game.sweep_tile((7, 7))
    game.clear_swept_flags()
    view = game.player_view()
    assert view[(7, 7)] == game.exploded
    assert game.lost is True


def test_sweep_tile():
    """
    This tests checks the sweep_tile functionality by sweeping
    some tiles on a known gameboard. It also implicity tests
    sum_adjacent_mines quite extensively, so right now that
    function doesn't have its own unit test.
    """
    grid = [[9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 10, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 10, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 10, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9, 9, 9]]
    grid = np.array(grid)

    locations = [(1, 6),
                 (3, 1),
                 (5, 1)]

    game = MineClicker(locations)
    # another test of the class initialisation
    assert np.array_equal(grid, game.grid)
    sweep_circle = [(0, 5),
                    (0, 6),
                    (0, 7),
                    (1, 7),
                    (2, 7),
                    (2, 6),
                    (2, 5),
                    (1, 5)]

    for location in sweep_circle:
        game.sweep_tile(location)
        assert game.grid[location] == 1
    game.sweep_tile((4, 1))
    assert game.grid[(4, 1)] == 2
    assert game.lost is False
    assert game.won is False
    game.sweep_tile(locations[0])
    assert game.lost is True
    assert game.won is False


testdata = (
            (
             ([9, 11],
              [10, 2]),
             False, True
            ),
            (
             ([10, 1],
              [1, 1]),
             True, False
            ),
            (
             ([9, 1],
              [10, 1]),
             False, False
            ),
            (
             ([1, 1],
              [1, 11]),
             False, True
            )
            )
@pytest.mark.parametrize("grid, won, lost", testdata)
def test_check_game_state(grid, won, lost):
    """
    This test checks check_game_state by verifying the the won/lost flags
    that check_game_state controls using minature gameboards of known win/loss
    condition
    """
    game = MineClicker()
    game.grid = np.array(grid)
    game.check_game_state()
    assert game.won is won
    assert game.lost is lost
