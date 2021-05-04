# Hit Point & Combat System

## Implementation Plan

### Ensuring Backwards Compatibility
Hit-point management will be baked into the model components which already exist in our Snarl design. Previously, life/death was tracked by a single boolean field: `is_alive`. We made use of the python `@property` decorator to continue the of use this field, despite not making an actual unique field of our class. We added a `health` field to our class, and the `is_alive` flag was `True` when `health` is greater than zero and holding the `False` value when `health` is less than or equal to zero. Negative/Zero health indicates that a player is not alive.

### Combat Implementation
An occupant attacks by selecting an occupied tile during their move/turn. The attack will deduct points from the victim occupant. If the victim is slain, the attacker will be placed at the victim's former location. If the victim is alive after the hit, the attacker will stay in place. Selecting a tile that is uninhabited by other occupants results in a normal/standard move.

- Previously, the `expel` method only applied to `Player` occupants. To support combat, we moved `expel` up to the shared `Occupant` class.
- We use double dispatch between the `Player` and `Adversary` types in order to handle interactions. The `interact_with_occupant` method is part of the `Occupant` interface as are `interact_with_adversary` and `interact_with_player`. A `Player`'s `interact_with_occupant(occupant)` method calls `occupant.interact_with_player(self)` and adversaries call `occupant.interact_with_adversary(self)`.
- Also, we added two methods to support health depletion and restoration. `receive_attack` is called by the victim of an attack to perform a health point deduction and possibly an explusion. `reset_health` is called at the start of each level, when all occupants of the level are restored to a start state.

## Occupant Start Health & Hit Strengths

### Player

Players start with 50 health points at the start of each level. Hits/interactions with adversaries result in a point deduction
dependent on the adversary type. Players have a hit strength of 15.

### Ghost

Ghosts have little-to-no influence on the material world. Ghost have a hit strength of 5, as a result of a good scare. Ghosts start with 30 health points.

### Zombie

Zombies eat players. Zombies can't gobble players up in one bite. An interaction with a zombie results in a 10 point deduction. Zombies start with 55 health points.

## Protocol Extensions

Player updates now have a `health` key which has an integer representing their current health.