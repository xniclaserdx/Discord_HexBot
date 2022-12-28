import interactions

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

class BasisModule(interactions.Extension):
    def __init__(self,client):
        self.client = client
    
    # command for basecalc
    @interactions.extension_command(
        name = "hex_base",
        description = "Converts decimal numbers to numbers of other bases",
        options = [
            interactions.Option(
                name = "number",
                description = "number you want to convert",
                type = interactions.OptionType.INTEGER,
                required = True,
            ),
            interactions.Option(
                name = "base",
                description = "base you want to convert to",
                type = interactions.OptionType.INTEGER,
                required = True,
            )
        ]
    )
    async def basecalc_command(self,ctx: interactions.CommandContext,number: int, base: int):
        await ctx.send(basis(number,base))

def setup(client):
    BasisModule(client)