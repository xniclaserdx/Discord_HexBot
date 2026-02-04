"""Module for checking Minecraft server status."""
from mcstatus import JavaServer
import interactions


def return_server_status(server: str, port: int) -> str:
    """
    Check the status of a Minecraft server.
    
    Args:
        server: Server hostname or IP address
        port: Server port number
        
    Returns:
        String with server status information
    """
    try:
        mc_server = JavaServer(server, port)
        status = mc_server.status()
        return f"The server has {status.players.online} player(s) online and replied in {round(status.latency, 3)} ms"
    except ConnectionError:
        return "Server seems offline or unreachable..."
    except TimeoutError:
        return "Server connection timed out..."
    except Exception as e:
        return f"Error checking server status: {type(e).__name__}"


def return_server_players(server: str, port: int) -> str:
    """
    Get the list of players on a Minecraft server.
    
    Args:
        server: Server hostname or IP address
        port: Server port number
        
    Returns:
        String with player names
    """
    try:
        mc_server = JavaServer(server, port)
        query = mc_server.query()
        return f"The server has the following players online: {', '.join(query.players.names)}"
    except Exception as e:
        return f"Could not query server players: {type(e).__name__}"


class McServerStatusModule(interactions.Extension):
    """Extension module for Minecraft server status commands."""
    
    def __init__(self, client):
        self.client = client
    
    @interactions.extension_command(
        name="mcstatus",
        description="Checks the status of a minecraft server",
        options=[
            interactions.Option(
                name="server",
                description="Minecraft server to be checked",
                type=interactions.OptionType.STRING,
                required=True,
            ),
            interactions.Option(
                name="port",
                description="Port of the Minecraft server. The default port is the standard port 25565, if none entered.",
                type=interactions.OptionType.INTEGER,
                required=False,
            )
        ]
    )
    async def mcstatus_command(self, ctx: interactions.CommandContext, server: str, port: int = 25565):
        """Handle Minecraft server status check command."""
        await ctx.send(return_server_status(server, port))


def setup(client):
    """Set up the McServerStatusModule extension."""
    McServerStatusModule(client)
