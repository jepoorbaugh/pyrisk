from risk.ai import AI
import random
import collections
from risk.territory import Area


class BetterAI(AI):
    """
    BetterAI: Thinks about what it is doing a little more - picks a priority
    continent and priorities holding and reinforcing it.
    """

    def start(self):
        self.area_priority: list[Area] = list(self.world.areas.values())

        def find_area_score(area):
            s = sum((1 if t.owner == self.player else 0) for t in area.territories)
            # print(sum((1 if t.owner == self else 0) for t in area.territories))
            # print(s, area)
            return s

        # stuff = ((1 if t.owner == self else 0) for t in x.territories)
        self.area_priority = sorted(
            self.area_priority,
            key=lambda x: find_area_score(x),
            reverse=True,
        )
        print(self.area_priority)

    def priority(self):
        # Set our priority to the area in which we own the most territories.
        priority = sorted(
            [t for t in self.player.territories if t.border],
            key=lambda x: self.area_priority.index(x.area),
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
        priority = self.priority()
        result = collections.defaultdict(int)
        while available:
            result[random.choice(priority)] += 1
            available -= 1
        return result

    def attack(self):
        for t in self.player.territories:
            if t.forces > 1:
                adjacent = [
                    a
                    for a in t.connect
                    if a.owner != t.owner and t.forces >= a.forces + 3
                ]
                if len(adjacent) == 1:
                    yield (t.name, adjacent[0].name, lambda a, d: a > d, None)
                else:
                    total = sum(a.forces for a in adjacent)
                    for adj in adjacent:
                        yield (
                            t,
                            adj,
                            lambda a, d: a > d + total - adj.forces + 3,
                            lambda a: 1,
                        )

    def freemove(self):
        srcs = sorted(
            [t for t in self.player.territories if not t.border], key=lambda x: x.forces
        )
        if srcs:
            src = srcs[-1]
            n = src.forces - 1
            return (src, self.priority()[0], n)
        return None
