import socket

from src.Adversary.remote_adversary import RemoteAdversary
from src.Player.remote_player import RemotePlayer
from src.Game.models.level.level_builder import LevelBuilder
from src.Game.controllers.game_manager import GameManager
from src.Remote.network_handler import send_msg
import src.Game.constants as constants

class SnarlServer:

    def __init__(self, level_file, max_players, wait, observe, host, port, max_adversaries=5):
        """
        Creates a game server for a networked game of snarl.
        """
        levels = LevelBuilder.create_levels_from_levels_file(level_file)
        self.__game_manager = GameManager(levels, observe, get_observation_confirmation=False)
        self.__timeout = wait
        self.__max_players = max(min(max_players, 4), 1)
        self.__max_adversaries = max_adversaries
        self.__clients = []
        self.__host = host
        self.__port = port

    def launch(self):
        """
        Creates a socket connection for a networked game of snarl.
        Listens for/awaits joins from incoming players/users.
        Starts a new game with registered players.
        """
        print(constants.CLEAR_SCREEN, "Starting the Snarl Server!")
        self.__initalize_socket()
        self.__listen_for_connections()
        self.__game_manager.launch_game()

        print("Game is over, closing the snarl server!")
        for conn in self.__clients:
            conn.close()
        self.__server_socket.close()

    def __initalize_socket(self):
        """
        Creates a socket connection from the specified host and port.
        """
        self.__server_socket = socket.socket()
        self.__server_socket.bind((self.__host, self.__port))
        self.__server_socket.listen()

    def __listen_for_connections(self):
        """
        Awaits connections from incoming players/adversaries
        until maximum player count is reached
        or waiting period for additional joins expires.
        """
        print("Waiting for players...")
        self.__accept_connections(
            lambda conn: self.__game_manager.register_player(RemotePlayer(conn)),
            self.__max_players)

        print("Waiting for adversaries...")
        self.__accept_connections(
            lambda conn: self.__game_manager.register_adversary(RemoteAdversary(conn)),
            self.__max_adversaries + len(self.__clients))

    def __accept_connections(self, registration_function, client_max):
        """
        Awaits connections from incoming players/adversaries until maximum player count is reached
        or waiting period for additional joins expires.
        """
        while len(self.__clients) < client_max:
            try:
                conn, _ = self.__server_socket.accept()
                self.__clients.append(conn)
                send_msg(conn, {"type": constants.WELCOME_MESSAGE,
                    "info": "Welcome to Snarl!\nGroup Name: Eglar\nUnlimited retries."})
                print("Registered a connection")
                registration_function(conn)
                self.__server_socket.settimeout(self.__timeout)
            except socket.timeout:
                break