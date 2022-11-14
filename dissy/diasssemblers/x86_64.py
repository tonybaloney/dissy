import distorm3
from typing import Tuple, List


def disassemble(file, position=0) -> Tuple[List, List]:
    with open(file, 'rb') as f:
        iterable = distorm3.DecomposeGenerator(position, f.read(), distorm3.Decode64Bits)

        offsets = []
        instructions = []
        for instruction in iterable:
            offsets.append(instruction.address)
            instructions.append(instruction)    

        return (offsets, instructions)
