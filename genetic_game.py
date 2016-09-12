import time
import random
import os
import copy
import argparse
import sys


import world
import player
import random_player
import genetic_player
import assembler
import cpu

class GeneticGame(object):
    def __init__(self, w, h, players):
        self.w = w
        self.h = h
        
        self.players = players
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

        for world_player in self.world.players:
            # Copy the results down to the player itself.
            world_player.player.dist += world_player.distance_travelled
            world_player.player.survived += 1 if world_player.is_alive() else 0
            world_player.player.kills += world_player.kills

    def get_winners(self):
        def find_winners(attr_func):
            winners = []
            curr_value = 0
            for p in self.players:
                value = attr_func(p)
                if not value:
                    continue

                if value > curr_value:
                    curr_value = value
                    winners = [p]
                    continue

                if value == curr_value:
                    winners.append(p)

            return winners

        return find_winners(lambda p:p.dist), find_winners(lambda p:p.survived), find_winners(lambda p:p.kills) 


        #for i in range(len(self.players)):
        #    print "-" * 20
        #    print "Player %d" % i
        #    player = self.players[i]
        #    print "Distance: %d" % player.dist
        #    print "Survived: %d" % player.survived
        #    print "Kills: %d" % player.kills

def mutate_insert_opcode(chromo):
    i = 0
    if chromo.data:
        # Get a list of 'safe' indexes we can insert at.
        test_cpu = cpu.CPU(chromo.data)
        indexes = test_cpu.index_mem()

        # Insert it where?
        i = orig_i = random.choice(indexes)

    # Generate an opcode to insert
    opcode = random.randint(0, len(cpu.instructionset) - 1)
    chromo.data.insert(i, opcode)

    # Generate any extra needed for this opcode.
    for _ in range(cpu.instructionset[opcode].extradata_len):
        i += 1
        jumplength = random.randint(-128, 127)
        chromo.data.insert(i, jumplength)

def mutate_remove_opcode(chromo):
    # If the chromo is empty, do nothing.
    if not chromo.data:
        return

    # Get a list of 'safe' indexes we can insert at.
    test_cpu = cpu.CPU(chromo.data)
    indexes = test_cpu.index_mem()

    # Insert it where?
    i = orig_i = random.choice(indexes)

    opcode = chromo.data[i]
    chromo.data.pop(i)

    # Remove any extra data for this opcode.
    for _ in range(cpu.instructionset[opcode].extradata_len):
        chromo.data.pop(i)

    # If its empty, reset the weight so it'll get eliminated someday.
    if not chromo.data:
        chromo.weight = 0

def mutate(chromo):
    # 5% chance of mutation
    chance = random.randint(1,100)
    if chance <= 5:
        # select a mutation
        mutations = [ mutate_insert_opcode,
                      mutate_remove_opcode ]

        func = random.choice(mutations)
        func(chromo)

def mutate_order(chromosomes):
    chance = random.randint(1,100)
    if chance <= 2:
        a = random.randint(0, len(chromosomes) -1)
        b = random.randint(0, len(chromosomes) -1)

        if a != b:
            chromosomes[a], chromosomes[b] = chromosomes[b], chromosomes[a]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_players", action='store', default=10)
    parser.add_argument("--num_generations", action='store', default=10)
    parser.add_argument("--num_games_per_generation", action='store', default=10)
    parser.add_argument("--num_steps_per_game", action='store', default=100000)

    args = parser.parse_args()

    players = [genetic_player.GeneticPlayer(2) for _ in range(int(args.num_players))]

    for generation in range(int(args.num_generations)):
        print "Running generation %d" % generation
        game = GeneticGame(15,15, players)

        # Run 10 games
        for i in range(int(args.num_games_per_generation)):
            print "\tRunning game %d" % i
            game.new_world()
            game.run_game(int(args.num_steps_per_game))

        # Write the players out for study.
        out_path = "./generation_%d" % (generation, )
        os.mkdir(out_path)
        for i in range(len(game.world.players)):
            players[i].write(out_path, "player_%d" % i)

        # Get the winners
        dist_winners, survival_winners, kill_winners = game.get_winners()

        # Add weights for the better players
        for p in dist_winners:
            p.add_weight(2)
        for p in kill_winners:
            p.add_weight(3)

        # From the winners generate 10 new children
        new_players = []
        for _ in range(10):
            # Pick 2 winners
            a = random.choice(players)
            b = random.choice(players)

            def random_weighted(a,b):
                total = 1 + a.weight + b.weight
                r = random.randint(1,total)
                if r > a.weight:
                    return b
                return a

            # Copy the chromosome, so we get indiviually mutated ones. Otherwise,
            # if we mutuate one, it would mutate all copys of that chromosome
            new_chromosomes = [copy.copy(random_weighted(c[0], c[1]))  for c in zip(a.chromosomes, b.chromosomes)]

            if len(a.chromosomes) > len(new_chromosomes):
                new_chromosomes += a.chromosomes[len(new_chromosomes):]

            if len(b.chromosomes) > len(new_chromosomes):
                new_chromosomes += b.chromosomes[len(new_chromosomes):]

            # Now mutate individual chromosomes.
            for chromo in new_chromosomes:
                mutate(chromo)

            # Mutate the order
            mutate_order(new_chromosomes)

            # Create the new player
            new_players.append(genetic_player.GeneticPlayer(2, new_chromosomes))

        players = new_players

    # Get the code from the player
    disassem = assembler.Disassembler()
    print disassem.disassemble(players[0].cpu.memory)


