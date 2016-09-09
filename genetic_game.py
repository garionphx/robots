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
        for player in self.players:
            player.dist = 0
            player.survived = 0
            player.kills = 0

    def new_world(self):
        self.world = world.World(w = self.w, h = self.h)
        for player in self.players:
            # Reset the hitpoints.
            player.hitpoints = 2
            self.world.add_player("Player %d" % (len(self.world.players) + 1), player)

    def draw_world(self):
        return self.world.draw()

    def step(self):
        self.world.step()

    def run_game(self, count):
        for i in xrange(count):
            self.step()

        for player in self.world.players:
            # find this player in the game;s list of players.
            player.player.dist += player.distance_travelled
            player.player.survived += 1 if player.is_alive() else 0
            player.player.kills += player.kills

    def get_player_stats(self):
        for i in range(len(self.players)):
            print "-" * 20
            print "Player %d" % i
            player = self.players[i]
            print "Distance: %d" % player.dist
            print "Survived: %d" % player.survived
            print "Kills: %d" % player.kills


if __name__ == '__main__':
    game = GeneticGame(15,15)

    game.new_world()
    game.run_game(100000)
    print game.draw_world()
    game.get_player_stats()

