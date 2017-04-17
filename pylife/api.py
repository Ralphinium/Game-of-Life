import game_of_life as life
import zerorpc
import logging


logging.basicConfig(filename="debug.log", level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(0)


class GameOfLifeAPI:
    def __init__(self):
        self.game = life.GameOfLife()
        self.running = False

    def tick(self, arr, wrap_around):
        """
        Returns the next generation for the given board. If there is a game currently running, the given board is 
        ignored. 
        :param arr: The current state of the board. 
        :param wrap_around: Boundary conditions.
        :return: The next state of the board.
        """
        if not self.running:
            logger.debug("New game has started @ tick.")
            self.game.board = arr
            self.running = True
        return self.game.tick(wrap_around)

    @zerorpc.stream
    def run(self, arr, wrap_around):
        """
        Generates a stream of generations, starting from the given board. If there is a game currently running, does
        nothing.
        :param arr: The current state of the board.
        :param wrap_around: Boundary conditions.
        :return: A generator of next states of the board.
        """
        if self.running:
            return
        logger.debug("New game has started @ run.")
        self.running = True
        self.game.board = arr
        while self.running:
            yield self.game.tick(wrap_around)

    def stop(self):
        """
        Stops whatever is currently running.
        """
        logger.debug("Currently running game has been stopped.")
        self.running = False
        return

def main():
    address = 'tcp://127.0.0.1:4242'
    s = zerorpc.Server(GameOfLifeAPI(), heartbeat=None)
    s.bind(address)
    s.run()
    logger.debug("Server has started.")

if __name__ == "__main__":
    main()