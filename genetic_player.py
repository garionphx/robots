import player_base
import random_player
import random

class GeneticPlayer(player_base.PlayerBase):
    def __init__(self, hitpoints, chromosomes=[]):
        if chromosomes:
            self.chromosomes = chromosomes
            self.memory = [i for chrom in self.chromosomes for i in chrom]
        else:
            rand_player = random_player.RandomPlayer(hitpoints)
            self.memory = rand_player.memory

            # Make chromosomes. Figure average size of a chromosome to be
            # 10 (need to check and see if the last one is a branch, if so, then
            # we need to add one.). 20 being the largest, min of 1.
            num_chroms = len(self.memory) / 10
            chunks = []
            while sum(chunks) < len(self.memory):
                randmax = min(20, (len(self.memory) - sum(chunks)))
                if randmax:
                    chunks.append(random.randint(1, randmax))

            assert sum(chunks) == len(self.memory)

            offset = 0
            self.chromosomes = []
            for chunk in chunks:
                self.chromosomes.append(self.memory[offset:offset + chunk])
                offset += chunk

            assert len(chunks) == len(self.chromosomes)

        super(self.__class__, self).__init__(hitpoints, self.memory)


if __name__ == '__main__':
    player = GeneticPlayer(7)


