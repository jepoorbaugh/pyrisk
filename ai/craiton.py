from ai import AI
from ai.stupid import StupidAI

from game import Game

import collections
import random


# from multiprocessing.pool import ThreadPool as Pool
# from multiprocessing import Pool
from pathos.pools import ProcessPool


class CrAItonAI(AI):
    """
    CrAItonAI: Uses MCTS to get the best possible next move.
    """

    def start(self):
        self.area_priority = list(self.world.areas)
        random.shuffle(self.area_priority)

        self.monte_carlo_sims = 10
        self.num_processes = 5

    def priority(self):
        priority = sorted(
            [t for t in self.player.territories if t.border],
            key=lambda x: self.area_priority.index(x.area.name),
        )
        priority = [t for t in priority if t.area == priority[0].area]
        return priority if priority else list(self.player.territories)

    def initial_placement(self, empty, available):
        if empty:
            empty = sorted(empty, key=lambda x: self.area_priority.index(x.area.name))
            return empty[0]
        else:
            return random.choice(self.priority())

    def reinforce(self, available):
        border = [t for t in self.player.territories if t.border]
        result = collections.defaultdict(int)
        for i in range(available):
            t = random.choice(border)
            result[t] += 1
        return result

    def attack(self):
        continue_attacks = True
        while continue_attacks:
            best_move = None
            # best_score = -100000
            # move = ()

            all_attacks = list(self.get_possible_attacks())
            attack_strat = lambda atk, deff: self.simulate(atk, deff)[0] > 0.5
            # with Pool() as p:
            #     # print("We got here")
            #     scores = p.starmap(self.evaluate_attack, all_attacks)

            pool = ProcessPool()
            print(all_attacks)
            scores = pool.map(self.evaluate_attack, all_attacks)

            # scores = list(map(self.evaluate_attack, all_attacks))

            best_move = all_attacks[scores.index(max(scores))]
            # for attack in self.get_possible_attacks():
            #     score = self.evaluate_attack(attack)
            #     # if our score is better than the current best score, store both
            #     if score > best_score:
            #         best_move = move
            #         best_score = score
            if best_move != None:
                yield (best_move[0], best_move[1], attack_strat, None)
            else:
                continue_attacks = False

    def evaluate_attack(self, attack_tuple):
        src, dest = attack_tuple
        # print(type(src), type(dest), type(tup))
        # print(f"Evaluating attack from {src} on {dest}")
        if (
            not src == None
            and not dest == None
            and self.simulate(
                self.world.territory(src).forces,
                self.world.territory(dest).forces,
            )[0]
            < 0.5
        ):
            return 0

        attack_strat = lambda atk, deff: self.simulate(atk, deff)[0] > 0.5

        score = 0
        for i in range(self.monte_carlo_sims):
            # Create a copy of the game to run the simulation on
            copy_game = self.create_game_copy()

            if src != None and dest != None:
                move = (
                    src,
                    dest,
                    attack_strat,
                    None,
                )

                # Make move
                copy_game.attack(
                    copy_game.players[self.player.name],
                    move,
                )
            else:
                move = None

            winner = copy_game.play(
                turn_order=copy_game.turn_order, randomize_turn_order=False
            )

            if self.player.name == winner:
                score += 1
            else:
                score -= 1

        # print(f"Attack {attack_tuple} Score: {score}")
        return score

    def freemove(self):
        srcs = sorted(
            [t for t in self.player.territories if not t.border], key=lambda x: x.forces
        )
        if srcs:
            src = srcs[-1]
            n = src.forces - 1
            return (src, self.priority()[0], n)
        return None

    def create_game_copy(self):
        copy_game: Game = Game(curses=False, iscopy=True)

        for p in list(self.game.players):
            copy_game.add_player(p, StupidAI)

        # Fix copy_game.world's territories to have the correct owners
        for name, territory in copy_game.world.territories.items():
            copy_game.world.territory(name).owner = copy_game.players[
                self.world.territory(name).owner.name
            ]
            copy_game.world.territory(name).forces = self.world.territory(name).forces

        turn_order = []
        for p in self.game.turn_order:
            turn_order.append(p)
        copy_game.turn = self.game.turn
        copy_game.turn_order = turn_order

        return copy_game

    def get_border(self):
        return set(t for t in self.player.territories if t.border)

    def get_possible_attacks(self):
        """Gets all possible attacks for the current board state
        Attacks are represented as tuples in the for (`src`, `dest`)
        """
        for src in self.get_border():
            for dest in src.connect:
                if dest.owner != src.owner and src.forces > 1:
                    yield (src.name, dest.name)
