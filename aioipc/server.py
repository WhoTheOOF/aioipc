import asyncio
import json


class IpcServerResponse:
    """Format the json data parsed into a nice object"""

    def __init__(self, data):
        self._json = data
        self.length = len(data)

        self.endpoint = data["endpoint"]

        for key, value in data["data"].items():
            setattr(self, key, value)

    def to_json(self):
        """Convert object to json"""
        return self._json

    def __repr__(self):
        return "<IpcServerResponse length={0.length}>".format(self)

    def __str__(self):
        return self.__repr__()


class Server:
    """Main server class"""

    def __init__(self, bot, host: str, port: int, secret_key: str):
        self.bot = bot
        self.loop = bot.loop

        self.port = port
        self.host = host

        self.clients = {}
        self.endpoints = {}

        self.secret_key = secret_key

    def add_route(self, func, name: str = False):
        if not name:
            self.endpoints[func.__name__] = func
        else:
            self.endpoints[name] = func

    async def handle_client_requests(self, reader, writer):
        """Processes the client request"""
        try:
            first_data = await reader.readuntil(b"xYbO")
            bytes_to_read = int(first_data.decode("utf-8").replace("xYbO", ""))

            data = await reader.readexactly(bytes_to_read)
            parsed_json = json.loads(data)
        except ConnectionResetError:
            return

        headers = parsed_json.get("headers")

        if headers is None or headers.get("Authorization") != self.secret_key:
            response = {"error": "Invalid or no token provided.", "status": 403}
        else:
            endpoint = parsed_json.get("endpoint")

            if endpoint is None or self.endpoints.get(endpoint) is None:
                response = {"error": f"No endpoint matching {endpoint} was found.", "status": 404}
            else:
                server_response = IpcServerResponse(parsed_json)

                try:
                    ret = await self.endpoints[endpoint](server_response)
                    response = ret
                except Exception as error:
                    self.bot.dispatch("ipc_error", endpoint, error)
                    response = {"error": f"IPC route raised an error.", "code": 500}

        try:
            response_dumped = json.dumps(response)
        except TypeError as error:
            response_dumped = json.dumps(
                {"error": f"IPC route returned values which are not able to be sent over sockets."
                          f"The following `TypeError` exception occured: {error}.",
                 "code": 500})

        response_encoded = response_dumped.encode("utf-8")

        response_dumped = f"{len(response_encoded)}uRkP" + response_dumped
        response_encoded = response_dumped.encode("utf-8")

        writer.write(response_encoded)
        await writer.drain()

        writer.close()
        await writer.wait_closed()

    def start(self):
        """Start the IPC server"""
        server_coro = asyncio.start_server(self.handle_client_requests, self.host, self.port, loop=self.loop)

        self.bot.dispatch("ipc_ready")
        self.loop.run_until_complete(server_coro)
