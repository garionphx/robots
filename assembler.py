#class OpCode(Symbol):
#    grammar = Enum(K("FORWARD"),
#                   K("LEFT"),
#                   K("RIGHT"),
#                   K("FIRE"),
#                   K("BRANCH_BUMP"),
#                   K("RESET"),
#                   K("LABEL"),
#                  )

class Instruction(object):
    def __init__(self, opcode, size):
        self.opcode = opcode
        self.size = size

class SimpleInstruction(Instruction):
    def __init__(self, opcode):
        super(self.__class__, self).__init__(opcode, 1)

class BranchInstruction(Instruction):
    def __init__(self, opcode):
        super(self.__class__, self).__init__(opcode, 2)

class AssembleError(Exception):
    pass

instruction_map = {
    'FORWARD'       : SimpleInstruction(0),
    'LEFT'          : SimpleInstruction(1),
    'RIGHT'         : SimpleInstruction(2),
    'BRANCH_BUMP'   : BranchInstruction(3),
    'CLEAR_BUMP'    : SimpleInstruction(4),
    'JUMP'          : SimpleInstruction(5),
    'RESET'         : SimpleInstruction(6),
    'FIRE'          : SimpleInstruction(7),
    }

reverse_map = { instruction_map[k].opcode : (k, instruction_map[k]) for k in instruction_map }


class Assembler(object):

    def __init__(self):
        self.assembler_instructions = {
            'LABEL' : self.label_handler,
            }

        # Stores the label_name:offset
        self.labels = {}

    def label_handler(self, pieces, offset):
        self.labels[pieces[1]] = offset

    def compile(self, program_file):
        memory = []

        with open(program_file, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line or line[0] == '#':
                continue

            pieces = line.split(' ')
            if pieces[0] in instruction_map:
                ins = instruction_map[pieces[0]]

                memory.append(ins.opcode)

                if ins.size > 1:
                    for i in range(1, ins.size):
                        data = pieces[i]
                        try:
                            data = int(data)

                            if data < -128 or data > 127:
                                raise AssembleError("Jump out of range")

                        except ValueError:
                            # assume its a label
                            pass

                        memory.append(data)

            elif pieces[0] in self.assembler_instructions:
                self.assembler_instructions[pieces[0]](pieces, len(memory))

            else:
                raise AssembleError("Unknown instruction: %s" % line)

            # Pass 2, set any labels.
            for i in range(len(memory)):
                if isinstance(memory[i], str):
                    if data in self.labels:
                        memory[i] = self.labels[data] - (i - 1)

        return memory

class Disassembler(object):
    def disassemble(self, memory):
        prg = ""
        iterator = iter(range(len(memory)))
        for i in iterator:
            opcode = memory[i]
            if opcode in reverse_map:
                prg += reverse_map[opcode][0]
                if reverse_map[opcode][1].size == 2:
                    i = iterator.next()
                    prg += " " + str(memory[i])
            else:
                prg += "** UNKNOWN OPCODE %s" % opcode

            prg += '\n'

        return prg



if __name__ == '__main__':
    asm = Assembler()
    mem = asm.compile('test.cpu')
    print mem

    dis = Disassembler()
    prg = dis.disassemble(mem)
    print prg
