# pyrisk: CrAIton Edition

## Intro

A simple implementation of a variant of the **Risk** board game for python, designed for playing with AIs.

Runs in `python` (2.7 or 3.x) using the `curses` library to display the map (but can be run in pure-console mode).

**NOTE**: For Windows devices install [windows-curses](https://pypi.org/project/windows-curses/) to run with the display map (the normal `curses` library should be pre-installed for Linux and macOS systems).

## Usage

``python pyrisk.py FooAI BarAI*2``

Use `--help` to see more detailed options, such as multi-game running. The AI loader assumes that `SomeAI` translates to a class `SomeAI` inheriting from `AI` in `ai/some.py`.

## Rules

A minimal version of the **Risk** rules are used:

- Players start with `35 - 5*players` armies.
- At the start of the game, territories are chosen one by one until all are claimed, and then the remaining armies may be deployed one at a time to reinforce claimed territories.
- Each turn, players recieve `3 + territories/3` reinforcements, plus a bonus for any complete continents.
- A player may make unlimited attacks per round into adjacent territories (including from freshly-conquered territories).
  - Each combat round, the attacker can attack with up to three armies.
  - Upon victory, a minimum of that combat round's attackers are moved into the target territory.
  - The attacker may cease the attack at the end of any combat round.
  - The defender defends with two armies (unless only one is available).
  - Each attacking and defending army rolls 1d6. The rolls on each side are ordered and compared. The loser of each complete pair is removed, with the defender winning ties.
- At the end of each turn, a player may make one free move
- Victory is achieved by world domination.

## API

Write a new class extending the `AI` class in `ai/__init__.py`. The methods are documented in that file. At a minimum, the following functions need to be implemented:

- `initial_placement(self, empty, remaining)`: Return an empty territory if any are still listed in ``empty``, else an existing territory to reinforce.
- `reinforce(self, available)`: Return a dictionary of territory -> count for the reinforcement step.
- `attack(self)`: Yield `(from, to, attack_strategy, move_strategy)` tuples for each attack you want to make.

The `AI` base class provides objects `game`, `player` and `world` which can be inspected for the current game state. *These are unproxied versions of the main game data structures, so you're trusted not to modify them.*

## CrAIton
For our project we set out to make an AI agent for Risk which somehow utilized Monte Carlo tree search since we had found a [paper](https://www.sto.nato.int/publications/STO%20Meeting%20Proceedings/STO-MP-SAS-OCS-ORA-2020/MP-SAS-OCS-ORA-2020-WCM-01.pdf) on the matter, but because of the complexity of the game we did not want to make everything from scratch. That is why we landed on pyrisk which allowed us to just focus on making the AI agent, but because of the structure of the project it actually made some things we tried to do unrealistic or impossible.

CrAIton is an AI agent for pyrisk that utilizes Monte Carlo tree search for attacking only. To improve efficiency, efforts to simulate games in parrallel for attacking were made, but it was found to be impossible with how Python and pyrisk operate. The `freemove` function was also changed from random to a heuristic. Finally the `start`, `initial_placement`, and `reinforce` functions were copied over from BetterAI because of a mixture of time constraints and lack of reason to change them.

Overall, these changes resulted in an pyrisk AI agent that performs **better** than previous best performing AI agent, BetterAI.
