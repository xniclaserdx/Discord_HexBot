def basis(x, basis):
    x=int(x)
    basis=int(basis)
    if basis >= 2 and basis <= 36:
        ergebnis = []
        while (x > 0):
            r = x % basis
            if r > 9:
                z = 65+r-10
                r = chr(z)
            ergebnis.append(r)
            x = x//basis
        ergebnis.reverse()
        return (''.join(map(str, ergebnis)))
    else:
        return ("Basis nicht unterstützt.")
