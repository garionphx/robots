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

    def reset(self):
        self.bump = False


class OpCode(object):
    def __init__(self, cycles, func):
        self.func = func
        self.cycles = cycles

        self._data = None
        self._cycle_count = 0

    def set_data(self, data):
        self._data = data

    def step(self):
        # Step the cycle_count for this opcode
        self._cycle_count += 1

        if self._cycle_count == self.cycles:
            self._cycle_count = 0
            self.func()

class CPUFault(Exception):
    pass

class CPU(object):

    def __init__(self, memory):
        self.PC = 0
        self.flags = Flags()
        self.memory = memory
        self.flag_set = False

        self.instructionset = ( OpCode(1, self.forward),
                                OpCode(1, self.left),      
                                OpCode(1, self.right),     
                                OpCode(1, self.branch_bump),
                                OpCode(1, self.clear_bump),
                                OpCode(1, self.jump),      
                                OpCode(1, self.reset),     
                                OpCode(1, self.fire),
                              )
        self.instructionset_length = len(self.instructionset)

        self._fire_callback =       None
        self._forward_callback =    None
        self._right_callback =      None
        self._left_callback =       None

    def branch_bump(self):
        if self.flags.bump:
            # Get the data in the next memory location
            branch_amount = self.memory[self.PC + 1]

            if branch_amount < -128 or branch_amount > 127:
                raise CPUFault("branch out of range %d:%d" % (self.PC, branch_amount))

            # do the jump, but -1 because we'll inc the PC counter when we exit this.
            self.PC += (branch_amount - 1)
        else:
            self.PC += 1 # Skip the branch_amount

    def clear_bump(self):
        self.flags.bump = False

    def jump(self):
        branch_amount = self.memory[self.PC + 1]

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
        PC = self.PC
        if PC < 0 or PC >= len(self.memory):
            self.PC = PC = 0
            self.flags.reset()

        memory = self.memory[PC]
        if memory < 0 or memory >= self.instructionset_length:
            self.PC = PC = 0
            self.flags.reset()
            memory = self.memory[PC]

        try:
            opcode = self.instructionset[memory]
        except:
            print "PC", self.PC
            print "memory", self.memory[self.PC]
            raise
        opcode.step()
        self.PC += 1

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
