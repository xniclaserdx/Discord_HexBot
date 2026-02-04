"""Module for base conversion calculations."""
import interactions


def convert_to_base(number: int, base: int) -> str:
    """
    Convert a decimal number to another base (2-36).
    
    Args:
        number: The decimal number to convert
        base: The target base (must be between 2 and 36)
        
    Returns:
        String representation of the number in the target base
    """
    number = int(number)
    base = int(base)
    
    if not (2 <= base <= 36):
        return "Base not supported. Please use a base between 2 and 36."
    
    if number == 0:
        return "0"
    
    result = []
    while number > 0:
        remainder = number % base
        if remainder > 9:
            # Convert to letter (A-Z for bases 11-36)
            char_code = 65 + remainder - 10
            remainder = chr(char_code)
        result.append(str(remainder))
        number = number // base
    
    result.reverse()
    return ''.join(result)

class BasisModule(interactions.Extension):
    """Extension module for base conversion commands."""
    
    def __init__(self, client):
        self.client = client
    
    @interactions.extension_command(
        name="hex_base",
        description="Converts decimal numbers to numbers of other bases",
        options=[
            interactions.Option(
                name="number",
                description="number you want to convert",
                type=interactions.OptionType.INTEGER,
                required=True,
            ),
            interactions.Option(
                name="base",
                description="base you want to convert to",
                type=interactions.OptionType.INTEGER,
                required=True,
            )
        ]
    )
    async def basecalc_command(self, ctx: interactions.CommandContext, number: int, base: int):
        """Handle the base conversion command."""
        await ctx.send(convert_to_base(number, base))


def setup(client):
    """Set up the BasisModule extension."""
    BasisModule(client)