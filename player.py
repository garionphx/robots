#!/usr/bin/env python

import cpu

class Player(object):
    def __init__(self, program):
        self.cpu = cpu.CPU(program)
        self.cpu.compile()

        # Hook up the io
        self.cpu.set_forward_callback(self.forward)
        self.cpu.set_left_callback(self.left)
        self.cpu.set_right_callback(self.right)

    def set_forward(self, forward):
        self._forward = forward
    def forward(self):
        self._forward()

    def set_right(self, right):
        self._right = right
    def right(self):
        self._right()

    def set_left(self, left):
        self._left = left
    def left(self):
        self._left()

    def bump(self):
        self.cpu.set_bump(True)

    def step(self):
        self.cpu.step()
