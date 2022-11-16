# dissy

A TUI disassembler for Python code and x64.

## Usage

Similar to the Python builtin `dis` module, use `dissy.dis` to disassemble a code object:

```python
import dissy
dissy.dis(co)
```

This will open a full-screen disassembler:

![](screenshot.jpg)
