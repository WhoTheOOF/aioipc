import asyncio
import json

from .errors import *


class Client:
    """Main client class, used for delivering data from the web server to the bot"""

    def __init__(self, host: str, secret_key: str):
        self.host = host
        self.secret_key = secret_key

    async def request(self, endpoint, port, **kwargs):
        """Make a request to the IPC server"""
        try:
            reader, writer = await asyncio.open_connection(self.host, port)

            data = {"endpoint": endpoint, "data": kwargs, "headers": {"Authorization": self.secret_key}}

            data_dumped = json.dumps(data)
            data_encoded = data_dumped.encode("utf-8")

            data_dumped = f"{len(data_encoded)}xYbO" + data_dumped
            data_encoded = data_dumped.encode("utf-8")

            writer.write(data_encoded)
            await writer.drain()

            first_data = await reader.readuntil(b"uRkP")
            bytes_to_read = int(first_data.decode("utf-8").replace("uRkP", "")) + len(first_data)

            data = await reader.readexactly(bytes_to_read)
            to_return = json.loads(data)

            writer.close()
            await writer.wait_closed()

            return to_return
        except ConnectionRefusedError:
            raise ServerConnectionRefusedError(f"No server found for ({self.host}, {port}), or server isn't accepting "
                                               f"connections.")
