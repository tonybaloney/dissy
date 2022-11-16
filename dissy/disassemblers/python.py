from dissy.disassemblers.types import DisassembledImage, NativeType
import dis
import opcode
from typing import Iterable
from rich.text import Text


TOKEN_COLORS = {
    "TOKEN_INSTRUCTION": "green",
    "TOKEN_NAME": "blue",
    "TOKEN_NAME_HIGHLIGHT": "cyan2",
    "TOKEN_NUMBER": "magenta",
    "TOKEN_DELIMITER": "white",
}

def disassemble(x, position=None) -> DisassembledImage:
    instructions_iter: Iterable[dis.Instruction] = dis.get_instructions(x, first_line=position)
    offsets = []
    instructions = []
    for i in instructions_iter:
        instructions.append(i)
        offsets.append(i.offset)

    return DisassembledImage(instructions=instructions, offsets=offsets, entry_point=position, native_type=NativeType.PYTHON, info=dis.code_info(x))


def format_instruction(instruction: dis.Instruction, related=None) -> Text:
    result = Text(instruction.opname, style=TOKEN_COLORS["TOKEN_INSTRUCTION"])
    if instruction.argval is not None:
        result += Text(" ", style=TOKEN_COLORS["TOKEN_DELIMITER"])
        result += Text(instruction.argrepr, style=TOKEN_COLORS["TOKEN_NAME_HIGHLIGHT"])
    return result


def is_jump(instruction: dis.Instruction) -> int | None:
    if not instruction:
        return None
    if instruction.opcode in opcode.hasjabs or instruction.opcode in opcode.hasjrel:
        return instruction.argval

    return None
