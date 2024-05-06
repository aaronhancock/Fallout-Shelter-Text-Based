"""Module containing all Item classes."""

from random import randint
from general_funcs import print_line
import json
from config import ITEMS_FILE


class Item(object):
    """Item class. Only used for on-the-fly cases, not storage."""

    def __init__(self, name):
        """Item constructor.

        Arguments:
        name -- name of item
        """
        self.name = name
        with open(ITEMS_FILE) as f:
            parsed = json.load(f)
            item = parsed.get(self.name)
            if item:
                self.value = item['value']
                self.weight = item['weight']
                self.components = item['components']
                self.rarity = item['rarity']
            else:
                print_line("Unknown item. This is a bug. Please contact the dev.")
        self.scrapped = False

    def count_component(self, component):
        """Count number of components in Item.

        Arguments:
        component -- component to count
        """
        return self.components.count(str(component))

    def scrap(self):
        """Destroy Item and add its components to inventory."""
        global inventory
        print_line(f"{self.name} has been scrapped and these components have been added to your inventory:")
        for item in self.components:
            inventory.append(item)
            print_line(item)

        chance = randint(0, 101)
        if people[0].scrapper * 3 > chance:
            print_line("Your scrapper skill has allowed you to gain more components!")
            for item in self.components:
                inventory.append(item)
        self.scrapped = True
        self.destroy("player")

    def destroy(self, target_inventory):
        """Remove item from inventory.

        Arguments:
        target_inventory -- inventory to remove Item from
        """
        global inventory
        global trader_inventory
        if target_inventory == "player":
            inventory = [x for x in inventory if Item(x).name != self.name]
        elif target_inventory == "trader":
            trader_inventory = [x for x in trader_inventory if Item(x).name != self.name]