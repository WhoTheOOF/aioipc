## aioipc

This was originally forked from an old version of [discord-ext-ipc](https://github.com/Ext-Creators/discord-ext-ipc),
thanks [Logan](https://github.com/lgaan) for writing most of it.

Some changes were made in order to make the extension work with bots running using clusters, allowing the client to make
requests to different ipc servers. Moreover, the data received by both the client, and the server are now being read
efficiently.
