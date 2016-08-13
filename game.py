#!/usr/bin/env python

import world
import player
import os

class Game(object):
    def __init__(self, w = 0, h = 0):
        if w == 0 or h == 0:
            rows, columns = os.popen('stty size', 'r').read().split()
            self.world = world.World(w = ((int(columns)-1)/2), h = ((int(rows)-2)/2))
        else:
            self.world = world.World(w = w, h = h)

        for _ in range(1):
            self.world.add_player(player.Player("test.cpu", 2))

    def draw_world(self):
        return self.world.draw()

    def step(self):
        self.world.step()

if __name__ == '__main__':
    import time

    game = Game(10,10)
    print game.draw_world()

    i = 1
    while 1:
        #if len(game.world.players) <= 5:
        #    break
        time.sleep(1)
        game.step()
        print game.draw_world()
        if i % 100 == 0:
            print "Number left:", len(game.world.players), "Iterations:", i
        i += 1

    print "Game won after", i, "iterations"
