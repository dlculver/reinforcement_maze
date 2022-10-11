# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


## reinforcement learning for solving mazes

from maze import QMaze

## constants

visited_mark = 0.8 ## cells visited will be painted by gray 0.8
rat_mark = 0.5 ## the cell occupied by the rat will be painted by gray 0.5
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

## action dictionary

actions_dict = {
    LEFT : 'left',
    RIGHT : 'right',
    UP : 'up',
    DOWN : 'down',
}

num_actions = len(actions_dict)

epsilon = 0.1


