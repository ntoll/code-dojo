opposites = dict(
    south = "north",
    east = "west",
    north = "south",
    west = "east")

class Room(object):
    def __init__(self, description, **exits):
        self._description = description
        for direction, room in exits.items():
            room.exits[opposites[direction]] = self
        self.exits = exits

    @property
    def description(self):
        return self._description + ". There are exits to the " + " and ".join(reversed(sorted(self.exits.keys())))

class Game(object):
    def __init__(self, firstRoom):
        self.room = firstRoom

    def cmd(self, action):
        direction = action = action.lower()
        if action == "look":
            return self.room.description
        if direction in self.room.exits:
            self.room = self.room.exits[direction]
            return "You go " + direction
        return "You can't do that"


def run_game():
    import sys
    northRoom = Room("You are in a passageway, it is still dark")
    eastRoom = Room("Swamp, dark")
    firstRoom = Room("You are in a dark cave", north=northRoom, east=eastRoom)

    game = Game(firstRoom)
    while True:
        line = raw_input("$ ")
        print game.cmd(line)

if __name__ == "__main__":
    run_game()
