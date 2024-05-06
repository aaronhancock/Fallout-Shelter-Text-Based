"""General functions used by most modules in this project."""

from time import sleep
from config import LOAD_DELAY

def input_int(s):
    """Allow user to input integers while catching errors.

    Arguments:
    s -- string to print as a prompt

    Returns:
    x -- integer inputted by user
    """
    while True:
        try:
            x = int(input(s))
            break
        except ValueError:
            print_line("Invalid. Only integer numbers are accepted!")
    return x


def print_line(*messages, fast=True):
    """Replace print() with artificial line spacing.

    Arguments:
    *messages -- any number of arguments to print
    """
    for message in messages:
        message = str(message)
        for line in message.splitlines():
            sleep(LOAD_DELAY if fast else 0.5)
            print(line)


def load_time(x, message):
    """Loading bars.

    Arguments:
    x -- length of loading bar in seconds
    message -- message to print before loading bar
    """
    print(str(message))
    sleep(x / 10000)


def count_item(item, target_inventory, inventory, trader_inventory):
    """Count total number of specified item in inventory.

    Arguments:
    item -- item to count
    target_inventory -- inventory to count in
    inventory -- player's inventory
    trader_inventory -- trader's inventory

    Returns:
    int -- count of item in inventory
    """
    item = str(item)
    if target_inventory == "player":
        return inventory.count(item)
    elif target_inventory == "trader":
        return trader_inventory.count(item)
    else:
        print_line("Unknown inventory type.")
        return 0