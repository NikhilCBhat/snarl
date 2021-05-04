# Milestone 6 - Refactoring Report

**Team members:**
Nikhil Bhat and Karmen Lu

**Github team/repo:**
https://github.ccs.neu.edu/CS4500-S21/Eglar

## Plan

For this milestone we plan to:
1. Create a `models/` folder containing `level/`, `occupants.py`, and `states.py`.
2. Improve our documentation
3. Update ambiguous variable, field, and method names.
4. Evaluate the merits of swapping from an (x,y) --> (row, col) coordinate system.

## Changes

During this week we made a handful of minor updates. We created a `models/` folder to be consistent with our `views/` and `controllers/` folder, that contains our `level/`, `occupants.py` and `states.py` files. Also, we updated the imports in testing files that were affected by this restructuring.

We improved our documentation in several places. One example would be in  `get_adjacent_tiles` where we specified that the method returns a list of location tuples rather than a list of tiles.

We also renamed the TileConfig class to FloorPlan, and removed a couple of magic strings including the strings “key” and “exit” for items, and the string "\033c\033[3J" used to clear the screen.

We also resolved a few small bugs, including the `get_level_dimensions` method in the `LevelBuilder`.

We evaluated whether to swap to a different coordinate system, and the results of that are in the `swap` branch. We decided to not move forward with this swap because given how so much of the project has been completed, we deemed that it would not make sense to refactor so much of our internal representation in order to satisfy the JSON formatting. We have useful methods such as `Level.get_tile` which abstracts away the coordinate system. Additionally, our `LevelBuilder` class has methods that handle taking input from JSON, and our test harnesses, handle swapping the input.
Our `Level`, `State`, and `FloorPlans` have methods to create JSON objects from their representation which satisfy the output coordinate system. Also, if the coordinate system in the test harness changed to x,y all of our work for this refactoring would be wasted.

Finally, we moved some code from our test harness to either a `utils.py` file or the `LevelBuilder`.

## Future Work

We were unable to figure out a better name for `GameState.__evaluate_game_state` but recognize that the function name is a bit ambiguous. If we think of a better name going forward, we will update the code to reflect that.

## Conclusion

The refactor week was a great way to take a breather after the last couple of assignments. We did not make any major changes to our code, as after evaluating our codebase we found that there were no pressing issues. We had spent considerable effort in previous milestones updating our code as issues came up, as a result, there wasn’t a _ton_ of tech debt.


