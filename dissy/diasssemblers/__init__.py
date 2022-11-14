from typing import List, Tuple

from enum import Enum, auto
from dissy.diasssemblers.x86_64 import disassemble as disassemble_x86_64

class NativeType(Enum):
    X86_64 = auto()


NATIVE_TO_DISASSEMBLER = {
    NativeType.X86_64: disassemble_x86_64,
}

JUMPS = ["JO", "JNO", "JS", "JNS", "JE", "JZ", "JNE", "JNZ"]

def disassemble(t, file) -> Tuple[List, List]:
    return NATIVE_TO_DISASSEMBLER[t](file)


def is_jump(instruction) -> int | None:
    # TODO : Move to x64 submodule
    if instruction.flowControl in ["FC_UNC_BRANCH", "FC_CND_BRANCH"]:
        return instruction.operands[0].value
    return None
