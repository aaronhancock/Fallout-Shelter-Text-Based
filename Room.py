"""Module containing Room class."""

from general_funcs import print_line
from Item import Item


class Room(object):
    """Room class."""

    def __init__(self, name, player):
        """Room class constructor.

        Arguments:
        name -- name of room
        player -- player object
        """
        self.name = name
        self.assigned = ''
        self.level = 1
        self.risk = False
        self.broken = False
        self.power_available = "On"
        self.can_produce = False
        self.assigned_limit = 0
        self.power_usage = 0
        self.components = []

        room_config = {
            "living": {
                "components": ["wood", "wood", "wood", "wood"],
                "power_usage": 5
            },
            "generator": {
                "risk": 2,
                "can_produce": True,
                "components": ["steel", "steel", "steel", "steel"],
                "assigned_limit": 3
            },
            "storage": {
                "components": ["steel", "steel"],
                "power_usage": 1
            },
            "kitchen": {
                "risk": 1,
                "can_produce": True,
                "assigned_limit": 3,
                "components": ["wood", "wood", "wood"],
                "power_usage": 10
            },
            "trader": {
                "assigned_limit": 1,
                "components": ["wood", "wood", "steel", "steel", "wood"],
                "power_usage": 2
            },
            "water works": {
                "risk": 2,
                "can_produce": True,
                "assigned_limit": 3,
                "components": ["wood", "wood", "steel"],
                "power_usage": 10
            },
            "radio": {
                "assigned_limit": 2,
                "components": ["wood", "wood", "steel", "steel", "wood"],
                "power_usage": 15
            }
        }

        if self.name in room_config:
            config = room_config[self.name]
            self.risk = config.get("risk", False)
            self.can_produce = config.get("can_produce", False)
            self.components = config.get("components", [])
            self.assigned_limit = config.get("assigned_limit", 0)
            self.power_usage = config.get("power_usage", 0)
        else:
            print_line("Unknown room type. Please check the configuration.")

        if self.can_produce:
            self.production = 0
            self.can_rush = True
            self.rushed = False
        else:
            self.can_rush = False

    def __str__(self):
        """String representation of object.

        Returns:
        self.name -- eg. "Living Room"
        """
        return "{}{} Room".format(self.name[0].upper(), self.name[1:])

    def rush(self):
        """Rush building of Room."""
        self.rushed = True
        self.risk += 5
        print_line(self.name, " has been rushed!")

    def fix(self):
        """Repair room if damaged."""
        pass

    def update_production(self, player, people):
        """Calculate production value of Room.

        Arguments:
        player -- player object
        people -- list of all people in the game
        """
        if self.broken:
            production = 0
            print_line(self.name, "is broken and needs to be fixed.")
        else:
            production = 0
            production_config = {
                "generator": {
                    "attribute": "strength",
                    "base_value": 10,
                    "player_bonus": player.electrician,
                    "bonus_multiplier": 0.05
                },
                "kitchen": {
                    "attribute": "intelligence",
                    "base_value": 10,
                    "player_bonus": player.cooking,
                    "bonus_multiplier": 0.05
                },
                "water works": {
                    "attribute": "perception",
                    "base_value": 10,
                    "player_bonus": player.cooking,
                    "bonus_multiplier": 0.05
                },
                "radio": {
                    "attribute": "charisma",
                    "base_value": 10,
                    "player_bonus": player.inspiration,
                    "bonus_multiplier": 0.05
                }
            }

            if self.name in production_config:
                config = production_config[self.name]
                for person_index in str(self.assigned):
                    if person_index == '1':
                        attribute_value = getattr(people[int(person_index)], config["attribute"])
                        production += attribute_value * config["base_value"]
                if config["player_bonus"] > 0:
                    production *= 1 + (config["player_bonus"] * config["bonus_multiplier"])
            else:
                print_line("Unknown room type for production calculation.")

            if player.inspiration > 0:
                production *= 1 + (player.inspiration * 0.03)
            if self.can_rush and self.rushed:
                production *= 2

        return production

    def count_assigned(self):
        """Count inhabitants assigned to Room."""
        return str(self.assigned).count('1')

    def see_assigned(self, people):
        """Print names of inhabitants assigned to Room.

        Arguments:
        people -- list of all people in the game
        """
        count = 0
        for x in str(self.assigned):
            if x == '1':
                person = people[count]
                print_line("      ", person.name, person.surname)
            count += 1

    def count_component(self, component):
        """Count components required to build Room.

        Arguments:
        component -- component to count

        Returns:
        int -- amount of component required to build Room
        """
        return self.components.count(str(component))

    def use_power(self):
        """Consume player's power."""
        for _ in range(self.power_usage):
            Item('watt').destroy("player")