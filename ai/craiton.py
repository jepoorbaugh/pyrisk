from ai import AI
from ai.stupid import StupidAI

from territory import Territory

from game import Game
from player import Player

from copy import deepcopy

import collections
import random


class CrAItonAI(AI):
    """
    CrAItonAI: Uses MCTS to get the best possible next move.
    """

    def start(self):
        self.monte_carlo_sims =5

    def initial_placement(self, empty, remaining):
        if empty:
            return random.choice(empty)
        else:
            t = random.choice(list(self.player.territories))
            return t

    def reinforce(self, available):
        border = [t for t in self.player.territories if t.border]
        result = collections.defaultdict(int)
        for i in range(available):
            t = random.choice(border)
            result[t] += 1
        return result

    def attack(self):
        best_move = None
        best_score = -100000

        move = ()
        continue_attacks = True
        while continue_attacks:
            for src, dest in self.get_possible_attacks():
                attack_strat = lambda atk, deff: self.simulate(atk, deff)[0] > 0.5
                score = 0
                for i in range(self.monte_carlo_sims):
                    # Create a copy of the game to run the simulation on
                    game = self.create_game_copy()

                    turn_order = []
                    for p in self.game.turn_order:
                        turn_order.append(p)

                    game.turn = self.game.turn
                    game.turn_order = turn_order

                    if src != None and dest != None:
                        move = (
                            game.world.territory(src),
                            game.world.territory(dest),
                            attack_strat,
                            None,
                        )

                        # Make move
                        game.attack(
                            game.players[self.player.name],
                            [move],
                        )
                    else:
                        move = None

                    winner = game.play(
                        turn_order=turn_order, randomize_turn_order=False
                    )

                    if self.player.name == winner:
                        score += 1
                    else:
                        score -= 1
                # print("Round Score: ", score)

                # if our score is better than the current best score, store both
                if score > best_score:
                    best_move = move
                    best_score = score
            if best_move != None:
                yield best_move
            else:
                continue_attacks = False

    def freemove(self):
        pass

    def create_game_copy(self):
        copy_game: Game = Game(curses=False)
        # copy_game.world = deepcopy(self.game.world)

        for p in list(self.game.players):
            copy_game.add_player(p, StupidAI)

        # Fix copy_game.world's territories to have the correct owners
        for name, territory in copy_game.world.territories.items():
            copy_game.world.territory(name).owner = copy_game.players[
                self.world.territory(name).owner.name
            ]
            copy_game.world.territory(name).forces = self.world.territory(name).forces

            # print(copy_game.world.territory(name), "\t", copy_game.world.territory(name).owner, "\t",copy_game.world.territory(name).forces)

        # print(f"Real Turn Order: {self.game.turn_order}")

        # copy_game.turn_order = self.game.turn_order
        copy_game.turn = self.game.turn
        return copy_game

    def get_border(self):
        # border_territories = set(
        #     t if t.border else None for t in self.player.territories
        # )
        # border_territories.remove(None)
        return set(t for t in self.player.territories if t.border)

    def get_possible_attacks(self):
        """Gets all possible attacks for the current board state
        Attacks are represented as tuples in the for (`src`, `dest`)
        """
        attacks = [(None, None)]
        for src in self.get_border():
            for dest in src.connect:
                if dest.owner != self.player and src.forces > 1:
                    attacks.append((src.name, dest.name))
        
        return attacks
