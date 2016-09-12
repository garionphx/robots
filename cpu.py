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
import sys

class Flags(object):
    def __init__(self):
        self.bump = False

    def reset(self):
        self.bump = False


class OpCode(object):
    def __init__(self, cycles, func, extradata_len = 0):
        self.func = func
        self.cycles = cycles
        self.extradata_len = extradata_len

        self._cycle_count = 0
        self.cpu = None

    def step(self, cpu):
        # Step the cycle_count for this opcode
        self._cycle_count += 1

        if self._cycle_count == self.cycles:
            self._cycle_count = 0
            self.func(cpu)
            return True

class CPUFault(Exception):
    pass

class CPU(object):

    def __init__(self, memory):
        self.PC = 0
        self.flags = Flags()
        self.memory = memory

        self.instructionset = instructionset
        self.instructionset_length = len(self.instructionset)

        self._fire_callback =       None
        self._forward_callback =    None
        self._right_callback =      None
        self._left_callback =       None

    def validate_mem(self):
        pc = 0
        while pc < len(self.memory):
            pc += 1 + self.instructionset[self.memory[pc]].extradata_len

        # Return the number of bytes needed to make this memory valid
        return pc - len(self.memory)

    def index_mem(self):
        if not self.memory:
            return []

        pc = 0
        indexes = [0]
        while pc < len(self.memory):
            pc += 1 + self.instructionset[self.memory[pc]].extradata_len
            indexes.append(pc)

        return indexes[:-1]

    def branch_bump(self):
        if self.flags.bump:
            # Get the data in the next memory location
            try:
                branch_amount = self.memory[self.PC + 1]
            except IndexError:
                print "** EXCEPTION BUMP PC: ", self.PC
                print "** EXCEPTION BUMP PC + 1: ", self.PC + 1
                print "** EXCEPTION len: ", len(self.memory)
                sys.exit()

            if branch_amount < -128 or branch_amount > 127:
                raise CPUFault("branch out of range %d:%d" % (self.PC, branch_amount))

            # do the jump, but -1 because we'll inc the PC counter when we exit this.
            self.PC += (branch_amount - 1)
        else:
            self.PC += 1 # Skip the branch_amount

    def clear_bump(self):
        self.flags.bump = False

    def jump(self):
        try:
            branch_amount = self.memory[self.PC + 1]
        except IndexError:
            print "** EXCEPTION JUMP PC: ", self.PC
            print "** EXCEPTION JUMP PC + 1: ", self.PC + 1
            print "** EXCEPTION len: ", len(self.memory)
            sys.exit()

        if branch_amount < -128 or branch_amount > 127:
            raise CPUFault("branch out of range %d:%d" % (self.PC, branch_amount))

        # do the jump, but -1 because we'll inc the PC counter when we exit this.
        self.PC += (branch_amount - 1)

    def reset(self):
        self.PC = -1 # Because we'll inv the PC when we exit this
        self.flags.reset()

    def forward(self):
        if self._forward_callback:
            self._forward_callback()

    def left(self):
        if self._left_callback:
            self._left_callback()

    def right(self):
        if self._right_callback:
            self._right_callback()

    def fire(self):
        if self._fire_callback:
            self._fire_callback()

    def set_forward_callback(self, func):
        self._forward_callback = func

    def set_right_callback(self, func):
        self._right_callback = func

    def set_left_callback(self, func):
        self._left_callback = func

    def set_fire_callback(self, func):
        self._fire_callback = func

    def set_bump(self,value):
        self.flags.bump = value

    def step(self):
        try:
            if self.PC < 0:
                self.PC = 0
            memory = self.memory[self.PC]
            opcode = self.instructionset[memory]
        except IndexError:
            self.PC = 0
            self.flags.reset()
            memory = self.memory[self.PC]
            opcode = self.instructionset[memory]

        try:
            if opcode.step(self):
                self.PC += 1
        except Exception, e:
            print "PC", self.PC
            print "memory", self.memory[self.PC]
            print "memory: ", self.memory
            print e
            raise


instructionset = ( OpCode(1, CPU.forward),
                   OpCode(1, CPU.left),      
                   OpCode(1, CPU.right),     
                   OpCode(1, CPU.branch_bump, 1), # 3
                   OpCode(1, CPU.clear_bump),
                   OpCode(1, CPU.jump, 1),        # 5
                   OpCode(1, CPU.reset),     
                   OpCode(1, CPU.fire),
                 )


if __name__ == '__main__':
    def forward():
        print("FORWARD")

    def left():
        print("LEFT")

    def right():
        print("RIGHT")

    old = False
    if old:
        cpu = CPU("test.cpu")

        # Hook up the IO
        cpu.set_forward_callback(forward)
        cpu.set_right_callback(right)
        cpu.set_left_callback(left)

        cpu.compile()

        print(cpu.PC)
        cpu.step()      # FORWARD

        print(cpu.PC)
        cpu.step()      # BRANCH_BUMP

        print(cpu.PC)
        cpu.step()      # JUMP

        print(cpu.PC)
        cpu.step()      # FORWARD

        print(cpu.PC)
        cpu.set_bump(True)
        cpu.step()      # BRANCH_BUMP

        print(cpu.PC)
        cpu.step()      # RIGHT

        print(cpu.PC)
        cpu.step()      # RESET

        print(cpu.PC)
        cpu.step()      # FORWARD

    else:
        import assembler
        asm = assembler.Assembler()
        mem = asm.compiler("test.cpu")
        cpu = CPU(mem)
        cpu.run()
