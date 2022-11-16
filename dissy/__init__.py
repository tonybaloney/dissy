from dissy.disassemblers import disassemble, NativeType
from dissy.app import DissyApp


def dis(code):
    image = disassemble(NativeType.PYTHON, code)
    DissyApp(image).run()
