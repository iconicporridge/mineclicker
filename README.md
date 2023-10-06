# Sam Henderson's mineclicker

Hello and welcome to this python minesweeper copy. You can just play game in your terminal or use the MineClicker class to help build your own game.

# Install

Once you've got hold of this project, install it like any other python package. I would recommend using a virtual environment, for example [venv](https://docs.python.org/3/library/venv.html) or [conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment).

Once you have (or haven't) setup an environment, navigate to the folder you have downloaded `mineclicker` to. Then type:

```
pip install ./mineclicker
```

or

```
pip install .\mineclicker
```

depending on how you (and your operating system) like your slashes.

# Testing

Before you play or use mineclicker, test the installation works as intended. Navigate to inside the `mineclicker` folder and run:

```
pytest
```

For more information on pytest flags and options, go to the [pytest documentation](https://docs.pytest.org/en/7.1.x/index.html).

If the tests fail, it might be because your version of python or numpy is from the far future! This project was last tested with python 3.11 and numpy 1.25.


# Playing mineclicker

To play a cli version of `mineclicker` type:

```
python -m mineclicker
```

You can also supply mine locations like:

```
python -m mineclicker 2,3 4,5 ...
```

# Using the MineClicker class

You can use the MineClicker class to help create your own minesweeper type game. In your project, import the class like:

```
from mineclicker.lib import MineClicker
```

you can then instance the class and use its functions like:

```
game = MineClicker()
game.check_game_state()
```

Look at `src/mineclicker/lib.py` for the MineClicker class documentation.

