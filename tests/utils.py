import sys
import json

def read_user_input():
    """
    Reads from STDIN
    returns a JSON-like list
    """
    string_input = sys.stdin.read()
    json_input = None
    decoder = json.JSONDecoder()

    json_input, end_index = decoder.raw_decode(string_input)

    return json_input

def print_json(json_like_object):
    """
    Prints a JSON like object as a JSON string
    to STDOUT
    """
    print(json.dumps(json_like_object))

def swap_level(json_level):
    """
    Swaps the coordinates in the json level representation
    """

    for room in json_level["rooms"]:
        room["origin"] = room["origin"][::-1]

    for item in json_level.get("objects", []):
        item["position"] = item["position"][::-1]

    for hallway in json_level.get("hallways", []):
        hallway["from"] = hallway["from"][::-1]
        hallway["to"] = hallway["to"][::-1]
        hallway["waypoints"] = [x[::-1] for x in hallway["waypoints"]]

    return json_level