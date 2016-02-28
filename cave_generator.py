"""
Generates caves with a cellular automata method and displays them on the
terminal with curses.
"""
import numpy as np
import curses
import time
from ipdb import set_trace as debug  # NOQA

WALL = 1
ROOM = 0


class CA():

    def __init__(self, xdim, ydim, init_wallfraction=0.6):
        self.xdim = xdim
        self.ydim = ydim
        self.cave = None

        self.cave = self.makecave(init_wallfraction)

        # Keep record of states; initialize with the first, random cave.
        self.states = []
        self.states.append(self.cave)

    def makecave(self, wallfrac):
        """
        Random cave of 0s and 1s
        """
        # Initial distribution of walls and room
        cave = np.random.random_sample((self.xdim, self.ydim))

        # Allocate walls and rooms
        walls = cave <= wallfrac
        rooms = cave > wallfrac
        cave[walls] = WALL
        cave[rooms] = ROOM

        # Set up edges
        cave[0, :] = WALL
        cave[-1, :] = WALL
        cave[:, 0] = WALL
        cave[:, -1] = WALL

        return cave

    def neighbors(self, x, y):
        """
        Array of neighbor states
        """

        return np.array([self.cave[x - 1, y],
                         self.cave[x - 1, y + 1],
                         self.cave[x - 1, y - 1],
                         self.cave[x, y + 1],
                         self.cave[x, y - 1],
                         self.cave[x + 1, y],
                         self.cave[x + 1, y + 1],
                         self.cave[x + 1, y - 1]])

    def is_WALL(self, x, y):
        if self.cave[x, y] == WALL:
            return True
        else:
            return False

    def is_ROOM(self, x, y):
        if self.cave[x, y] == ROOM:
            return True
        else:
            return False

    def nr_neighbor_WALLS(self, x, y):
        return sum(self.neighbors(x, y))

    def rule_4_5(self, x, y):

        nr_neighbor_WALLS = self.nr_neighbor_WALLS(x, y)

        if self.is_WALL(x, y) and nr_neighbor_WALLS >= 4:
            return WALL

        elif self.is_ROOM(x, y) and nr_neighbor_WALLS >= 5:
            return WALL

        else:
            return ROOM

    def timestep(self):
        # Copy previous state
        next_state = np.copy(self.cave[:])

        for x in range(1, self.xdim - 1):
            for y in range(1, self.ydim - 1):

                next_state[x, y] = self.rule_4_5(x, y)

        self.cave = next_state

        self.savecave()

    def savecave(self):

        self.states.append(self.cave)


def cave2string(cave):

    xdim, ydim = cave.shape

    image = ''
    for y in range(ydim):
        row = []
        for x in range(xdim):
            value = cave[x, y]
            if value == WALL:
                row.append('#')
            elif value == ROOM:
                row.append(' ')
            else:
                print('how did you get here?')
                1 / 0

        # add row to image
        image += ''.join(row) + '\n'

    return image


def main():

    cavesize = 40
    nr_steps = 15

    myCA = CA(cavesize, cavesize, init_wallfraction=0.45)

    # calculate caves
    for t in range(nr_steps):
        myCA.timestep()

    # show output
    mywindow = curses.initscr()
    for nr, cave in enumerate(myCA.states):
        mywindow.addstr(0, 0, cave2string(cave) + '\nIteration nr {0}'.format(nr))
        mywindow.refresh()
        time.sleep(0.4)
    curses.endwin()

    # how many iterations are needed to coverge?
    converged = False
    previous_iteration = myCA.states[0]
    for nr, cave in enumerate(myCA.states[1:], start=1):
        if np.array_equal(previous_iteration, cave):
            print("Coverged after {0} iterations".format(nr))
            converged = True
            break
        else:
            previous_iteration = cave

    if not converged:
        print('Not enough iterations to converge')

if __name__ == '__main__':
    main()
