from periphery import GPIO


r = GPIO(77, "out")
g = GPIO(73, "out")
b = GPIO(138, "out")

def red():
        print("R")
        r.write(True)
        g.write(False)
        b.write(False)

def green():
        print("G")
        r.write(False)
        g.write(True)
        b.write(False)

def blue():
        print("B")
        r.write(False)
        g.write(False)
        b.write(True)
