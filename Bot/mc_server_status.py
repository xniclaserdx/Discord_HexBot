from mcstatus import JavaServer
import interactions

def return_server_status(server, port):
    try:
        server = JavaServer(server, port)
        status = server.status()
        return f"The server has {status.players.online} player(s) online and replied in {round(status.latency,3)} ms"
    except:
        return f"Server seems offline..."


def return_server_players(server, port):
    query = server.query()
    return f"The server has the following players online: {', '.join(query.players.names)}"

class McServerStatusModule(interactions.Extension):
    def __init__(self,client):
        self.client = client
    
    # command for mc server status check
    @interactions.extension_command(
        name = "mcstatus",
        description = "Checks the status of a minecraft server",
        options = [
            interactions.Option(
                name = "server",
                description = "Minecraft server to be checked",
                type = interactions.OptionType.STRING,
                required = True,
            ),
            interactions.Option(
                name = "port",
                description = "Port (hab kein Plan wofür der ist, gerne ergänzen)",
                type = interactions.OptionType.INTEGER,
                required = False,
            )
        ]
    )
    async def mcstatus_command(self,ctx: interactions.CommandContext,server: str, port: int = 25565):
        await ctx.send(return_server_status(server,port))

def setup(client):
    McServerStatusModule(client)