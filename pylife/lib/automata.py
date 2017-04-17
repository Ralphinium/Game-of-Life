from convolution import int_fft_convolve
import numpy as np


def next_step(state: np.ndarray, rule='B3/S23', k: np.ndarray = None, wrap_around=False) -> np.ndarray:
    """
    Given the current state of the board and the rules, compute for the next state of the board.
    
    Rules are strings of the form "By/Sx" where x and y are a sequence of distinct digits between 0 and 8, in 
    numerical order. If `d` is in `y` then a dead cell with `d` live neighbors becomes alive in the next step. A `d` in
    `x` means a live cell with `d` live neighbors stays alive in the next step.
    :param state: The current state of the board. A 2D matrix of 0s and 1s where 0 denotes a dead cell and 1 denotes a 
        live cell.
    :param rule: A string that denotes the rules for the lives of the cells. 
    :param k: The kernel or the neighborhood that the rules will check for. For Life-like automata, this is
        [1 1 1]
        [1 0 1]
        [1 1 1]
    :param wrap_around: Boundary checking. If True, then we treat the board as if it wraps around itself. 
    :return: The next state of the board.
    """
    # If no k is given, assume Moore neighborhood.
    if k is None:
        k = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

    neighbors = int_fft_convolve(state, k, wrap_around)  # Calculate the number of live neighbors.
    assert neighbors.shape == state.shape

    born_rule = [int(i) for i in rule.split('/')[0].replace('B', '')]
    survive_rule = [int(i) for i in rule.split('/')[1].replace('S', '')]

    next_state = np.zeros(state.shape)

    for i in born_rule:
        next_state[np.where((neighbors == i) & (state == 0))] = 1

    for i in survive_rule:
        next_state[np.where((neighbors == i) & (state == 1))] = 1

    return next_state

