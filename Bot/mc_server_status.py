from mcstatus import JavaServer


def return_server_status(server, port):
    try:
        server = JavaServer(server, port)
        status = server.status()
        return f"The server has {status.players.online} player(s) online and replied in {round(status.latency,3)} ms"
    except:
        try:
            server = JavaServer(server, 25565)
            status = server.status()
            return f"The server has {status.players.online} player(s) online and replied in {round(status.latency,3)} ms"
        except:
            return f"Server seems offline..."


def return_server_players(server, port):
    query = server.query()
    return f"The server has the following players online: {', '.join(query.players.names)}"
