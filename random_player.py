#!/usr/bin/env python

import random

import assembler # to get the opcodes and type of instruction
import player_base

class RandomPlayer(player_base.PlayerBase):
    def __init__(self, hitpoints):
        length = random.randint(1,1024)

        self.memory = []
        for i in range(length):

            opcode = random.randint(0, len(assembler.reverse_map) - 1)
            self.memory.append(opcode)

            #  if its a branching opcode, select a range to jump
            if isinstance(assembler.reverse_map[opcode][1], assembler.BranchInstruction):
                jumplength = random.randint(-128, 127)
                self.memory.append(jumplength)

        super(self.__class__, self).__init__(hitpoints, self.memory)

if __name__ == '__main__':
    player = RandomPlayer(7)
    dis = assembler.Disassembler()
    prg = dis.disassemble(player.memory)
    print prg

