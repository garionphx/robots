#!/usr/bin/env python

"""
***********************************
* COMMANDS
***********************************
FORWARD
LEFT
RIGHT


***********************************
* FLAGS
***********************************
BUMP


***********************************
* Branching
***********************************
BRANCH_BUMP <distance>
JUMP <distance>

"""

class Flags(object):
    def __init__(self):
        self.bump = False


class OpCode(object):
    def __init__(self, size, cycles, func = None):
        self.func = func
        self.size = size
        self.cycles = cycles

        self._data = None
        self._cycle_count = 0

    def set_data(self, data):
        self._data = data

    def step(self):
        # Returns True if the command executed

        # Step the cycle_count for this opcode
        self._cycle_count += 1

        if self._cycle_count == self.cycles:
            self._cycle_count = 0
            if self.func:
                if self._data:
                    self.func(self, self._data)
                else:
                    self.func(self)


class CPU(object):

    def __init__(self, program_file):
        self.program_file = program_file

        self.PC = 0
        self.flags = Flags()
        self.memory = []
        self.flag_set = False

        # Set up the op codes
        self.opcodes = {
            'FORWARD'       : OpCode(1, 1, self.forward),
            'LEFT'          : OpCode(1, 1, self.left),
            'RIGHT'         : OpCode(1, 1, self.right),
            'BRANCH_BUMP'   : OpCode(2, 1, self.branch_bump),
            'JUMP'          : OpCode(2, 1, self.jump),
            'RESET'         : OpCode(1, 1, self.reset),
            } 

    def reset_flags(self):
        if not self.flag_set:
            self.flags.bump = False

        self.flag_set = False

    def branch_bump(self, opcode, data):
        if self.flags.bump:
            self.PC += data[0]
        else:
            self.PC += opcode.size

        self.reset_flags()

    def jump(self, opcode, data):
        self.PC += data[0]
        self.reset_flags()

    def reset(self, opcode):
        self.PC = 0
        self.reset_flags()

    def forward(self, opcode):
        if self._forward_callback:
            self._forward_callback()

        self.PC += opcode.size
        self.reset_flags()

    def left(self, opcode):
        if self._left_callback:
            self._left_callback()

        self.PC += opcode.size
        self.reset_flags()

    def right(self, opcode):
        if self._right_callback:
            self._right_callback()

        self.PC += opcode.size
        self.reset_flags()

    def set_forward_callback(self, func):
        self._forward_callback = func

    def set_right_callback(self, func):
        self._right_callback = func

    def set_left_callback(self, func):
        self._left_callback = func

    def set_bump(self,value):
        self.flags.bump = value
        self.flag_set = True


    def compile(self):
        with open(self.program_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            for opcode in self.opcodes:
                if line.startswith(opcode):
                    data = line.split(' ')

                    # Store the opcode in memory
                    self.memory.append(self.opcodes[opcode])

                    # If we have a size, store that too
                    if self.opcodes[opcode].size == len(data):
                        self.memory += [ int(i) for i in data[1:]]

    def step(self):
        opcode = self.memory[self.PC]

        if opcode.size > 0:
            opcode.set_data(self.memory[self.PC + 1 : self.PC + opcode.size])

        opcode.step()



if __name__ == '__main__':
    def forward():
        print "FORWARD"

    def left():
        print "LEFT"

    def right():
        print "RIGHT"

    cpu = CPU("test.cpu")

    # Hook up the IO
    cpu.set_forward_callback(forward)
    cpu.set_right_callback(right)
    cpu.set_left_callback(left)

    cpu.compile()

    print cpu.PC
    cpu.step()      # FORWARD

    print cpu.PC
    cpu.step()      # BRANCH_BUMP

    print cpu.PC
    cpu.step()      # JUMP

    print cpu.PC
    cpu.step()      # FORWARD

    print cpu.PC
    cpu.set_bump(True)
    cpu.step()      # BRANCH_BUMP

    print cpu.PC
    cpu.step()      # RIGHT

    print cpu.PC
    cpu.step()      # RESET

    print cpu.PC
    cpu.step()      # FORWARD










