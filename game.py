#!/usr/bin/env python

import world
import player

class Game(object):
    def __init__(self):
        self.world = world.World(w = 80, h = 14)

        for _ in range(30):
            self.world.add_player(player.Player("test.cpu"))

    def draw_world(self):
        return self.world.draw()

    def step(self):
        self.world.step()

if __name__ == '__main__':
    import time

    game = Game()
    print game.draw_world()

    while 1:
        time.sleep(.05)
        game.step()
        print game.draw_world()
