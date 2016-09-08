import time

import world
import player
import random_player
import genetic_player
import assembler

class GeneticGame(object):
    def __init__(self, w = 0, h = 0):
        self.w = w
        self.h = h
        
        self.players = [genetic_player.GeneticPlayer(2) for _ in range(10)]

    def new_world(self):
        self.world = world.World(w = self.w, h = self.h)
        for player in self.players:
            self.world.add_player("Player %d" % (len(self.world.players) + 1), player)

    def draw_world(self):
        return self.world.draw()

    def step(self):
        self.world.step()

    def run_game(self, count):
        for i in xrange(count):
            self.step()


if __name__ == '__main__':
    game = GeneticGame(15,15)

    game.new_world()
    game.run_game(100000)
    print game.draw_world()

