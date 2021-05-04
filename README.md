# Snarl

Snarl is a text based dungeon crawler developed for CS4500: Software Dev @ Northeastern.

## Local Player Guide

### Usage

Run `./localSnarl`. The following arguments are optional:
* `--levels FILENAME` where FILENAME is the name of a file containing JSON level specifications (see description below). The default file is snarl.levels.

* `--players N` where `N` is the number of players. If your local implementation only sensibly supports a single player, and the given N is greater than 1, print an error message saying so and exit. Default is 1.

* `--start N` where `N` is the level to start from. If `N` is greater than the number of available levels, the behavior is undefined. Default is 1.

* `--observe` by default, only the players’ view should be presented. If this option is given, an observer view (the full level) should be presented in addition to or instead of the player view. Note: if you would like, you **can** choose to observe a game with multiple players.

### Play Guide

Note:
The game **does not** create an extra screen for the GUI. Everything is displayed in the terminal.

The game uses an (x,y) coordinate system when providing coordinates to the player.

#### Setup
After running `./localSnarl` the game will prompt each player and observer for their name.
Type in a name, and press enter.

Next, the program will ask each player whether they want to start the game. Type y and press enter.

#### Gameplay

During gameplay, the game will render the player's/observer's views sequentially.
The view consists of a map of the level, and a table of state information.

##### Player Actions
When it is a player's turn, they will get a list of moves they can make. The player must type the number of the move they want to make, and press enter. The numbers for each move are listed in the table.

Alternatively, the player can provide a 1-2 character string containing the letters w,a,s, or d and then press enter.
The program will then interpret this string as one of the following moves. The mappings are as follows:
* w: up
* a: left
* s: down
* d: right

To move to the topleft location, a human would type 'we' then enter. To move to a position two tiles to the left, a human would type 'aa' then enter.

To end the game prematurely type ctrl-D when prompted for a move to close STDIN and exit the game.

##### Observer Actions
After each turn, the observer will get a view of the game. They must press enter in order to proceed.

#### Ending

When the game is over, a game over screen is shown. It indicates whether the players won/lost, and each player's rank. Players are ranked based on the number of exits traveled to, and ties are broken by the number of keys found.
