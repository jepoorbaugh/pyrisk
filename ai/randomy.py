from ai import AI
import random
import collections


class RandomyAI(AI):
    """
    RandomyAI: Plays a completely random game, randomly choosing and reinforcing
    territories, and attacking wherever it can without any considerations of wisdom.
    """

    def initial_placement(self, empty, remaining):
        if empty:
            return random.choice(empty)
        else:
            t = random.choice(list(self.player.territories))
            return t

    def attack(self):
        # Make a list of territories that have opposition nearby
        offensive_territories = []

        for t in self.player.territories:
            for a in t.connect:
                if a.owner != self.player:
                    offensive_territories.append(t)
                    break
        
        # Randomly choose offensive territory
        src_territory = random.choice(offensive_territories)

        # Make a list of territories that can be attacked from the src_territory
        defensive_territories = []

        for t in src_territory.connect:
            if t.owner != self.player:
                defensive_territories.append(t)
        
        # Randomly choose defensive territory
        dst_territory = random.choice(defensive_territories)

        # Yield results
        # NOTE: It also is randomly chosen whether or not the AI keeps attacking
        yield (src_territory, dst_territory, lambda x, y: random.choice([True, False]), None)

    def reinforce(self, available):
        # Make list of border territories
        border = [t for t in self.player.territories if t.border]

        # Instantiate result list so it can be appended to while empty
        result = collections.defaultdict(int)

        # Go through and randomly reinforce the borders troop by troop
        for i in range(available):
            t = random.choice(border)
            result[t] += 1

        # Return reinforcement result
        return result
