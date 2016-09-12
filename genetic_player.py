import player_base
import random_player
import random
import cpu
import assembler

class Chromosome(object):
    def __init__(self, data, weight):
        self.data = data
        self.weight = weight

class GeneticPlayer(player_base.PlayerBase):
    def __init__(self, hitpoints, chromosomes=[]):
        if chromosomes:
            self.chromosomes = chromosomes
            self.memory = [i for chrom in self.chromosomes for i in chrom.data]
        else:
            rand_player = random_player.RandomPlayer(hitpoints)
            self.memory = rand_player.memory

            # Make chromosomes. Figure average size of a chromosome to be
            # 10 (need to check and see if the last one is a branch, if so, then
            # we need to add one.). 20 being the largest, min of 2.
            num_chroms = len(self.memory) / 10
            chunks = []
            while sum(chunks) < len(self.memory):
                randmax = min(20, (len(self.memory) - sum(chunks)))
                if randmax > 2:
                    chunks.append(random.randint(2, randmax))
                else:
                    chunks.append(randmax)

            assert sum(chunks) == len(self.memory)

            offset = 0
            self.chromosomes = []

            for i in range(len(chunks)):
                if chunks[i]:
                    mem = self.memory[offset:offset + chunks[i]]

                    # Validate the possible chromosome.
                    test_cpu = cpu.CPU(mem)
                    adjust = test_cpu.validate_mem()
                    if adjust:
                        chunks[i] += adjust
                        chunks[i+1] -= adjust
                        mem = self.memory[offset:offset + chunks[i]]

                    self.chromosomes.append(Chromosome(mem, 0))

                    offset += chunks[i]

            assert len(chunks) == len(self.chromosomes)

        super(self.__class__, self).__init__(hitpoints, self.memory)

    def add_weight(self, value):
        for c in self.chromosomes:
            c.weight += value

    def write(self, path, name):
        with open("%s/%s.data" % (path, name), 'w') as f:
            f.write("# Chromosomes\n")
            f.write("# -----------\n")
            for chromo in self.chromosomes:
                f.write("# data: %s\n" % (str(chromo.data), ))
                f.write("# weight: %d\n" % (chromo.weight, ))
                f.write("# - \n")

            f.write("\n")

            f.write("Code\n")
            f.write("----\n")
            disassem = assembler.Disassembler()
            f.write(disassem.disassemble(self.cpu.memory))

            f.write("\n")
            f.write("Results\n")
            f.write("-------\n")
            f.write("Distance: %d\n" % self.dist)
            f.write("Kills: %d\n" % self.kills)
            f.write("Survived: %d\n" % self.survived)


if __name__ == '__main__':
    player = GeneticPlayer(7)


