from dissy.disassemblers.types import DisassembledImage, NativeType
import dis
from typing import Iterable

TOKEN_COLORS = {
    "TOKEN_INSTRUCTION": "green",
    "TOKEN_NAME": "blue",
    "TOKEN_NAME_HIGHLIGHT": "cyan2",
    "TOKEN_NUMBER": "magenta",
    "TOKEN_DELIMITER": "white",
}

def disassemble(file, position=0) -> DisassembledImage:
    instructions: Iterable[dis.Instruction] = dis.get_instructions(file, first_line=position)
    offsets = []
    instructions = []
    for i in instructions:
        instructions.append(i)
        offsets.append(i.offset)

        return DisassembledImage(instructions=instructions, offsets=offsets, entry_point=position, native_type=NativeType.PYTHON)
