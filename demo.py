import dissy
import dissy.app


def demo():
    a = 2
    b = 3.0
    c = 4.0
    c += a * b
    try:
        print(c)
    except Exception:
        print("Error")
    for i in range(10):
        print(i)
    with x as y:
        print()


dissy.dis(demo, show_caches=False, adaptive=False)
