from logging import Logger
from typing import Dict, Self

import constants
from player import Player

class Game:
    # TODO: actual interface
    def __init__(self, l: Logger) -> None:
        self.logger = l
        self.players: Dict[str,Player] = {}
        self.current_player = None
        
    def to_file(self, filename: str, next_player: str) -> None:
        with open(filename, 'w') as f:
            f.write(f'Next player: {next_player}\n')
            for p in self.players.values():
                f.write(p.serialize()+'\n')
                
    def add_player_by_name(self, player_name: str) -> None:
        self.players[player_name] = Player(player_name, self.logger)
        
    def add_player(self, player: Player) -> None:
        self.players[player.name] = player
                
    @classmethod
    def from_file(cls, filename: str, l: Logger) -> Self:
        g = cls(l)
        with open(filename) as f:
            lines = f.readlines()
            for line in lines[1:]:
                g.add_player(Player.deserialize(line[:-1],l))
        return g
