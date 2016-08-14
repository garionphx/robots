#!/usr/bin/env python

import assembler
import player_base

class Player(player_base.PlayerBase):
    def __init__(self, program, hitpoints):
        asm = assembler.Assembler()

        super(self.__class__, self).__init__(hitpoints, asm.compile(program))

