from rich.text import Text
import dissy.disassemblers.x86_64 as x86_64
import dissy.disassemblers.python as python_dis
from dissy.disassemblers.types import NativeType, DisassembledImage

NATIVE_TO_DISASSEMBLER = {
    NativeType.X86_64: x86_64.disassemble,
    NativeType.PYTHON: python_dis.disassemble,
}

def disassemble(t, file) -> DisassembledImage:
    return NATIVE_TO_DISASSEMBLER[t](file)


def is_jump(t: NativeType, instruction) -> int | None:
    if t == NativeType.X86_64:
        return x86_64.is_jump(instruction)
    elif t == NativeType.PYTHON:
        return python_dis.is_jump(instruction)
    else:
        raise NotImplementedError


def format_instruction(t, instruction, related=None) -> Text:
    if t == NativeType.X86_64:
        return x86_64.format_instruction(instruction, related)
    elif t == NativeType.PYTHON:
        return python_dis.format_instruction(instruction, related)
    else:
        raise NotImplementedError


def format_offset(t: NativeType, offset: int) -> Text:
    if t == NativeType.X86_64:
        return Text("%.8x" % offset)
    elif t == NativeType.PYTHON:
        return Text("%d" % offset)
    raise NotImplementedError