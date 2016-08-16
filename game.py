#!/usr/bin/env python

import os
import json
import BaseHTTPServer

import world
import player


class Game(object):
    def __init__(self, w = 0, h = 0):
        if w == 0 or h == 0:
            rows, columns = os.popen('stty size', 'r').read().split()
            self.world = world.World(w = ((int(columns)-1)/2), h = ((int(rows)-2)/2))
        else:
            self.world = world.World(w = w, h = h)

        for _ in range(3):
            self.world.add_player(player.Player("test.cpu", 2))

    def draw_world(self):
        return self.world.draw()

    def step(self):
        self.world.step()

class WebGame(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, w = 10, h = 10):
        self.w = w
        self.h = h
        self.world = world.World(w = w, h = h)

        for i in range(3):
            self.world.add_player("Player %d" % i, player.Player("test.cpu", 2))

        # create the webserver.
        self.server = BaseHTTPServer.HTTPServer(('', 8000), WebGameHandler)

    def getWorld(self):
        return self.world.world

    def getPlayers(self):
        return self.world.players

    def step(self):
        self.world.step()

class WebGameHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.handlers = {
            '/' : self.index,
            '/board' : self.board,
            '/players' : self.players,
            '/step' : self.step,
        }

        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def json_repr(self, obj):
        """Represent instance of a class as JSON.
        Arguments:
        obj -- any object
        Return:
        String that reprent JSON-encoded object.
        """
        def serialize(obj):
            """Recursively walk object's hierarchy."""
            if isinstance(obj, (bool, int, long, float, basestring)):
                return obj
            elif isinstance(obj, world.Pos):
                return serialize( { 'n':obj.room_n is not None,
                                    'e':obj.room_e is not None,
                                    'w':obj.room_w is not None,
                                    's':obj.room_s is not None} )
            elif isinstance(obj, world.WorldPlayerController):
                return serialize( {'distance' : obj.distance_travelled,
                                   'hits' : obj.hits,
                                   'hitpoints': obj.player.hitpoints,
                                   'name': obj.name,
                                   'x' : obj.pos.x,
                                   'y' : obj.pos.y,
                                   'dir' : obj.direction } )
            elif isinstance(obj, dict):
                obj = obj.copy()
                for key in obj:
                    obj[key] = serialize(obj[key])
                return obj
            elif isinstance(obj, list):
                return [serialize(item) for item in obj]
            elif isinstance(obj, tuple):
                return tuple(serialize([item for item in obj]))
            elif hasattr(obj, '__dict__'):
                return serialize(obj.__dict__)
            else:
                return repr(obj) # Don't know how to handle, convert to string
        return json.dumps(serialize(obj))

    def index(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('game.html', 'r') as f:
            self.wfile.write(f.read())

    def board(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data = (game.w, game.h, game.getWorld())
        self.wfile.write(self.json_repr(data))

    def players(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(self.json_repr(game.getPlayers()))

    def step(self):
        game.step()
        self.send_response(200)
        

    def do_GET(self):
        if self.path in self.handlers:
            return self.handlers[self.path]()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('not found')



game = WebGame(15,15)
if __name__ == '__main__':
    import time

    game.server.serve_forever()
    #print game.draw_world()

    i = 1
    while 1:
        #if len(game.world.players) <= 5:
        #    break
        time.sleep(.25)
        game.step()
        print game.draw_world()
        if i % 100 == 0:
            print "Number left:", len(game.world.players), "Iterations:", i
        i += 1

    print "Game won after", i, "iterations"
