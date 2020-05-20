try:
    from periphery import GPIO


    b = GPIO(77, "out") # Actually blue
    r = GPIO(73, "out") # Actually red
    g = GPIO(138, "out") # Actually green
    ir = GPIO(141, "out")

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

    def IRon():
        # I know it's backwards.
        ir.write(False)

    def IRoff():
        ir.write(True)
except:
    print("Using dummy LED controls")
    def red():
        ...

    def green():
        ...


    def blue():
        ...


    def IRon():
        ...

    def IRoff():
        ...