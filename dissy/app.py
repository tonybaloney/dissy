from textual.app import App, ComposeResult 
from textual.widgets import Header, Footer, DataTable
from textual.reactive import Reactive
from typing import List
from rich.syntax import Syntax
from rich.text import Text

from dissy.diasssemblers import disassemble, NativeType, is_jump

import click


class InstructionView(DataTable):
    instructions: Reactive[List] = Reactive([])
    offsets: Reactive[List] = Reactive([])

    def watch_cursor_cell(self, old, value) -> None:
        updated = False
        if jmp := is_jump(self.instructions[value.row]):
            try:
                offset_row = self.offsets.index(jmp)
                self.data[offset_row][0].stylize("bold magenta")
                self.refresh_cell(offset_row, 0)
                updated = True
            except ValueError:
                pass
        if jmp := is_jump(self.instructions[old.row]):
            try:
                offset_row = self.offsets.index(jmp)
                self.data[offset_row][0] = Text(self.data[offset_row][0].plain)
                self.refresh_cell(offset_row, 0)
                updated = True
            except ValueError:
                pass

        if updated:
            self._clear_caches()
        return super().watch_cursor_cell(old, value)


class DissyApp(App):
    """An interactive TUI disassembler."""

    def __init__(self, offsets, instructions):
        self.offsets = offsets
        self.instructions = instructions
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
        table.instructions = self.instructions
        table.offsets = self.offsets
        syntax = Syntax("", lexer="nasm", theme="ansi_dark" if self.dark else "ansi_light")
        table.add_columns("Offset", "Arrow", "Instruction")
        for (offset, line) in zip(self.offsets, self.instructions):
            table.add_row(Text("%.8x" % offset), syntax.highlight(str(line)))

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
    
    def action_jump_to(self) -> None:
        """An action to jump to target."""
        table = self.query_one(InstructionView)
        jmp = is_jump(self.instructions[table.cursor_cell.row])
        if jmp:
            try:
                row = self.offsets.index(jmp)
                table.cursor_cell = (row, 0)
            except ValueError:
                pass

@click.command()
@click.argument('file', type=click.Path(exists=True))
def main(file):
    """Run the app."""
    offsets, instructions = disassemble(NativeType.X86_64, file)
    DissyApp(offsets, instructions).run()
