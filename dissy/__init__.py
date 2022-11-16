from dissy.app import DissyApp
from dissy.disassemblers.python import disassemble


def dis(code, show_caches=False, adaptive=False):
    image = disassemble(code, show_caches=show_caches, adaptive=adaptive)
    DissyApp(image).run()
