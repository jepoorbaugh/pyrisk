from ai.craiton import CrAItonAI
import json
from territory import Territory

from game import Game
from player import Player

from copy import deepcopy


def json_to_world(game: Game, j: dict, players: list[Player]):
    """
    Take a JSON dictionary and edit the game object
    """
    for territory_id, territory_data in j.items():
        t: Territory = game.world.territory(territory_id)
        t.owner = players[territory_data["owner"]]
        t.forces = territory_data["troops"]


g = Game(curses=False)
players = [CrAItonAI, CrAItonAI, CrAItonAI, CrAItonAI, CrAItonAI]
for i in range(len(players)):
    g.add_player(f"Player {i + 1}", players[i])
    g.players[f"Player {i + 1}"].ai.start()

g.turn = 0
g.turn_order = list(g.players.keys())

with open("world.json") as file:
    json_to_world(g, json.load(file), list(g.players.values()))

print(g.world.territories["Alaska"].owner)

print(list(g.players["Player 3"].ai.attack()))
