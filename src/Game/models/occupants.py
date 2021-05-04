import src.Game.constants as constants

class Occupant:

    def __init__(self,
                id,
                tiles_to_filter_out,
                move_distance,
                actor_type,
                visible_distance,
                health,
                hit_strength,
                representation_string,
                level_id=0,
                non_traversable_tiles = {constants.WALL_STRING, constants.VOID_STRING}):

        self.actor_type = actor_type
        self.id = id
        self.current_tile = None
        self.has_exited = False
        self.tiles_to_filter_out = tiles_to_filter_out
        self.move_distance = move_distance
        self.visible_distance = visible_distance
        self.health = health
        self.max_health = health
        self.hit_strength = hit_strength
        self.non_traversable_tiles = non_traversable_tiles
        self.ejections = set()
        self.level_id = level_id
        self.representation_string = representation_string

    @property
    def current_location(self):
        return self.current_tile.location

    @property
    def is_alive(self):
        return self.health > 0

    @property
    def is_active(self):
        return self.is_alive and not self.has_exited

    def reset_health(self):
        self.health = self.max_health

    def move(self, new_tile):
        """
        Moves an occupant to a given tile.
        """
        # Occupant - Occupant interactions
        current_tile_occupant = new_tile.current_occupant
        if current_tile_occupant is None:
            if self.current_tile:
                self.current_tile.current_occupant = None
            new_tile.current_occupant = self
            self.current_tile = new_tile
        else:
            self.interact_with_occupant(current_tile_occupant)

        # Occupant - Item interactions
        self.interact_with_item(new_tile.current_item)

    def expel(self):
        """
        Expels an occupant from the game.
        """
        self.ejections.add(self.level_id)
        self.health = 0
        # Remove occupant from current tile
        if self.current_tile:
            self.current_tile.current_occupant = None

    def receive_attack(self, attacker):
        """
        Updates health and is_alive/life status in response to an attack.
        """
        self.health -= attacker.hit_strength
        if not self.is_alive:
            # expel self
            self.expel()
            # attacker moves to current occupant's former spot
            attacker.current_tile.current_occupant = None
            attacker.current_tile = self.current_tile
            self.current_tile.current_occupant = attacker

    def reset_health(self):
        """
        Resets an occupants health
        """
        self.health = self.max_health

    def interact_with_item(self, item):
        """
        Occupant - Item interaction

        Note: This is unused right now,
        but the stub is here in case
        we want to support more complicated item iteractions
        like potions in the future
        """
        pass

    def interact_with_occupant(self, occupant):
        """
        Occupant - Occupant Interaction
        """
        pass

    def interact_with_player(self, player):
        """
        Occupant - Player Interaction
        """
        pass

    def interact_with_adversary(self, adversary):
        """
        Occupant - Adversary Interaction
        """
        pass

    def to_json(self):
        """
        Creates a JSON representation of an occupant
        """
        return {
            "type": self.actor_type,
            "name": self.id,
            "position": self.current_location[::-1]
        }

    def __eq__(self, other):
        """
        Override equality for Occupant to be based on id
        """
        if isinstance(other, Occupant):
            return self.id == other.id
        return False

    def __str__(self):
        """
        Single char string for representation
        """
        return self.representation_string

class Player(Occupant):

    def __init__(self, id):
        super().__init__(id,
                        {constants.WALL_STRING, constants.VOID_STRING, constants.PLAYER_STRING},
                        constants.PLAYER_MOVE_DISTANCE,
                        constants.PLAYER_ACTOR_TYPE,
                        constants.PLAYER_VISIBLE_DISTANCE,
                        constants.PLAYER_HEALTH,
                        constants.PLAYER_HIT_STRENGTH,
                        constants.PLAYER_STRING)

        self.keys_found = set()
        self.exits = set()
        self.ejections = set()

    def interact_with_occupant(self, occupant):
        occupant.interact_with_player(self)

    def interact_with_adversary(self, adversary):
        self.receive_attack(adversary)

class Adversary(Occupant):

    def __init__(self,
                id,
                tiles_to_filter_out,
                move_distance,
                actor_type,
                level_id,
                health,
                hit_strength,
                representation_string,
                non_traversable_tiles = {constants.WALL_STRING, constants.VOID_STRING}):

        super().__init__(id,
                        tiles_to_filter_out,
                        move_distance,
                        actor_type,
                        -1,
                        health,
                        hit_strength,
                        representation_string,
                        level_id,
                        non_traversable_tiles)

    def interact_with_occupant(self, occupant):
        occupant.interact_with_adversary(self)

    def interact_with_player(self, player):
        self.receive_attack(player)

class Ghost(Adversary):
    def __init__(self, id, level_number=0):
        super().__init__(id,
                        {constants.VOID_STRING, constants.GHOST_STRING, constants.ZOMBIE_STRING},
                        constants.ADVERSARY_MOVE_DISTANCE,
                        constants.GHOST_ACTOR_TYPE,
                        level_number,
                        constants.GHOST_HEALTH,
                        constants.GHOST_HIT_STRENGTH,
                        constants.GHOST_STRING,
                        {constants.VOID_STRING})

class Zombie(Adversary):
    def __init__(self, id, level_number=0):
        super().__init__(id,
                        {constants.VOID_STRING, constants.WALL_STRING, constants.GHOST_STRING,
                                                constants.ZOMBIE_STRING, constants.DOOR_STRING},
                        constants.ADVERSARY_MOVE_DISTANCE,
                        constants.ZOMBIE_ACTOR_TYPE,
                        level_number,
                        constants.ZOMBIE_HEALTH,
                        constants.ZOMBIE_HIT_STRENGTH,
                        constants.ZOMBIE_STRING)
