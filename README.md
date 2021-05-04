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

## Networked Player Guide

### Usage

#### Snarl Server
Run `./snarlServer` to start the server. The following arguments are optional:
* `--levels FILE` where FILE is the name of a file containing JSON level specifications (see description below). The default file is snarl.levels.

* `--clients N`, where 1 ≤ N ≤ 4 is the maximum number of clients the server should wait for before starting the game. This option determines max_clients in the protocol specification. Default is 4.

* `--wait N`, where N is the number of seconds to wait for the next client to connect. This option determines reg_timeout. Default is 60.

* `--observe` by default, only the players’ view should be presented. If this option is given, a local observer view (the full level) is presented in the server console.

* `--address IP`, where IP is an IP address on which the server should listen for connections. Default is 127.0.0.1.

* `--port NUM`, where NUM is the port number the server will listen on. Default is 45678

#### Snarl Client
Run `./snarlClient` to start the player client. The following arguments are optional:
* `--address IP`, where IP is an IP address the client should connect to. Default is `127.0.0.1`.

*  `--port NUM`, where NUM is the port number the client should connect to. Default is `45678`

### Play Guide

Note:
The game **does not** create an extra screen for the GUI. Everything is displayed in the terminal.

#### Setup
After running `./snarlClient` the game will prompt each player for their name. If an invalid name is specified, the player will be reprompted until a valid name is specified.
Type in a name, and press enter.

#### Gameplay

During gameplay, the game will render a view to each of the client consoles. The view includes a level map, the current turn number, and the player's current position.

##### Player Actions
When it is a player's turn, the player will be prompted for a move. Then, a player specifies their move and presses enter. It will remain the current player's turn until a valid move is specified by the current player. The current player has unlimited invalid moves and the client console will wait for a valid move to progress the game.

The move can be specified in a set of parentheses: `(row,column)`. For example, `(1,2)` indicates that a player wants to move to the tile at row 1, column 2.

Alternatively, the player can provide a 1-2 character string containing the letters w,a,s, or d and then press enter.
The program will then interpret this string as one of the following moves. The mappings are as follows:
* w: up
* a: left
* s: down
* d: right

To move to the topleft location, a human would type 'we' then enter. To move to a position two tiles to the left, a human would type 'aa' then enter.

To end the game prematurely type ctrl-D when prompted for a move to close STDIN and exit the game.

##### Observe Option
If the observe option is specified, a view of the game will be printed to the server console after each turn.

#### Ending
When a level is over, a player is provided with a table that lists key finders, exit finders, and ejected players.

When the game is over, a game over screen is shown on server and client consoles. It provides a table of player scores: number of times a player has been ejected, number of times a player has exited, and number of keys found by a player. Players are ordered/ranked based on the number of exits traveled to, and ties are broken by the number of keys found.
