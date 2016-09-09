from random import shuffle, randrange, randint
import copy

from pprint import pprint

RED         = '\033[31m'
GREEN       = '\033[32m'
ORANGE      = '\033[33m'
BLUE        = '\033[34m'
PURPLE      = '\033[35m'
CYAN        = '\033[36m'
LIGHTGREY   = '\033[37m'
DARKGREY    = '\033[90m'
LIGHTRED    = '\033[91m'
LIGHTGREEN  = '\033[92m'
YELLOW      = '\033[93m'
LIGHTBLUE   = '\033[94m'
PINK        = '\033[95m'
LIGHTCYAN   = '\033[96m'
END         = '\033[0m'

colors = [
    RED,
    GREEN,     
    ORANGE,    
    BLUE,      
    PURPLE,    
    CYAN,      
    DARKGREY,  
    LIGHTRED,  
    LIGHTGREEN,
    YELLOW,    
    LIGHTBLUE, 
    PINK,      
    LIGHTCYAN, 
    ]
 
class Pos(object):
    def __init__(self, visited, x, y):
        self.x = x
        self.y = y
        self.visited = visited
        self.player = None

        self.next_rooms = {
            'n' : None,
            's' : None,
            'e' : None,
            'w' : None }

    def set_next_room(self, direction, room):
        self.next_rooms[direction] = room

    def get_next_room(self, direction):
        return self.next_rooms[direction]


class WorldPlayerController:
    def __init__(self, world, player, name):
        self.player = player
        self.name = name
        self.world = world
        self.pos = None
        self.color = colors[randint(0, len(colors) - 1)]
        self.distance_travelled = 0
        self.hits = 0

        while 1:
            # Pick a random spot in the maze
            rand_x = randrange(len(self.world.world) - 1)
            rand_y = randrange(len(self.world.world[0]) - 1)
            pos = self.world.world[rand_x][rand_y]

            # Is there someone else there?
            found = False
            for p in self.world.players:
                if p.pos == pos:
                    found = True
                    break
            if not found:
                self.pos = pos
                self.pos.player = self
                break

        self.direction = 'n'

        # Hookup the IO
        self.player.set_forward(self.forward)
        self.player.set_left(self.left)
        self.player.set_right(self.right)
        self.player.set_fire(self.fire)

    def step(self):
        self.player.step()

    def forward(self):
        new_room = self.pos.get_next_room(self.direction)

        # bump detection
        if not new_room or new_room.player:
            self.player.bump()
        else:
            # Move the player
            self.pos.player = None
            new_room.player = self

            self.pos = new_room

            self.distance_travelled += 1

    turn_left = {'n' : 'w',
                 'w' : 's',
                 's' : 'e',
                 'e' : 'n'}
    def left(self):
        self.direction = self.turn_left[self.direction]

    turn_right = {'n' : 'e',
                  'e' : 's',
                  's' : 'w',
                  'w' : 'n'}
    def right(self):
        self.direction = self.turn_right[self.direction]

    def fire(self):
        fire_room = self.pos
        while fire_room:
            # Go to the next room
            fire_room = fire_room.get_next_room(self.direction)

            # Is there something there?
            if fire_room and fire_room.player:
                fire_room.player.hit()
                self.hits += 1
                break

    def hit(self):
        self.player.hit()

        if not self.player.is_alive():
            # Kill player
            self.pos.player = None
            self.world.players.remove(self)

    def is_alive(self):
        return self.player.is_alive()


class World(object):
    def __init__(self, w, h):
        self.world = self.make_maze(w, h)
        self.players = []

    def make_maze(self, w = 16, h = 8):

        vis = [ [Pos(False, x, y) for y in range(h)] + [Pos(True, x, y)] for x in range(w)] + [[Pos(True, x, y) for _ in range(h + 1)]]

        def walk(x, y):

            vis[x][y].visited = True

            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if xx < 0 or yy < 0:
                    continue

                if vis[xx][yy].visited: 
                    continue

                if xx == x: 
                    # We moved N/S
                    if y > yy:
                        # We move N.
                        vis[x][y].set_next_room('n', vis[xx][yy])
                        vis[xx][yy].set_next_room('s', vis[x][y])
                    else:
                        # We move S.
                        vis[x][y].set_next_room('s', vis[xx][yy])
                        vis[xx][yy].set_next_room('n', vis[x][y])

                if yy == y: 
                    # We moved E/W
                    if x > xx:
                        # We moved W
                        vis[x][y].set_next_room('w', vis[xx][yy])
                        vis[xx][yy].set_next_room('e', vis[x][y])
                    else:
                        # We moved E
                        vis[x][y].set_next_room('e', vis[xx][yy])
                        vis[xx][yy].set_next_room('w', vis[x][y])

                walk(xx, yy)

        walk(randrange(w), randrange(h))

        return vis

    def add_player(self, name, player):
        self.players.append(WorldPlayerController(self, player, name))

    def find_player(self, name):
        return next((player.player for player in self.players if name == player.name), None)

    def draw(self):
        dir_chars = {
            'n' : '^',
            'e' : '>',
            'w' : '<',
            's' : 'v' 
            }


        s = ""
        for y in range(len(self.world[0]) - 1):
            row = [self.world[x][y] for x in range(len(self.world))]

            # Line 1, N 
            for x in range(len(row[:-1])):
                pos = row[x]
                if pos.get_next_room('n') is None or (y == 0):
                    s += "+-"
                else:
                    s += "+ "
            s += '+\n'

            # Line 2, e, w
            for x in range(len(row[:-1])):
                pos = row[x]
                if pos.get_next_room('w') is None or (x == 0):
                    s += "|"
                else:
                    s += " "

                # Is the player here?
                p = False
                for player in self.players:
                    if player.pos == pos:
                        p = True
                        s += player.color + dir_chars[player.direction] + END

                if not p:
                    s += " "

            s += '|\n'

        # Line 3, s
        for pos in row[:-1]:
            s += "+-"
        s += '+'

        return s

    def step(self):
        # copy the list of players
        players = copy.copy(self.players)

        shuffle(players)

        for player in players:
            if player.is_alive():
                player.step()
        #[player.step() for player in filter(lambda x: x.is_alive(), players)]

        # Delete any dead players
        #self.players = list(set(self.players) - set(filter(lambda x: not x.is_alive(), players)))
 
if __name__ == '__main__':
    print(make_maze())
