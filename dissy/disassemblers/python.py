import dis
import sys
from typing import Iterable

import opcode
from rich.text import Text

from dissy.disassemblers.types import DisassembledImage, NativeType

TOKEN_COLORS = {
    "TOKEN_INSTRUCTION": "green",
    "TOKEN_NAME": "blue",
    "TOKEN_NAME_HIGHLIGHT": "cyan2",
    "TOKEN_NUMBER": "magenta",
    "TOKEN_DELIMITER": "white",
}


def disassemble(
    x, position=None, show_caches=False, adaptive=False
) -> DisassembledImage:
    if sys.version_info >= (3, 11):
        instructions_iter: Iterable[dis.Instruction] = dis.get_instructions(
            x, first_line=position, show_caches=show_caches, adaptive=adaptive
        )
    else:
        instructions_iter: Iterable[dis.Instruction] = dis.get_instructions(
            x, first_line=position
        )
    offsets = []
    instructions = []
    for i in instructions_iter:
        instructions.append(i)
        offsets.append(i.offset)

    return DisassembledImage(
        instructions=instructions,
        offsets=offsets,
        entry_point=position,
        native_type=NativeType.PYTHON,
        info=dis.code_info(x),
    )


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
