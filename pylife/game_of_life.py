from lib import automata
import numpy as np
from typing import Union, Iterable


class GameOfLife:
    def __init__(self, grid: Union[np.ndarray, Iterable]=None):
        if grid:
            self._board = np.array(grid, dtype=np.float)
        else:
            self._board = None
        self.k = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.float)    # The neighborhood kernel.

    def tick(self, wrap_around=False):
        if self._board:
            return automata.next_step(self._board, k=self.k, wrap_around=wrap_around)

    @property
    def rows(self):
        return self._board.shape[0]

    @property
    def cols(self):
        return self._board.shape[1]

    @property
    def alive(self):
        return np.sum(self._board)

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, arr):
        self._board = np.array(arr, dtype=np.float)
