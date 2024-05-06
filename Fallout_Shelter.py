"""Text-based Fallout Shelter game developed by T.G."""
from random import randint

from Human import Player, NPC
from Room import Room
from Item import Item

from general_funcs import *


def storage_capacity(all_rooms):
    """Calculate max inventory capacity of player.

    Arguments:
    all_rooms -- list of currently built rooms

    Returns:
    capacity -- max inventory capacity of player
    """
    capacity = all_rooms("storage").production
    return capacity


def see_people():
    """Display info of all inhabitants."""
    for person in people:
        print_line(person.name, person.surname)
        print_line(
            "    Age:" + str(person.age),
            " Gender:" + person.gender.upper(),
            " Hunger:" + str(person.hunger),
            " Thirst:" + str(person.thirst),
            "   Room:" + person.assigned_room)


def see_inventory(inven):
    """Display all items in inventory.

    Arguments:
    inven -- inventory to show, 'player' or 'trader'
    """
    inven = str(inven)
    seen_items = []
    if inven == "player":
        for x in inventory:
            if x not in seen_items:
                count = count_item(x, "player")
                if count > 0:
                    it = Item(x)
                    print_line(
                        f"{x}*{count}",
                        f"| Weight: {it.weight}",
                        f"| Value: {it.value}",
                        f"| Components: {', '.join(it.components)}",
                        f"| Rarity: {it.rarity}")
                    seen_items.append(x)
    elif inven == "trader":
        for x in trader_inventory:
            if x not in seen_items:
                count = count_item(x, "trader")
                if count > 0:
                    it = Item(x)
                    print_line(
                        f"{x}*{count}",
                        f"| Weight: {it.weight}",
                        f"| Value: {it.value}",
                        f"| Components: {', '.join(it.components)}",
                        f"| Rarity: {it.rarity}")
                    seen_items.append(x)
    else:
        print_line("Bug with inventory system. Please contact dev!")


def print_help():
    """Print list of commands available to player."""
    print_line("""Commands:

    Room actions:
    see rooms           : View all rooms
    build x             : Construct room 'x'
    rush x              : Rush construction of room 'x'
    upgrade x           : Upgrade room 'x'
    fix x               : Fix damaged room 'x'

    Inhabitant actions:
    see people          : View all inhabitants
    feed x              : Feed inhabitant 'x'
    enable auto_feed    : Enable automatically feeding inhabitants
    disable auto_feed   : Disable automatically feeding inhabitants
    coitus x y          : Send inhabitants 'x' and 'y' to the love-house
    scavenge x          : Send inhabitant 'x' to scavenge in the wasteland
    heal x              : Heal inhabitant 'x'
    heal all            : Heal all inhabitants
    assign x y          : Assign inhabitant 'x' to room 'y'
    auto assign         : Automatically assign unassigned inhabitants to rooms

    Inventory actions:
    see items           : View all held items
    scrap x             : Destroy item and add its components to your inventory
    trade               : Begin trading interaction

    Other actions:
    skip                : Skip current day
    see day             : View day number
    see resources       : View all resources available
    end                 : Quit game
    help                : See this help text
    """, fast=True)


def living_capacity():
    """Get maximum inhabitant capacity of shelter.

    Returns:
    int -- maximum capacity of shelter
    """
    room = rooms[get_room_index('living')]
    print_line(f"Maximum number of inhabitants: {5 * room.level}")
    return 5 * room.level


def see_resources(inventory, trader_inventory):
    """Print food, water, and power Player has available."""
    print_line(f"Food: {count_item('food', 'player', inventory, trader_inventory)}")
    print_line(f"Water: {count_item('water', 'player', inventory, trader_inventory)}")
    print_line(f"Power: {count_item('watt', 'player', inventory, trader_inventory)}")


def get_person_index(first_name, surname):
    """Get index of inhabitant in list of all inhabitants.

    Arguments:
    first_name -- first name of inhabitant to search for
    surname -- surname of inhabitant to search for

    Returns:
    x -- index of person in list
    """
    for x in range(len(people)):
        if people[x].name == first_name.capitalize() and people[x].surname == surname.capitalize():
            return x
    return -1


def scavenge(first_name, surname, days=0):
    """Send inhabitant on scavenging mission.

    Arguments:
    first_name -- first name of inhabitant to send
    surname -- surname of inhabitant to send
    days -- number of days to scavenge (default: 0)
    """
    global people
    if not check_person(first_name, surname):
        print_line("Error with scavenging system. Please contact dev!")
    else:
        person = people[get_person_index(first_name, surname)]
        person.scavenging = True
        if not isinstance(days, int) or days <= 0:
            person.days_to_scavenge_for = 100
        else:
            person.days_to_scavenge_for = days
    use_points(10)


def build(r, player):
    """Build room specified.

    Arguments:
    r -- name of room to build
    player -- player object
    """
    global rooms
    global inventory
    built_room = Room(str(r), player)
    rooms.append(built_room)
    load_time(5, f"Building {r}")
    for y in built_room.components:
        for x in inventory:
            if y == x:
                Item(x).destroy("player")
                break
    player.gain_xp(100)
    use_points(10)


def craft(x):
    """Craft specified item.

    Arguments:
    x -- item to craft
    """
    global inventory
    load_time(5, f"Crafting {x}")
    add_to_inven(x, 1, "player")
    a = Item(x)
    chance = player.crafting * 2
    for y in a.components:
        for x in inventory:
            if y == x:
                chance_game = randint(0, 101)
                if chance_game > chance:
                    inventory.remove(x)
                break
    player.gain_xp(a.rarity * 10)
    use_points(5)


def get_player_gender():
    """Ask player what gender they are.

    Returns:
    char -- 'm' or 'f'
    """
    while True:
        gender = input("Please choose a gender (M/F): ")
        if len(gender) > 0:
            gender = gender[0].lower()
            if gender in ["m", "f"]:
                return gender
            else:
                print_line("Invalid gender choice!")
        else:
            print_line("No input detected!")


def get_gender():
    """Randomly generate gender for NPC.

    Returns:
    char -- 'm' or 'f'
    """
    return "m" if randint(0, 1) == 0 else "f"


def check_person(first_name, surname):
    """Check if inhabitant exists in list of all inhabitants.

    Arguments:
    first_name -- first name of inhabitant to check
    surname -- surname of inhabitant to check

    Returns:
    bool -- whether inhabitant exists or not
    """
    for per in people:
        if per.name == first_name.capitalize() and per.surname == surname.capitalize():
            return True
    return False


def gain_xp(first_name, last_name, amount):
    """Add experience to Human.

    Arguments:
    first_name -- first name of Human
    last_name -- last name of Human
    amount -- amount of experience to add
    """
    global people
    person = people[get_person_index(first_name, last_name)]
    person.XP += amount


def check_xp(first_name, surname):
    """Check experience of inhabitant.

    Arguments:
    first_name -- first name of inhabitant to check
    surname -- surname of inhabitant to check
    """
    global people
    person = people[get_person_index(first_name, surname)]
    xp_needed = 1000 + (3 ** person.level)
    if person.XP >= xp_needed:
        print_line(f"{person.name} has {person.XP} XP")
        print_line(f"{person.name} has leveled up")
        person.level_up()
        print_line(f"{person.name} is now level {person.level}")


def level_up(person):
    """Level up Human and ask player for input on what stat to level up.

    Arguments:
    person -- Person object at level x

    Returns:
    person -- Person object at level x+1
    """
    see_stats(person)
    person.level += 1
    if person.name == people[0].name:  # If player has leveled up
        print_line("\n")
        choice = input("Please choose an attribute to level up: ")
        choice = choice.lower()
        if choice == "strength":
            person.strength += 1
        elif choice == "perception":
            person.perception += 1
        elif choice == "endurance":
            person.endurance += 1
        elif choice == "charisma":
            person.charisma += 1
        elif choice == "intelligence":
            person.intelligence += 1
        elif choice == "luck":
            person.luck += 1
        elif choice == "medic":
            person.medic += 1
        elif choice == "crafting":
            person.crafting += 1
        elif choice == "tactician":
            person.tactician += 1
        elif choice == "cooking":
            person.cooking += 1
        elif choice == "inspiration":
            person.inspiration += 1
        elif choice == "scrapper":
            person.scrapper += 1
        elif choice == "barter":
            person.barter += 1
        elif choice == "electrician":
            person.electrician += 1
        else:
            print_line("Invalid choice")
            person.level -= 1
            level_up(person)
    else:
        # Automatically level up NPCs based on a predefined logic
        # (You can customize this based on your game's requirements)
        person.strength += 1
        person.perception += 1
        person.endurance += 1
        person.charisma += 1
        person.intelligence += 1
        person.luck += 1


def create_NPC(parent_1, parent_2):
    """
    Create new child inhabitant.

    Arguments:
        parent_1 -- parent of new child
        parent_2 -- parent of new child

    Returns:
        person -- New NPC
    """
    while True:
        name = input("Choose a first name for the new child: ")
        if len(name.split()) == 1:  # Player can only input one word
            if name not in used_names:
                name = name.capitalize()
                if parent_2.gender == "m":
                    parent_1, parent_2 = parent_2, parent_1
                if len(people) < 5 and day_count < 3:
                    age = 21
                else:
                    age = 0
                person = NPC(name, day_count, parent_1.surname, parent_2.surname, age, get_gender())
                parent_1.children.append(f"{name} {parent_1.surname}")
                parent_2.children.append(f"{name} {parent_1.surname}")
                parent_1.partner = f"{parent_2.name} {parent_2.surname}"
                parent_2.partner = f"{parent_1.name} {parent_1.surname}"
                see_people()
                update_all_assignment()
                if day_count > 2:  # First few births cost no points
                    use_points(50)
                player.gain_xp(100)
                use_points(25)
                used_names.append(name)
                load_time(5, f"{name} is being born!")
                return person
            else:
                print_line("Someone already has that name.")
        else:
            print_line("You have to input a single word!")


def death(person):
    """Kill inhabitant.

    Arguments:
    person -- Person who's dying

    Returns:
    None
    """
    global end
    global rooms
    print_line(f"{person.name} {person.surname} has died!")
    if isinstance(person, Player):  # If player has died.
        end = True
    else:
        if person.assigned_room != "":
            room = rooms[get_room_index(person.assigned_room)]
            room.assigned = room.assigned.replace("1", "0", 1)
    people.remove(person)


def mature(person):
    """Increment Human's age.

    Arguments:
    person -- Human who's aging

    Returns:
    person -- Human with one more year
    """
    person.age += 1
    print_line(f"{person.name} has matured and is now {person.age} years old!")
    return person


def take_damage(person, amount):
    """Take health from Human.

    Arguments:
    person -- Human who's taking damage
    amount -- amount of health to take

    Returns:
    person -- Human who has taken damage
    """
    global people
    person = people[get_person_index(person.name, person.surname)]

    person.defense = person.strength * 10
    damage_taken = amount - person.defense
    if damage_taken < 1:
        damage_taken = 0
    else:
        person.HP -= damage_taken
        if person.HP < 1:
            death(person)

    return person


def first_few():
    """Create first few inhabitants with random names."""
    global people
    global used_names
    global rooms
    names = [
        "Thompson",
        "Elenor",
        "Codsworth",
        "Sharmak",
        "Luthor",
        "Marshall",
        "Cole",
        "Diven",
        "Davenport",
        "John",
        "Max",
        "Lex",
        "Leth",
        "Exavor"]
    for person in people:
        used_names.append(person.name)
        used_names.append(person.surname)
    while len(people) < 5:
        num_1 = randint(0, len(names) - 1)
        num_2 = randint(0, len(names) - 1)
        if num_1 == num_2 or names[num_1] in used_names or names[num_2] in used_names:
            continue
        people.append(NPC(names[num_1], day_count, names[num_2], "Alena", 21, get_gender()))
        used_names.append(names[num_1])
        used_names.append(names[num_2])


def create_player():
    """Create player inhabitant.

    Returns:
    Player -- player object
    """
    while True:
        name = input("Choose a first name for yourself: ")
        if len(name) <= 0:
            print_line("You need a name!")
        elif len(name.split()) != 1:
            print_line("Only single word inputs are accepted.")
        else:
            name = name.capitalize()
            break
    while True:
        parent_1 = input("What is the surname of your father? ")
        if len(parent_1) <= 0:
            print_line("Your father needs a surname!")
        elif len(parent_1.split()) != 1:
            print_line("Only single word inputs are accepted.")
        else:
            parent_1 = parent_1.capitalize()
            break
    while True:
        parent_2 = input("What is the surname of your mother? ")
        if len(parent_2) <= 0:
            print_line("Your mother needs a surname!")
        elif len(parent_2.split()) != 1:
            print_line("Only single word inputs are accepted.")
        else:
            parent_2 = parent_2.capitalize()
            break
    while True:
        gender = input("What is your gender? (m/f) ")
        if len(gender) == 0:
            print_line("You need a gender.")
        elif gender.lower() not in ["m", "f"]:
            print_line("Invalid input. Only accepts 'm' or 'f'.")
        else:
            gender = gender.lower()
            break

    return Player(name, day_count, parent_1, parent_2, 21, gender)


def see_stats(person):
    """Check stats of inhabitant.

    Arguments:
    person - Person whose stats are being viewed
    """
    print_line(f"Strength: {person.strength}")
    print_line(f"Perception: {person.perception}")
    print_line(f"Endurance: {person.endurance}")
    print_line(f"Charisma: {person.charisma}")
    print_line(f"Intelligence: {person.intelligence}")
    print_line(f"Luck: {person.luck}")
    if person.name == player.name:  # Player has extra stats
        print_line("")
        print_line(f"Medic: {person.medic}")
        print_line(f"Crafting: {person.crafting}")
        print_line(f"Tactician: {person.tactician}")
        print_line(f"Cooking: {person.cooking}")
        print_line(f"Inspiration: {person.inspiration}")
        print_line(f"Scrapping: {person.scrapper}")
        print_line(f"Bartering: {person.barter}")
        print_line(f"Electrician: {person.electrician}")


def auto_assign():
    """Automatically assign inhabitants to rooms."""
    global people
    global rooms
    for person in people:
        if person.assigned_room == "":
            for r in rooms:
                if r.count_assigned() < r.assigned_limit:
                    person.assign_to_room(r.name, people, rooms)
                    break


def update_all_assignment():
    """When vault population increases, updates length of the assignment variable."""
    global rooms
    for r in rooms:
        current_count = len(r.assigned)
        required_count = len(people)
        if current_count < required_count:
            difference = required_count - current_count
            r.assigned += "0" * difference


def get_room_index(room):
    """Get index of room in room list.

    Arguments:
    room -- room to get index of

    Returns:
    r -- index of room
    """
    for r in range(len(rooms)):
        if rooms[r].name == room:
            return r
    return -1


def check_room(room):
    """Check if room exists.

    Arguments:
    room -- room to check for

    Returns:
    bool -- whether room exists or not
    """
    return room in all_rooms


def check_built_room(room):
    """Check if room has been built yet.

    Arguments:
    room -- room to check for

    Returns:
    bool -- whether room has been built or not
    """
    for r in rooms:
        if room == r.name:
            return True
    return False


def see_rooms(player):
    """Print each room and details."""
    print_line("")
    for r in rooms:
        print_line(" ".join(word.capitalize() for word in r.name.split()))
        if r.can_produce:
            r.update_production(player, people)
            print_line(
                f"\n    Risk: {r.risk * 10}%",
                f"    Level: {r.level}",
                f"    Power: {r.power_available}",
                f"    Production: {r.production}")
        else:
            print_line(
                f"\n    Risk: {r.risk}%",
                f"    Level: {r.level}",
                f"    Power: {r.power_available}")

        if r.can_produce or r.name == "trader":
            r.see_assigned(people)


def can_use_power(room, inventory, trader_inventory):
    """
    Determine whether the room may use power or not.

    Arguments:
    room -- the room to check power usage for
    inventory -- player's inventory
    trader_inventory -- trader's inventory

    Returns:
    bool -- whether room may use power
    """
    return count_item('watt', 'player', inventory, trader_inventory) > room.power_usage


def power_usage():
    """Check total power needed.

    Returns:
    total -- total power needed by all rooms
    """
    total = sum(r.power_usage for r in rooms)
    return total


def power_production():
    """Check total power being produced.

    Returns:
    production -- total amount of power being produced
    """
    generator = rooms[get_room_index('generator')]
    return generator.production


def rand_item(target_inventory):
    """Put a random item in inventory.

    Arguments:
    target_inventory -- inventory to put item in
    """
    num = randint(1, 1024)
    lst = [2**a for a in range(0, 11)]
    count = 0
    for chance in lst:
        if num < chance:
            break
        count += 1
    rar = 10 - count
    possible_items = [x for x in all_items if Item(x).rarity == rar]
    if possible_items:
        actual_item = possible_items[randint(0, len(possible_items) - 1)]
        if target_inventory == "player":
            add_to_inven(actual_item, 1, 'inventory')
        elif target_inventory == "trader":
            add_to_inven(actual_item, 1, 'trader')
        else:
            print_line("Bug with random item system. Please contact dev!")


def count_weight():
    """Calculate weight of all items in inventory.

    Returns:
    weight -- weight of all items in inventory
    """
    weight = sum(Item(x).weight for x in inventory)
    return weight


def find_rand_item(inven, items):
    """Find random items and add them to inventory.

    Arguments:
    inven -- inventory to add items to
    items -- how many items to add
    """
    for _ in range(items):
        rand_item(inven)


def add_to_inven(x, number, inven):
    """Add given item to inventory.

    Arguments:
    x -- item to add to inventory
    number -- amount of item to add to inventory
    inven -- inventory to add item to
    """
    global trader_inventory
    global inventory
    x = str(x)
    inven = str(inven)
    if x not in all_items:
        print_line(
            "Item doesn't exist in the game's databases. ",
            "Major bug with inventory adding system. Please contact dev.")
    else:
        if inven == "player":
            inventory.extend([x] * number)
        elif inven == "trader":
            trader_inventory.extend([x] * number)


def lose_items(inven, number):
    """Randomly delete multiple items from inventory.

    Arguments:
    inven -- inventory to delete items from
    number -- amount of items to delete
    """
    global inventory
    global trader_inventory
    if inven == "trader":
        for _ in range(number):
            if trader_inventory:
                index = randint(0, len(trader_inventory) - 1)
                trader_inventory.pop(index)
    elif inven == "player":
        print_line("The raid made off with these items!")
        for _ in range(number):
            if inventory:
                index = randint(0, len(inventory) - 1)
                item = inventory.pop(index)
                print_line(item)
    else:
        print_line("Major bug in item losing system. Please contact dev!")


def scrap(it):
    """Scrap item and receive its components.

    Arguments:
    it -- item to scrap
    """
    global inventory
    if it not in all_items:
        print_line(
            "Bug with item scrapping system.",
            "Invalid argument passed to function. Please contact dev.")
    else:
        if it in inventory:
            Item(it).scrap()
            load_time(300, f"Scrapping {it}")
            player.gain_xp(Item(it).rarity * 10)
            inventory.remove(it)
    use_points(2)


def raid(player):
    """Force raid on shelter."""
    update_defense(player)
    raiders = ["Super Mutant", "Raider", "Synth", "Feral Ghoul"]
    raider = raiders[randint(0, len(raiders) - 1)]
    increasing_attack = day_count // 5
    attack_power = randint(1, increasing_attack)
    load_time(10, f"There was a {raider} raid on your shelter!")
    print_line(f"The total enemy power was {attack_power}")
    print_line(f"Your total defenses are {defense}")
    if defense > attack_power:
        print_line("Your defenses were strong enough to send them packing!")
    else:
        loss = attack_power - defense
        lose_items("player", loss)
        if loss > 10:
            death_chance = loss // 10
            dice = randint(2, 25)
            if death_chance < dice:
                possible_deaths = people[1:]
                if possible_deaths:
                    victim = possible_deaths[randint(0, len(possible_deaths) - 1)]
                    print_line(f"{victim.name} {victim.surname} has been killed in a raid")
                    death(victim)
    for person in people:
        person.gain_xp(attack_power * 10)
    use_points(30)


def update_defense(player):
    """Update defense of shelter based on guns and turrets in inventory."""
    global defense
    defense = 0
    turret_count = count_item("turret", "player")
    defense += 10 * turret_count
    gun_count = count_item("gun", "player")
    defense += gun_count
    strength_sum = sum(person.strength for person in people)
    defense += strength_sum
    if player.tactician > 0:
        defense *= 1 + (player.tactician * 0.05)
    if player.inspiration > 0:
        defense *= 1 + (player.inspiration * 0.03)


def avg_hunger():
    """Calculate average hunger level of all inhabitants.

    Returns:
    avg -- average hunger level
    """
    total = sum(x.hunger for x in people)
    avg = total // len(people)
    return avg


def avg_thirst():
    """Calculate average thirst level of all inhabitants.

    Returns:
    avg -- average thirst level
    """
    total = sum(x.thirst for x in people)
    avg = total // len(people)
    return avg


def feed(first_name, surname, amount):
    """Reduce hunger level of inhabitant.

    Arguments:
    first_name -- first name of inhabitant to feed
    surname -- surname of inhabitant to feed
    amount -- how much to feed inhabitant
    """
    global people
    global inventory
    person = people[get_person_index(first_name, surname)]
    person.hunger -= amount * 10
    if person.hunger < 0:
        person.hunger = 0
    Item('food').destroy('player')


def drink(first_name, surname, amount):
    """Reduce thirst level of inhabitant.

    Arguments:
    first_name -- first name of inhabitant to feed
    surname -- surname of inhabitant to feed
    amount -- how much to feed inhabitant
    """
    global inventory
    global people
    person = people[get_person_index(first_name, surname)]
    person.thirst -= amount
    if person.thirst < 0:
        person.thirst = 0
    Item('water').destroy('player')


def auto_feed_all(inventory, trader_inventory):
    """Automatically feed all inhabitants."""
    global people
    food_count = count_item("food", "player", inventory, trader_inventory)
    water_count = count_item("water", "player", inventory, trader_inventory)
    load_time(200, "Feeding all inhabitants.")
    while food_count > 0 and avg_hunger() > 2:
        for person in people:
            feed(person.name, person.surname, 1)
            food_count -= 1
    while water_count > 0 and avg_thirst() > 2:
        for person in people:
            drink(person.name, person.surname, 1)
            water_count -= 1


def happiness_loss():
    """Decrease overall happiness level based on overall hunger and thirst."""
    global happiness
    loss = 0
    for y in range(30, 101, 10):
        if avg_hunger() < y:
            loss += y - 30
            break
    for y in range(30, 101, 10):
        if avg_thirst() < y:
            loss += y - 30
            break
    if loss > 0:
        happiness -= loss
        print_line(
            f"Due to your inhabitants being hungry and/or thirsty, the "
            f"shelter's overall happiness has dropped to {happiness}")


def use_points(point):
    """Remove action points from total.

    Arguments:
    point -- how many points to remove
    """
    global action_points
    global overuse
    global overuse_amount
    if point > 50:
        print_line(
            "Bug with point usage system. ",
            "It's trying to use more than 50, " +
            "please note this and contact dev.")
    else:
        usage = action_points - point
        overuse = False
        if usage < 0:
            overuse_amount = abs(usage)
            overuse = True
        else:
            action_points -= usage

def trade():
    """Trading system."""
    load_time(100, "Initializing trading system.")
    global inventory
    global trader_inventory
    global caps
    global trader_caps
    stop_trade = False
    while not stop_trade:
        print_line("")
        print_line("Here are the traders' items: ")
        see_inventory("trader")
        print_line(f"\nThe trader has {trader_caps} caps.")

        print_line("\nHere are your items: ")
        see_inventory("player")
        print_line(f"\nYou have {caps} caps.")

        print_line(
            "\nFor instance, input (buy 5 food) if you want to buy 5 " +
            "units of food. Or input (end) to stop trading.")
        a = input("What trade would you like to make? ")
        if len(a) < 1:
            print_line("You have to input something")
            continue

        let_trade = False
        if len(a.split()) != 3:
            if len(a.split()) == 2:
                if a.split()[1] in all_items:
                    if a.split()[0] in ["buy", "sell"]:
                        a = f"{a.split()[0]} 1 {a.split()[1]}"
                        let_trade = True
                    else:
                        print_line("Invalid input. You can (buy) or (sell)")
                else:
                    print_line("This item doesn't exist")
            elif a.split()[0] in ['end', 'stop']:
                stop_trade = True
            else:
                print_line("You have to input 3 words. Buy/sell, amount, item")
        elif len(a.split()) == 3:
            let_trade = True

        if let_trade:
            if a.split()[2] in all_items:
                check = True
                try:
                    amount = int(a.split()[1])
                except ValueError:
                    print_line("You have to input a number as the second word")
                    check = False
                if check:
                    cost = Item(a.split()[2]).value
                    print_line(f"Cost of one item: {cost}")
                    total_cost = cost * amount
                    print_line(f"Cost of all items: {total_cost}")
                    action = a.split()[0].lower()
                    if action == "buy":
                        for x in range(0, 4):
                            total_cost = int(total_cost * (1.2 - (x * 0.05)))
                        if total_cost > caps:
                            print_line("You can't afford that!")
                        else:
                            count = count_item(a.split()[2], "trader")
                            if amount > count:
                                if not count:
                                    print_line(f"The trader doesn't have any {a.split()[2]}")
                                else:
                                    print_line(f"The trader doesn't have {a.split()[1]} of {a.split()[2]}")
                            else:
                                for _ in range(amount):
                                    trader_inventory.remove(a.split()[2])
                                    inventory.append(a.split()[2])
                                caps -= total_cost
                                trader_caps += total_cost
                    elif action == "sell":
                        for x in range(0, 4):
                            total_cost = int(total_cost * (0.8 + (x * 0.05)))
                        if total_cost > trader_caps:
                            print_line("The trader can't afford that!")
                        else:
                            count = count_item(a.split()[2], "player")
                            if amount > count:
                                if not count:
                                    print_line(f"You don't have any {a.split()[2]}")
                                else:
                                    print_line(f"You don't have {amount} of {a.split()[2]}")
                            else:
                                for _ in range(amount):
                                    inventory.remove(a.split()[2])
                                    trader_inventory.append(a.split()[2])
                                trader_caps -= total_cost
                                caps += total_cost
                    else:
                        print_line("Invalid Input. Only 'buy' and 'sell' are accepted")
                else:
                    print_line("Only numbers are accepted")
            else:
                print_line(f"Sorry. {a.split()[2]} doesn't exist!")
    load_time(100, "Ending trade")

def choice():
    """Choice/Command input system."""
    global auto_feed
    global people
    global rooms
    global player
    a = input("Choose what to do: ")
    if len(a) > 0:
        if a.split()[0] == "build":
            potential_room = ' '.join(a.split()[1:])
            if len(a.split()) < 2:
                print_line("You have to input 2 or more words to build a room.")
            elif not check_room(potential_room):
                print_line(f"Checking for room: {potential_room}")
                print_line("This room doesn't exist.")
            elif check_built_room(potential_room):
                print_line("You've already built this room.")
            else:
                room = Room(potential_room, player)
                checked = []
                can_craft = True
                for component in room.components:
                    if component not in checked:
                        if room.count_component(component) > count_item(component, "player", inventory, trader_inventory):
                            print_line(f"You don't have enough {component} to build {potential_room}")
                            can_craft = False
                        checked.append(component)
                if can_craft:
                    print_line(f"You have built a {potential_room}")
                    build(potential_room, player)

        elif a.split()[0] == "craft":
            if a.split()[1] not in all_items:
                print_line("Invalid item. Try again.")
            else:
                can_craft = True
                actual_item = Item(a.split()[1])
                if len(actual_item.components) == 0:
                    print_line("This is a basic item and so cannot be crafted.")
                else:
                    checked = []
                    for component in actual_item.components:
                        if component not in checked:
                            number_available = count_item(component, "player", inventory, trader_inventory)
                            number_needed = actual_item.count_component(component)
                            if number_needed > number_available:
                                print_line(f"You don't have enough {component} to craft {a.split()[1]}")
                                can_craft = False
                            checked.append(component)
                    if can_craft:
                        print_line(f"You have crafted a {a.split()[1]}")
                        craft(a.split()[1])

        elif a.split()[0] == "scrap":
            if len(a.split()) == 2:
                if a.split()[1] not in all_items:
                    print_line("Invalid item. Please try again.")
                else:
                    count = count_item(str(a.split()[1]), "player", inventory, trader_inventory)
                    if count > 0:
                        scrap(a.split()[1])
                    else:
                        print_line("You don't have that item.")
            elif len(a.split()) == 3:
                if int(a.split()[1]) in range(1, 100):
                    if a.split()[2] in all_items:
                        count = count_item(str(a.split()[1]), "player", inventory, trader_inventory)
                        if count >= int(a.split()[1]):
                            for _ in range(int(a.split()[1])):
                                scrap(a.split()[2])
                        else:
                            print_line("You don't have enough of these items to scrap that many times.")
                    else:
                        print_line("This item doesn't exist.")
                else:
                    print_line("Invalid input. You can scrap an item up to 99 times (If you have that many).")
            else:
                print_line("Invalid Input. Either enter (scrap wood) or (scrap 5 wood)")

        elif a.split()[0] == "rush":
            potential_room = ' '.join(a.split()[1:])
            if not check_room(potential_room):
                print_line("This room doesn't exist.")
            elif not check_built_room(potential_room):
                print_line("You haven't built this room yet.")
            elif not Room(potential_room).can_rush:
                print_line("This room cannot be rushed")
            elif Room(potential_room).rushed:
                print_line("This room has already been rushed.")
            else:
                room = rooms[get_room_index(potential_room)]
                chance = randint(0, 9)
                if room.risk > chance:
                    print_line(f"{room.name} has failed to rush and is broken!")
                    room.broken = True
                else:
                    check = input(f"Are you sure? {room.name} has a {room.risk * 10}% chance of breaking.")
                    if len(check) > 0:
                        if check[0].lower() == "y":
                            room.rush()
                        else:
                            print_line("Rush failed.")
                    else:
                        print_line("Rush failed.")

        elif a.split()[0] == "fix":
            potential_room = ' '.join(a.split()[1:])
            if not check_room(potential_room):
                print_line("This room doesn't exist.")
            elif not check_built_room(potential_room):
                print_line("You haven't built this room yet.")
            elif not rooms[get_room_index(potential_room)].broken:
                print_line("This room isn't even broken. There's no need to fix it!")
            else:
                room = rooms[get_room_index(potential_room)]
                can_fix = True
                items_needed = []
                for it in room.components:
                    chance = randint(0, 1)
                    if chance:
                        items_needed.append(it)
                checked_items = []
                for it in items_needed:
                    if it not in checked_items:
                        available = count_item(it, 'player', inventory, trader_inventory)
                        needed = room.count_component(it)
                        if needed > available:
                            print_line(f"You need {needed - available} more {it} to fix this room.")
                            can_fix = False
                        checked_items.append(it)
                if can_fix:
                    room.broken = False
                    for it in items_needed:
                        Item(it).destroy("player")
                    print_line(f"{room.name} has been fixed and is now in full working order.")

        elif a.split()[0] == "see":
            if a.split()[1] == "people":
                see_people()
            elif a.split()[1] == "items":
                see_inventory("player")
            elif a.split()[1] == "rooms":
                see_rooms(player)
            elif a.split()[1] == "day":
                print_line(f"Today is day {day_count}")
            elif a.split()[1] == "resources":
                see_resources(inventory, trader_inventory)
            else:
                print_line("Incorrect input. You can (see people), (see inventory), (see rooms) or (see resources)")

        elif a.split()[0] == "coitus":
            if len(a.split()) != 5:
                print_line("You need to input 2 mature people of opposite genders in the form (coitus Alex Marshall Mallus Cumberland)")
            elif not check_person(a.split()[1], a.split()[2]):
                print_line(f"No such {a.split()[1]} {a.split()[2]} exists!")
            elif not check_person(a.split()[3], a.split()[4]):
                print_line(f"No such {a.split()[3]} {a.split()[4]} exists!")
            elif len(people) == living_capacity():
                print_line("You've reached the vault's maximum capacity. Upgrade your living room to hold more people")
            else:
                person_1 = people[get_person_index(a.split()[1], a.split()[2])]
                person_2 = people[get_person_index(a.split()[3], a.split()[4])]
                if (person_1.partner == "" and person_2.partner == "") or person_1.partner == f"{person_2.name} {person_2.surname}":
                    if person_1.age < 18:
                        print_line(f"{a.split()[1]} isn't old enough to copulate.")
                    elif person_2.age < 18:
                        print_line(f"{a.split()[3]} isn't old enough to copulate.")
                    elif person_1.surname == person_2.surname:
                        print_line("Incest isn't allowed. At least be ethical!")
                    elif person_1.gender == person_2.gender:
                        print_line("The people need to be different genders! COME ON MAN CAN U EVEN BIOLOGY!?")
                    else:
                        person = create_NPC(person_1, person_2)
                        people.append(person)
                else:
                    print_line("Infidelity shall not be allowed!!!")
                    if person_1.partner != "":
                        print_line(f"{person_1.name} {person_1.surname} is married to {person_1.partner}")
                    else:
                        print_line(f"{person_1.name} {person_1.surname} isn't married.")
                    if person_2.partner != "":
                        print_line(f"{person_2.name} {person_2.surname} is married to {person_2.partner}")
                    else:
                        print_line(f"{person_2.name} {person_2.surname} isn't married.")

        elif a.split()[0] == "feed":
            if len(a) > 0:
                if avg_hunger() < 2:
                    print_line("Your people are working on full bellies boss!")
                elif len(a.split()) == 2:
                    if a.split()[1] not in [person.name for person in people]:
                        print_line("This person doesn't exist.")
                    else:
                        hunger = next(person.hunger for person in people if person.name == a.split()[1])
                        amount = int(input(f"Feed {a.split()[1]} by how much? "))
                        if amount < hunger:
                            print_line(f"You don't have enough food to feed {a.split()[1]}")
                        else:
                            feed(a.split()[1], "", amount)
                else:
                    print_line("Invalid input! Can only feed one person like this. Use the auto_feed system to feed everyone.")
            else:
                print_line("Invalid input. Who do you want to feed?")

        elif a.split()[0] == "trade":
            if not check_built_room('trader'):
                print_line("You haven't built a trader room yet!")
            elif '1' not in str(rooms[get_room_index('trader')].assigned):
                print_line("No one has been assigned to this room! You can't trade until then.")
            else:
                trade()

        elif a.split()[0] == "assign":
            potential_room = ' '.join(a.split()[4:])
            if len(a.split()) < 5:
                print_line("You have to input 4 or more words. E.g., assign Thomas Marc to living")
            elif not check_person(a.split()[1], a.split()[2]):
                print_line(f"This {a.split()[1]} doesn't exist.")
            elif not check_room(potential_room):
                print_line("This room doesn't exist.")
            elif not check_built_room(potential_room):
                print_line("You haven't built this room yet")
            elif rooms[get_room_index(potential_room)].assigned_limit == rooms[get_room_index(potential_room)].count_assigned():
                print_line("This room is full.")
                print_line("You can assign someone in the room to another room to create space.")
            else:
                person_index = get_person_index(a.split()[1].capitalize(), a.split()[2].capitalize())
                people[person_index].assign_to_room(potential_room)

        elif a.split()[0] == "auto":
            if a.split()[1] == "assign":
                auto_assign()

        elif a.split()[0] == "upgrade":
            if not check_room(a.split()[1]) or not check_built_room(a.split()[1]):
                print_line("This room doesn't exist. Try again.")
            elif a.split()[1] == "trader":
                print_line("This room cannot be upgraded")
            else:
                r = rooms[get_room_index(a.split()[1])]
                items_needed = r.components.copy()
                for _ in range(r.level - 1):
                    items_needed.extend(r.components)
                can_up = True
                for ite in all_items:
                    needed = items_needed.count(ite)
                    available = count_item(ite, "player", inventory, trader_inventory)
                    if available < needed:
                        can_up = False
                        print_line(f"You don't have enough {ite} to upgrade your {r.name}")
                        break
                if can_up:
                    for component in items_needed:
                        inventory.remove(component)
                    r.upgrade()
                    print_line(f"{r.name} has been upgraded and is now level {r.level}")

        elif a.split()[0] == "disable":
            if a.split()[1] == "auto_feed":
                auto_feed = False
                print_line("Warning. You have disabled the auto_feed feature. Be careful, your people may starve!")
            else:
                print_line("Invalid input. You can disable the 'auto_feed' system.")

        elif a.split()[0] == "enable":
            if a.split()[1] == "auto_feed":
                auto_feed = True
                print_line("Auto-feed system is working optimally.")
            else:
                print_line("Invalid Input. You can enable the 'auto_feed' system.")

        elif a.split()[0] == "scavenge":
            if a.split()[1] not in [person.name for person in people]:
                print_line("This person doesn't exist.")
            elif next(person.scavenging for person in people if person.name == a.split()[1]):
                print_line("This person is already out scavenging.")
            else:
                cho = input("Would you like to scavenge for a certain number of days or until their health gets low? (1-100/H) ")
                try:
                    cho = int(cho)
                except ValueError:
                    pass
                scavenge(a.split()[1], "", cho)

        elif a.split()[0] == "heal":
            if a.split()[1] == "all":
                for person in people:
                    person.heal(100)
            else:
                if a.split()[1] not in [person.name for person in people]:
                    print_line("That person doesn't exist.")
                else:
                    stim_count = count_item("stimpack", "player", inventory, trader_inventory)
                    if stim_count > 0:
                        next(person for person in people if person.name == a.split()[1]).heal(100)
                        inventory.remove("stimpack")

        elif a.split()[0] == "skip":
            global skip
            skip = True

        elif a.split()[0] == "end":
            global player_quit
            confirm = input("Are you sure? All unsaved data will be lost! ")
            confirm = confirm[0].lower()
            if confirm == "y":
                player_quit = True

        elif a.split()[0] == "help":
            print_help()

        else:
            print_line("Invalid Input. Try again.")
    else:
        print_line("You have to choose something!")


def game():
    """Game system."""
    global action_points
    global end
    global position
    global people
    global day_count
    global inventory
    global rooms
    global caps
    global trader_caps
    global trader_inventory
    global all_rooms
    global all_items
    global defense
    global overuse
    global overuse_amount
    global happiness
    global auto_feed
    global used_names
    global player_quit
    global skip
    global player
    load_time(300, "Initializing game.")

    day_count = 1
    skip = False
    end = False
    position = "secure"
    player_quit = False

    people = []
    used_names = []
    inventory = ['turret']

    player = create_player()
    load_time(100, "Creating player.")
    first_few()
    load_time(200, "Populating Vault with 5 random inhabitants")

    rooms = [
        Room('generator', player),
        Room('living', player),
        Room('kitchen', player),
        Room('water works', player),
        Room('trader', player)]

    all_items = [
        "wood",
        "steel",
        "turret",
        "food",
        "water",
        "wire",
        "silicon",
        "chip",
        "watt",
        "copper",
        "gun"]

    all_rooms = [
        "living",
        "bath",
        "generator",
        "kitchen",
        "trader",
        "storage",
        "water works"]

    caps = 100
    trader_caps = 400
    happiness = 100
    trader_inventory = []
    find_rand_item("trader", 20)
    defense = 0
    overuse = False
    auto_feed = True

    print_line("Welcome to the text-based fallout shelter game!")
    print_line("Welcome, great Overseer!")
    print_line("It is your great duty to increase the population of your vault and keep your inhabitants happy.")

    print_line("\nYou have been given 100 caps to start your journey.")
    action_points = 50
    update_all_assignment()

    print_help()

    while not end and position == "secure" and not player_quit:
        action_points = 50
        if overuse:
            action_points = 50 - overuse_amount
        load_time(300, "A new day dawns.")
        print_line(f"Today is day {day_count}")

        if auto_feed:
            auto_feed_all(inventory, trader_inventory)

        number = randint(0, len(trader_inventory) // 5)
        lose_items("trader", number)
        number = randint(0, len(trader_inventory) // 5)
        find_rand_item("trader", number)

        print_line(f"Producing {rooms[get_room_index('generator')].production} power")
        add_to_inven("watt", rooms[get_room_index('generator')].production, "player")
        see_resources(inventory, trader_inventory)

        for r in rooms:
            if r.name != 'generator' and r.can_produce:
                if can_use_power(r, inventory, trader_inventory):
                    r.use_power()
                    r.update_production(player, people)
                    if r.name == "kitchen":
                        add_to_inven("food", r.production, 'player')
                        print_line(f"Cooking {r.production} food.")
                    elif r.name == "water works":
                        add_to_inven("water", r.production, 'player')
                        print_line(f"Pumping {r.production} water.")
                else:
                    print_line(f"You don't have enough power to keep the {r.name} supplied.")
                if r.can_rush and r.rushed:
                    r.rushed = False

        for person in people:
            person.hunger += 10
            if person.hunger > 99:
                print_line(f"{person.name} {person.surname} has died of hunger")
                death(person)
            elif person.hunger > 80:
                print_line(f"Warning! {person.name} {person.surname} is starving and may die soon.")
            elif person.hunger > 50:
                print_line(f"{person.name} {person.surname} is hungry.")
            person.thirst += 10
            if person.thirst > 99:
                print_line(f"{person.name} {person.surname} has died of thirst")
                death(person)
            elif person.hunger > 80:
                print_line(f"Warning! {person.name} {person.surname} is extremely thirsty and may die soon.")
            elif person.hunger > 50:
                print_line(f"{person.name} {person.surname} is thirsty.")
            check_xp(person.name, person.surname)
            if person.name != player.name:
                if person.scavenging:
                    if person.days_to_scavenge_for == person.days_scavenging:
                        person.scavenging = False
                        person.days_to_scavenge_for = 0
                        person.days_scavenging = 0
                    else:
                        person.days_scavenging += 1
                        rand_item("player")
                        health_loss = randint(0, 50)
                        take_damage(person, health_loss)
                        person.gain_xp(randint(10, 200))
                    if person.health < 20:
                        person.scavenging = False
                        person.days_to_scavenge_for = 0
                        person.days_scavenging = 0
                if person.assigned_room != "":
                    r = rooms[get_room_index(person.assigned_room)]
                    if r.can_produce:
                        person.gain_xp(r.production // 10)

        raid_chance = randint(1, 5)
        if day_count < 11:
            raid_chance = 1
        if day_count == 5 or raid_chance > 4:
            raid(player)

        while action_points > 0 and not overuse and not player_quit:
            choice()
            if skip:
                break
        skip = False

        print_line(f"Due to your shelter's happiness level, you have gained {happiness // 10} experience")
        player.gain_xp(happiness // 10)
        if happiness < 5:
            position = "lost"
        elif happiness < 25:
            print_line("Warning. Your people are unhappy. You could lose your position if you don't improve the situation soon.")
        happiness_loss()

        day_count += 1

    else:
        if end:
            print_line("Too bad. You died.")
        elif position == "lost":
            print_line("Too bad. You lost your position because of your poor leadership skills.")
        again = input("Want to play again? ")
        if again[0].lower() == "y":
            game()
        else:
            print_line("Okay. Thanks for playing!!!")


if __name__ == '__main__':
    game() 