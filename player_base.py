#!/usr/bin/env python

import cpu

class PlayerBase(object):
    def __init__(self, hitpoints, program):
        self.cpu = cpu.CPU(program)

        self.hitpoints = hitpoints

        # Hook up the io
        self.cpu.set_forward_callback(self.forward)
        self.cpu.set_left_callback(self.left)
        self.cpu.set_right_callback(self.right)
        self.cpu.set_fire_callback(self.fire)

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

    def set_fire(self, fire):
        self._fire = fire
    def fire(self):
        self._fire()

    def bump(self):
        self.cpu.set_bump(True)

    def hit(self):
        self.hitpoints -= 1

    def step(self):
        if self.hitpoints > 0:
            self.cpu.step()

    def is_alive(self):
        return self.hitpoints > 0


