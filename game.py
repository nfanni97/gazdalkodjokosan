from logging import Logger
from typing import List, Self

import constants
from player import Player

class Game:
    def __init__(self, l: Logger) -> None:
        self.logger = l
        self.players: List[Player] = []
        
    def to_file(self, filename: str, next_player: str) -> None:
        with open(filename, 'w') as f:
            f.write(f'Next player: {next_player}')
            for p in self.players:
                f.write(p.serialize()+'\n')
                
    def add_player(self, player: Player) -> None:
        self.players.append(player)
                
    @classmethod
    def from_file(cls, filename: str, l: Logger) -> Self:
        g = cls(l)
        with open(filename) as f:
            lines = f.readlines()
            for line in lines[1:]:
                g.add_player(Player.deserialize(line[:-1],l))
        return g
