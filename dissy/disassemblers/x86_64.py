try:
    import distorm3
except ImportError:
    raise ImportError(
        "distorm3 is not installed. Please install it with 'pip install distorm3'"
    )
from rich.text import Text

from dissy.disassemblers.types import DisassembledImage, NativeType

TOKEN_COLORS = {
    "TOKEN_INSTRUCTION": "green",
    "TOKEN_NAME": "blue",
    "TOKEN_NAME_HIGHLIGHT": "cyan2",
    "TOKEN_NUMBER": "magenta",
    "TOKEN_DELIMITER": "white",
}


def disassemble(file, position=0) -> DisassembledImage:
    with open(file, "rb") as f:
        iterable = distorm3.DecomposeGenerator(
            position, f.read(), distorm3.Decode64Bits
        )

        offsets = []
        instructions = []
        for instruction in iterable:
            offsets.append(instruction.address)
            instructions.append(instruction)

        return DisassembledImage(
            instructions=instructions,
            offsets=offsets,
            entry_point=position,
            native_type=NativeType.X86_64,
        )


def is_jump(instruction) -> int | None:
    if not instruction:
        return None
    if instruction.flowControl in ["FC_UNC_BRANCH", "FC_CND_BRANCH"]:
        return instruction.operands[0].value
    return None


def operand_as_text(operand, highlight_names) -> Text:
    if operand.type == distorm3.OPERAND_IMMEDIATE:
        if operand.value >= 0:
            return Text("0x%x" % operand.value, style=TOKEN_COLORS["TOKEN_NUMBER"])
        else:
            return Text(
                "-0x%x" % abs(operand.value), style=TOKEN_COLORS["TOKEN_NUMBER"]
            )
    elif operand.type == distorm3.OPERAND_REGISTER:
        return Text(
            operand.name,
            style=TOKEN_COLORS["TOKEN_NAME_HIGHLIGHT"]
            if operand.name in highlight_names
            else TOKEN_COLORS["TOKEN_NAME"],
        )
    elif operand.type == distorm3.OPERAND_ABSOLUTE_ADDRESS:
        return Text("[0x%x]" % operand.disp, style=TOKEN_COLORS["TOKEN_NUMBER"])
    elif operand.type == distorm3.OPERAND_FAR_MEMORY:
        return Text(f"{hex(operand.seg)}:{hex(operand.off)}", style="yellow")
    elif operand.type == distorm3.OPERAND_MEMORY:
        result = Text("[", style=TOKEN_COLORS["TOKEN_DELIMITER"])
        if operand.base is not None:
            result += Text(
                distorm3.Registers[operand.base],
                style=TOKEN_COLORS["TOKEN_NAME_HIGHLIGHT"]
                if distorm3.Registers[operand.base] in highlight_names
                else TOKEN_COLORS["TOKEN_NAME"],
            ) + Text("+", style=TOKEN_COLORS["TOKEN_DELIMITER"])
        if operand.index is not None:
            result += Text(
                distorm3.Registers[operand.index],
                style=TOKEN_COLORS["TOKEN_NAME_HIGHLIGHT"]
                if distorm3.Registers[operand.index] in highlight_names
                else TOKEN_COLORS["TOKEN_NAME"],
            )
            if operand.scale > 1:
                result += Text(
                    "*%d" % operand.scale, style=TOKEN_COLORS["TOKEN_NUMBER"]
                )
        if operand.disp >= 0:
            result += Text("+0x%x" % operand.disp, style=TOKEN_COLORS["TOKEN_NUMBER"])
        else:
            result += Text(
                "-0x%x" % abs(operand.disp), style=TOKEN_COLORS["TOKEN_NUMBER"]
            )
        return result + Text("]", style=TOKEN_COLORS["TOKEN_DELIMITER"])


def format_instruction(instruction, related=None) -> Text:
    t = Text(instruction.mnemonic, style=TOKEN_COLORS["TOKEN_INSTRUCTION"])
    if related:
        highlight_names = [
            r.name for r in related.operands if r.type == distorm3.OPERAND_REGISTER
        ]
        highlight_names.extend(
            [
                distorm3.Registers[r.base]
                for r in related.operands
                if r.type == distorm3.OPERAND_MEMORY and r.base is not None
            ]
        )
        highlight_names.extend(
            [
                distorm3.Registers[r.index]
                for r in related.operands
                if r.type == distorm3.OPERAND_MEMORY and r.index is not None
            ]
        )
    else:
        highlight_names = []

    if len(instruction.operands) > 0:
        t.append(" ")
        args = Text(", ").join(
            operand_as_text(operand, highlight_names=highlight_names)
            for operand in instruction.operands
        )
        t.append(args)
    return t
