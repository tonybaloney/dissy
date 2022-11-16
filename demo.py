import dissy
import dissy.app

def foo():
    print("Hello, world!")
    for x in range(10):
        print(x)


dissy.dis(dissy.app.InstructionView.watch_cursor_cell)
