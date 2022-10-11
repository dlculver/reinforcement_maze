## class QMaze, defining the environment

import numpy as np

## maze is a 2d array consisting of floats between 0.0 and 1.0
## 1.0 corresponds to a free cell and 0.0 corresponds to an occupied cell
## rat = (row, col) and initial rat position is (0,0)

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

class QMaze:
    def __init__(self, maze, rat = (0,0)):
        self._maze = np.array(maze)
        nrows, ncols = self._maze.shape
        self.target = (nrows - 1, ncols - 1)
        self.free_cells = [(r, c) for r in range(nrows) for c in range(ncols) if self._maze[r,c] == 1.0]
        self.occupied_cells = [(r,c) for r in range(nrows) for c in range(ncols) if self._maze[r,c] == 0.0]
        self.free_cells.remove(self.target) ## the target shouldn't be regarded as a free cell

        if self.target in self.occupied_cells:
            raise Exception("The target cannot be an occupied cell.")
        if not rat in self.free_cells:
            raise Exception("The rat must be in an unoccupied cell.")

        self.reset(rat)

## the above initializes the board, we have the method in __init__ and defined below. The purpose of reset() is to
## initialize the actual maze data, i.e. location of the rat, rewards accrued, etc.
    def reset(self, rat):
        self.rat = rat
        self.maze = np.copy(self._maze)
        nrows, ncols = self.maze.shape
        row, col = rat
        self.maze[row, col] = rat_mark
        self.state = (row, col, 'start')
        self.lower_threshold = -0.5*self.maze.size
        self.total_reward = 0
        self.visited = set()

    def update_state(self, action):
        nrows, ncols = self.maze.shape
        rat_row, rat_col, mode = self.state

        if self.maze[rat_row, rat_col] > 0.0:
            self.visited.add((rat_row, rat_col)) ## add cell to set of visited cells

        valid_actions = self.valid_actions()

        if not valid_actions:
            mode = 'blocked'
        elif action in valid_actions:
            mode = 'valid'
            if action == RIGHT:
                rat_col += 1
            if action == LEFT:
                rat_col -= 1
            if action == UP:
                rat_row -= 1
            if action == DOWN:
                rat_row += 1
        else:   ## invalid actions result in now change of the rat's position
            mode = 'invalid'

        ## update the state
        self.state = (rat_row, rat_col, mode)

    ## the following method only outputs the reward for the particular state, we will get the total reward later
    def get_reward(self):
        row, col, mode = self.state
        nrows, ncols = self.maze.shape

        if (row, col) == (nrows-1, ncols-1):
            return 1.0
        if mode == 'blocked':
            return self.lower_threshold - 1 ## if the rat is blocked then it loses
        if (row, col) in self.visited:
            return -0.25
        if mode == 'invalid':
            return -0.75
        if mode == 'valid':
            return -0.04

    ## we want a method for giving us the current status of the game, i.e. has the rat lost

    def get_status(self):
        if self.total_reward < self.lower_threshold:
            return 'lose'
        row, col, mode = self.state
        nrows, ncols = self.maze.shape
        if (row, col) == (nrows-1, ncols-1):
            return 'win'

    ## the following method now uses the previous two, to both update the board and get the total reward

    def act(self, action):
        self.update_state(action)
        reward = self.get_reward()
        self.total_reward += reward
        status = self.get_status()
        envstate = self.observe()
        return envstate, status, reward

    ## the following method outputs the configuration of the maze without any marks (besides the rat and walls)
    def draw_env(self):
        canvas = np.copy(self.maze)
        nrows, ncols = self.maze.shape
        ## clear all visual marks
        for r in range(nrows):
            for c in range(ncols):
                if canvas[r,c] > 0.0:
                    canvas[r,c] == 1.0

        ## draw the rat
        row, col, mode = self.state
        canvas[row,col] = rat_mark
        return canvas

    ## this method returns the ``environment state'' as a 1-dimensional array
    def observe(self):
        canvas = self.draw_env()
        envstate = canvas.reshape((1,-1))
        return envstate


    ## this method is to quickly access whether a particular action is valid or not
    def valid_actions(self, cell = None):
        if cell is None:
            row, col, mode = self.state
        else:
            row, col = cell

        actions = [LEFT, RIGHT, UP, DOWN]
        nrows, ncols = self.maze.shape
        ## the following deals with the boundary of the maze
        if row == 0:
            actions.remove(UP)
        elif row == nrows - 1:
            actions.remove(DOWN)
        elif col == 0:
            actions.remove(LEFT)
        elif col == ncols - 1:
            actions.remove(RIGHT)

        ## the following deals with occupied cells

        if row > 0 and self.maze[row - 1, col] == 0.0:
            actions.remove(UP)
        if row < nrows - 1 and self.maze[row + 1] == 0.0:
            actions.remove(DOWN)
        if col > 0 and self.maze[row, col-1] == 0.0:
            actions.remove(LEFT)
        if col < ncols - 1 and self.maze[row, col + 1] == 0.0:
            actions.remove(RIGHT)

        return actions


