# dissy

A TUI disassembler for Python code and x64.

## Installation

```console
$ pip install dissy
```

## Usage

Similar to the Python builtin `dis` module, use `dissy.dis` to disassemble a code object:

```python
import dissy
dissy.dis(co)
```

This will open a full-screen disassembler:

![Screenshot of dissy](screenshot.png)

## x64 dumps disassembly

You can also use the command-line version of dissy to disassemble x64 memory dumps.

```console
$ dissy dump.raw
```

![Screenshot of dissy](screenshot.png)
