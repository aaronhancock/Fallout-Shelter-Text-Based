"""Module containing all Human classes."""

from general_funcs import print_line


def get_room_index(room, rooms):
    """Get index of room in room list.

    Arguments:
    room -- room to get index of
    rooms -- list of all rooms in the game

    Returns:
    r -- index of room
    """
    for r in range(len(rooms)):
        if rooms[r].name == room:
            return r
    return -1


class Human(object):
    """Basic class for all humans in game."""

    def __init__(self, first_name, day_of_birth, parent_1, parent_2, age, gender):
        """Constructor for Human class.

        Arguments:
        first_name -- first name of Human
        day_of_birth -- day Human was born
        parent_1 -- name of Human's father
        parent_2 -- name of Human's mother
        age -- age of Human
        gender -- gender of Human
        """
        self.name = first_name
        self.day_of_birth = day_of_birth
        self.parent_1 = parent_1
        self.parent_2 = parent_2
        self.gender = gender
        self.surname = self.parent_1
        self.partner = ""
        self.age = age
        self.hunger = 0
        self.thirst = 0
        self.HP = 100
        self.XP = 0

        self.strength = 1
        self.perception = 1
        self.endurance = 1
        self.charisma = 1
        self.intelligence = 1
        self.luck = 1

        self.assigned_room = ""
        self.children = []
        self.partner = ""
        self.level = 1

    def __str__(self):
        """String representation of object, first name and last name.

        Returns:
        str -- "Firstname Lastname"
        """
        return "{} {}".format(self.name, self.surname)

    def level_up(self):
        """Level up Human and ask player for input on what stat to level up."""
        see_stats(self.name, self.surname)
        self.level += 1

        attributes = {
            "strength": self.strength,
            "perception": self.perception,
            "endurance": self.endurance,
            "charisma": self.charisma,
            "intelligence": self.intelligence,
            "luck": self.luck
        }

        if self.name == people[0].name:  # If player has leveled up
            print_line("\n")
            choice = input("Please choose an attribute to level up: ")
            if choice.lower() in attributes:
                attributes[choice.lower()] += 1
            else:
                print_line("Invalid choice")
                self.level -= 1
                self.level_up()
        else:  # If NPC has leveled up
            attribute = max(attributes, key=attributes.get)
            attributes[attribute] += 1

    def heal(self, amount):
        """Heal Human.

        Arguments:
        amount -- amount of health to give
        """
        player = people[0]
        if player.medic > 0:  # Medic Boost.
            amount *= 1 + (0.05 * player.medic)
        self.HP += amount
        if self.HP > 99:  # Truncates health
            self.HP = 100

    def rebirth(self):
        """Don't know if I'll ever use this."""
        self.age = 0
        print_line(self.name, "has been reborn and their stats have been reset")
        self.strength = 1
        self.perception = 1
        self.endurance = 1
        self.charisma = 1
        self.intelligence = 1
        self.luck = 1

    def get_index(self, people):
        """Return index of Human in list of all people.

        Arguments:
        people -- list of all people in the game

        Returns:
        x -- index of Human in list
        """
        for x in range(len(people)):
            if people[x].name == self.name and people[x].surname == self.surname:
                return int(x)

    def unassign(self, people):
        """Unassign Human from room.

        Arguments:
        people -- list of all people in the game
        """
        for room in rooms:
            string_room_name = str(room.assigned)
            lst = list(string_room_name)
            lst[self.get_index(people)] = '0'
            room.assigned = ''.join(lst)
        self.assigned_room = ''

    def assign_to_room(self, chosen_room, people, rooms):
        """Assign Human to room.

        Arguments:
        chosen_room -- room to assign to
        people -- list of all people in the game
        rooms -- list of all rooms in the game
        """
        person_index = self.get_index(people)
        room_index = get_room_index(chosen_room, rooms)
        room = rooms[room_index]

        if self.assigned_room != '':
            self.unassign(people)

        string = str(room.assigned)
        lst = list(string)
        lst[person_index] = '1'
        room.assigned = ''.join(lst)
        self.assigned_room = str(chosen_room)
        print_line(f"{self.name} {self.surname} has been assigned to {chosen_room}")

    def can_mate(self):
        """Check if Human meets requirements to have children.

        Returns:
            bool -- whether or not human can mate
        """
        if self.age < 18:
            return False
        if len(self.children) > 5:  # Upper limit of children is 5
            return False
        # Have to wait for a year before parent can have child again.
        for child in self.children:
            if next(person.age for person in people if person.name == child.split()[0]) < 1:
                return False
        return True

    def gain_xp(self, amount):
        """Add experience to Human.

        Arguments:
        amount -- amount of experience to add
        """
        self.XP += amount


class NPC(Human):
    """NPC class, inherits Human attributes."""

    def __init__(self, first_name, day_of_birth, parent_1, parent_2, age, gender):
        """NPC class constructor.

        Arguments:
        first_name -- first name of NPC
        day_of_birth -- day NPC was born on
        parent_1 -- name of father
        parent_2 -- name of mother
        age -- age of NPC
        gender -- gender of NPC
        """
        Human.__init__(self, first_name, day_of_birth, parent_1, parent_2, age, gender)
        self.scavenging = False
        self.days_scavenging = 0
        self.days_to_scavenge_for = 0

    def die(self):
        """Kill NPC."""
        global people
        global rooms
        print_line(self.name, " has died")
        if self.assigned_room != "":
            for x in range(len(people)):  # Fetches the index of the person.
                if people[x].name == self.name:
                    index = x
                    break
            for r in rooms:
                # Removes person from the rooms' assigned records.
                r.assigned = r.assigned[:index] + r.assigned[index+1:]
        people.remove(self)


class Player(Human):
    """Player class, inherits Human attributes."""

    def __init__(self, first_name, day_of_birth, parent_1, parent_2, age, gender):
        """Player class constructor.

        Arguments:
        first_name -- first name of Player
        day_of_birth -- day Player was born
        parent_1 -- name of Player's father
        parent_2 -- name of Player's mother
        age -- age of player
        gender -- gender of player
        """
        Human.__init__(self, first_name, day_of_birth, parent_1, parent_2, age, gender)

        self.medic = 0  # Improves healing capabilities of stimpacks
        self.crafting = 0  # Chance to not use components when crafting.
        self.tactician = 0  # Boosts defense.
        self.cooking = 0  # Boosts production level of kitchen.
        self.barter = 0  # Increases selling prices, decreases buying prices.
        self.inspiration = 0  # Boosts production and defense.
        self.scrapper = 0  # Boosts chance of bonus components when scrapping.
        self.electrician = 0  # Boosts power production