

---
title: Connection Using WebSocket
slug: remote-websocket
---
{{< hint info >}}
WebSocket connection is provided by Plugin_Remote. Please make sure this plugin is enabled when using it.
{{< /hint >}}

# Communication Using WebSocket

It supports [connection and control](../remote-control) using WebSocket. **MMDAgent-EX acts as a client** and connects to the WebSocket server specified in .mdf. Once the connection is established, all subsequent messages from MMDAgent-EX are sent to the server. Also, any text sent from the server to the socket is issued as a message within MMDAgent-EX.

## Setting the Connection Destination of MMDAgent-EX

Specify the host name, port number, and path of the target WebSocket server in .mdf. This feature will be turned ON by these settings.

{{<mdf>}}
Plugin_Remote_Websocket_Host=localhost
Plugin_Remote_Websocket_Port=9001
Plugin_Remote_Websocket_Directory=/chat
{{</mdf>}}

When connecting to a WebSocket Secure (WSS) server (a server with the scheme `wss`, like `wss://foo.bar.com/channel`), please specify `443` for the port number. The `ws://` scheme is `80`.

{{<mdf>}}
Plugin_Remote_Websocket_Host=foo.bar.com
Plugin_Remote_Websocket_Port=443
Plugin_Remote_Websocket_Directory=/channel
{{</mdf>}}

{{< hint danger >}}
WebSocket and TCP/IP cannot be set simultaneously. When using WebSocket, please omit the settings for the TCP/IP server/client from .mdf.
{{< /hint >}}

## Example 1: Receiving Messages from MMDAgent-EX

Below is a sample of the server side. This program starts as a WebSocket server at port 9001, and then prints the messages received from MMDAgent-EX connecting locally. Please `pip install` `asyncio` and `websockets` beforehand.

```python
import asyncio
import websockets

# handler for each connection
async def handle_client(websocket, path):
    print("connected")
    async for message in websocket:
        print(f"Received message: {message}")

# main
async def main():
    async with websockets.serve(handle_client, "localhost", 9001):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
```

After starting the above, launch MMDAgent-EX with the .mdf set as follows.

{{<mdf>}}
Plugin_Remote_Websocket_Host=localhost
Plugin_Remote_Websocket_Port=9001
Plugin_Remote_Websocket_Directory=/chat
{{</mdf>}}

After launch, once the communication is established, the messages received from MMDAgent-EX will be displayed on the program side sequentially.

## Example 2: Simultaneously Sending and Receiving Messages

Let's extend the above program to enable parallel transmission as well. The following program:

- Prints messages received from MMDAgent-EX
- Sends a `TEST_MESSAGE` to MMDAgent-EX every 2 seconds

This example performs both of these operations. Using asynchronous I/O, it generates separate asynchronous tasks for receiving and sending with `asyncio.create_task()`.

{{< hint warning >}}
Attention: Please remember to always append a newline ("`\n`") at the end of the transmission message. MMDAgent-EX processes messages using a newline as a delimiter.
{{< /hint >}}

```python
import asyncio
import websockets
import time

##################################################
# handler for received messages
async def consumer_handler(websocket):
    async for message in websocket:
        print(f"Received message: {message}")

##################################################
# handler to send message: you must append "\n" for each message!
async def producer_handler(websocket):
    while True:
        await asyncio.sleep(2)
        message = "TEST_MESSAGE\n"
        await websocket.send(message)

##################################################
# handler for each connection
async def handle_client(websocket, path):
    # create task to read from the socket
    consumer_task = asyncio.create_task(consumer_handler(websocket))
    # create task to write to the socket
    producer_task = asyncio.create_task(producer_handler(websocket))
    # wait until at least one task has been terminated
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    # cancel other task and close connection
    for task in pending:
        task.cancel()

# main
async def main():
    async with websockets.serve(handle_client, "localhost", 9001):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
```

After starting this server, start MMDAgent-EX, press the `d` key, and make sure that the test message (`TEST_MESSAGE`) from the server arrives every 2 seconds.

![websocket test](/images/websocket_snap.png)

The settings and programs explained here are also included in the `example_websocket` folder in the Examples, so you can try them out.