from mcstatus import JavaServer


def return_server_status(server, port):
    server = JavaServer(server, port)
    status = server.status()
    return f"The server has {status.players.online} player(s) online and replied in {status.latency} ms"


def return_server_players(server, port):
    query = server.query()
    return f"The server has the following players online: {', '.join(query.players.names)}"
