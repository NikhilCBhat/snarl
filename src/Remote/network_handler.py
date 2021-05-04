import sys
import json
import socket

def send_msg(sock, message):
    """
    Sends a message
    """
    sock.sendall(json.dumps(message).encode())

class NetworkHandler:

    def __init__(self, sock=None, host='localhost', port=8000):
        """
        Sets up a network handler to take care of sending/receiving messages.
        """
        if sock:
            self.__socket = sock
        else:
            self.__socket = socket.socket()
            self.__socket.connect((host, port))
        self.__data = ""

    def send(self, message):
        """
        Writes a specified message to this client's connection to the server.
        """
        send_msg(self.__socket, message)

    def receive(self):
        """
        Reads from this client's socket connection to the server.
        """
        decoder = json.JSONDecoder()
        while True:
            try:
                valid_json, index = decoder.raw_decode(self.__data)
                self.__data = self.__data[index:]
                return valid_json
            except:
                incoming_data = self.__socket.recv(4096).decode()
                if not incoming_data:
                    print("Error: Someone disconnected! :'(")
                    self.close()
                self.__data += incoming_data

    def receive_until(self, condition):
        """
        Continues to receive until a condition is met
        """
        response = None
        while not condition(response):
            response = self.receive()
        return response

    def close(self):
        """
        Closes the socket and exits.
        """
        self.__socket.close()
        sys.exit()