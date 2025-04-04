from risk.ai import AI
from risk.ai.better import BetterAI
from risk.player import Player

from risk.game import Game
from risk.territory import Territory, Area

import json

def json_to_world(game: Game, j: dict, players: list[Player]):
    """
    Take a JSON dictionary and edit the game file
    """
    # with open(filename) as file:
    #     data = dict(json.load(file))

    for territory_id, territory_data in j.items():
        t: Territory = game.world.territory(territory_id)
        t.owner = players[territory_data["owner"]]
        t.forces = territory_data["troops"]


def simulate_turn(j: dict):
    game = Game(curses=False)

    # Link our AI
    game.add_player("The Agent", BetterAI)
    game.add_player("Player 1", AI)
    game.add_player("Player 2", AI)
    game.add_player("Player 3", AI)
    game.add_player("Player 4", AI)
    game.turn_order = list(game.players)

    # TODO: Return each move the AI did

    # Put the json data into world
    json_to_world(game, j, list(game.players.values()))

    # Now we copy-paste the turn code to see what the Agent would do
    game.player.ai.start()
    
    # Reinforcement phase
    choices = game.player.ai.reinforce(game.player.reinforcements)
    assert sum(choices.values()) == game.player.reinforcements
    for tt, ff in choices.items():
        t = game.world.territory(tt)
        f = int(ff)
        if t is None:
            print("reinforce invalid territory %s", tt)
            continue
        if t.owner != game.player:
            print("reinforce unowned territory %s", t.name)
            continue
        if f < 0:
            print("reinforce invalid count %s", f)
            continue
        t.forces += f
        game.event(
            ("reinforce", game.player, t, f),
            territory=[t],
            player=[game.player.name],
        )

    # Attack phase
    for src, target, attack, move in game.player.ai.attack():
        st = game.world.territory(src)
        tt = game.world.territory(target)

        if st is None:
            game.aiwarn("attack invalid src %s", src)
            continue
        if tt is None:
            game.aiwarn("attack invalid target %s", target)
            continue
        if st.owner != game.player:
            game.aiwarn("attack unowned src %s", st.name)
            continue
        if tt.owner == game.player:
            game.aiwarn("attack owned target %s", tt.name)
            continue
        if tt not in st.connect:
            game.aiwarn("attack unconnected %s %s", st.name, tt.name)
            continue

        initial_forces = (st.forces, tt.forces)
        opponent = tt.owner
        victory = game.combat(st, tt, attack, move)
        final_forces = (st.forces, tt.forces)
        game.event(
            (
                "conquer" if victory else "defeat",
                game.player,
                opponent,
                st,
                tt,
                initial_forces,
                final_forces,
            ),
            territory=[st, tt],
            player=[game.player.name, tt.owner.name],
        )

    # Movement phase
    freemove = game.player.ai.freemove()
    # freemoves.extend([self.player.ai.freemove()])

    if freemove:
        src, target, count = freemove
        st = game.world.territory(src)
        tt = game.world.territory(target)
        f = int(count)
        valid = True
        if st is None:
            game.aiwarn("freemove invalid src %s", src)
            valid = False
        if tt is None:
            game.aiwarn("freemove invalid target %s", target)
            valid = False
        if st.owner != game.player:
            game.aiwarn("freemove unowned src %s", st.name)
            valid = False
        if tt.owner != game.player:
            game.aiwarn("freemove unowned target %s", tt.name)
            valid = False
        if not 0 <= f < st.forces:
            game.aiwarn("freemove invalid count %s", f)
            valid = False
        if valid:
            st.forces -= count
            tt.forces += count
            game.event(
                ("move", game.player, st, tt, count),
                territory=[st, tt],
                player=[game.player.name],
            )

    game.turn += 1

    out = {}
    for territory in game.world.territories.values():
        out[territory.name] = {
            "owner": list(game.players.values()).index(territory.owner),
            "troops": territory.forces,
        }

    return json.dumps(out)
