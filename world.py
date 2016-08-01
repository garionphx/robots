from random import shuffle, randrange
from pprint import pprint
 
class Pos(object):
    def __init__(self, visited):
        self.visited = visited
        self.room_n = None
        self.room_s = None
        self.room_e = None
        self.room_w = None

class WorldPlayerController:
    def __init__(self, world, player):
        self.player = player
        self.world = world
        self.pos = None
        while 1:
            # Pick a random spot in the maze
            pos = self.world.world[randrange(len(self.world.world))][randrange(len(self.world.world[0]))]

            # Is there someone else there?
            found = False
            for p in self.world.players:
                if p.pos == pos:
                    found = True
                    break
            if not found:
                self.pos = pos
                break

        self.direction = 'n'

        # Hookup the IO
        self.player.set_forward(self.forward)
        self.player.set_left(self.left)
        self.player.set_right(self.right)

    def step(self):
        self.player.step()

    def forward(self):
        curr_dir = self.direction
        if curr_dir == 'n':
            new_room = self.pos.room_n
        elif curr_dir == 'e':
            new_room = self.pos.room_e
        elif curr_dir == 's':
            new_room = self.pos.room_s
        elif curr_dir == 'w':
            new_room = self.pos.room_w
            
        # bump detection
        if not new_room:
            self.player.bump()
        elif any([(p.pos == new_room) for p in self.world.players]):
            self.player.bump()
        else:
            self.pos = new_room

    def left(self):
        turn = {'n' : 'w',
                'w' : 's',
                's' : 'e',
                'e' : 'n'}

        self.direction = turn[self.direction]

    def right(self):
        turn = {'n' : 'e',
                'e' : 's',
                's' : 'w',
                'w' : 'n'}

        self.direction = turn[self.direction]

class World(object):
    def __init__(self, w, h):
        self.world = self.make_maze(w, h)
        self.players = []

    def make_maze(self, w = 16, h = 8):

        vis = [ [Pos(False) for _ in range(h)] + [Pos(True)] for _ in range(w)] + [[Pos(True) for _ in range(h + 1)]]

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
                        vis[x][y].room_n = vis[xx][yy]
                        vis[xx][yy].room_s = vis[x][y]
                    else:
                        # We move S.
                        vis[x][y].room_s = vis[xx][yy]
                        vis[xx][yy].room_n = vis[x][y]

                if yy == y: 
                    # We moved E/W
                    if x > xx:
                        # We moved W
                        vis[x][y].room_w = vis[xx][yy]
                        vis[xx][yy].room_e = vis[x][y]
                    else:
                        # We moved E
                        vis[x][y].room_e = vis[xx][yy]
                        vis[xx][yy].room_w = vis[x][y]

                walk(xx, yy)

        walk(randrange(w), randrange(h))

        return vis

    def add_player(self, player):
        self.players.append(WorldPlayerController(self, player))

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
                if pos.room_n is None or (y == 0):
                    s += "+-"
                else:
                    s += "+ "
            s += '+\n'

            # Line 2, e, w
            for x in range(len(row[:-1])):
                pos = row[x]
                if pos.room_w is None or (x == 0):
                    s += "|"
                else:
                    s += " "

                # Is the player here?
                p = False
                for player in self.players:
                    if player.pos == pos:
                        p = True
                        s += dir_chars[player.direction]

                if not p:
                    s += " "

            s += '|\n'

        # Line 3, s
        for pos in row[:-1]:
            s += "+-"
        s += '+\n'

        return s

    def step(self):
        shuffle(self.players)
        for player in self.players:
            player.step()

 
if __name__ == '__main__':
    print(make_maze())
