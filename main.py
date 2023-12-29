import logging
from datetime import datetime
from sys import argv

from game import Game
import utils

# TODO: add tests

if __name__ == '__main__':
    logging.basicConfig(filename=f'{datetime.now():%Y-%B-%d}.log',filemode='w',
                        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    l = logging.getLogger()
    try:
        if len(argv) > 1:
            filename = argv[1]
            g = Game.from_file(filename, l)
        else:
            g = Game(l)
            g.add_player_by_name('Fanni')
            g.add_player_by_name('Dorci')
            g.add_player_by_name('Gabi')
            g.add_player_by_name('Viki')
    except Exception:
        g.to_file(f'{datetime.now():%Y-%B-%d}.game','error')
        raise
    