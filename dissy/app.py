from textual.app import App, ComposeResult 
from textual.widgets import Header, Footer, DataTable
from textual.reactive import Reactive
from typing import List
from rich.text import Text


from dissy.disassemblers import disassemble, is_jump, format_instruction
from dissy.disassemblers.types import NativeType, DisassembledImage

import click


class InstructionView(DataTable):
    image: Reactive[DisassembledImage] = Reactive([])

    def watch_cursor_cell(self, old, value) -> None:
        prev_instruction = self.image.instructions[old.row] if old else None
        instruction = self.image.instructions[value.row] if value else None

        ELBOW_TOP = "╭"
        ELBOW_BOTTOM = "╰"
        LINE_MIDDLE = "│"
        jump_to = None
        if jmp := is_jump(self.image.native_type, instruction):
            try:
                jump_to = self.image.offsets.index(jmp)
                self.data[value.row][1] = ELBOW_TOP
                self.data[jump_to][0].stylize("bold magenta")
                self.data[jump_to][1] = ELBOW_BOTTOM
                self.refresh_cell(jump_to, 0)
            except ValueError:
                pass

        if jmp := is_jump(self.image.native_type, prev_instruction):
            try:
                offset_row = self.image.offsets.index(jmp)
                self.data[offset_row][0] = Text(self.data[offset_row][0].plain)
                self.refresh_cell(offset_row, 0)
            except ValueError:
                pass

        # Find related registers
        for idx in self.data.keys():
            if jump_to:
                if idx == jump_to:
                    self.data[idx][1] == ELBOW_BOTTOM
                elif idx > value.row and idx < jump_to:
                    self.data[idx][1] = LINE_MIDDLE
                elif idx != value.row:
                    self.data[idx][1] = " "
            else:
                self.data[idx][1] = " "
            self.refresh_cell(idx, 1)
            self.data[idx][2] = format_instruction(self.image.native_type, self.image.instructions[idx], related=instruction)
            self.refresh_cell(idx, 2)

        self._clear_caches()
        return super().watch_cursor_cell(old, value)

    def do_jump(self):
        jmp = is_jump(self.image.native_type, self.image.instructions[self.cursor_cell.row])
        if jmp:
            self.cursor_cell = self.cursor_cell._replace(row=self.image.offsets.index(jmp))


class DissyApp(App):
    """An interactive TUI disassembler."""

    def __init__(self, image: DisassembledImage):
        self.image = image
        super().__init__()

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"),
                ("j", "jump_to", "Jump to target"),
                ("q", "quit", "Quit")]
    TITLE = "Dissy"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield InstructionView()
        yield Footer()

    def on_mount(self):
        table = self.query_one(InstructionView)
        table.show_header = False
        table.image = self.image
        table.add_columns("Offset", "I", "Instruction 2")
        for (offset, line) in zip(self.image.offsets, self.image.instructions):
            table.add_row(Text("%.8x" % offset), " ", format_instruction(self.image.native_type, line))

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
    
    def action_jump_to(self) -> None:
        """An action to jump to target."""
        table = self.query_one(InstructionView)
        table.do_jump()


@click.command()
@click.argument('file', type=click.Path(exists=True))
def main(file):
    """Run the app."""
    image = disassemble(NativeType.X86_64, file)
    DissyApp(image).run()
