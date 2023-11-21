import asyncio
import websockets
import time

import pyaudio

##################################################
# handler for received messages
async def consumer_handler(websocket):
    async for message in websocket:
        print(f"Received message: {message}")

##################################################
# handler to send message: you must append "\n" for each message!
async def producer_handler(websocket):
    await websocket.send("__AV_START\n")
    await websocket.send("__AV_SETMODEL,0\n")
    chunk_samples = 480
    chunk_bytes = chunk_samples * 2
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=chunk_samples
        )
    while True:
        input_data = stream.read(chunk_samples)
        header = ("SND" + f"{chunk_bytes:04}").encode('ascii')
        payload = bytearray(header + input_data)
        await websocket.send(payload)
        await asyncio.sleep(0.01)

##################################################
# handler for each connection
async def handle_client(websocket, path):
    # create task to read from the socket
    consumer_task = asyncio.create_task(consumer_handler(websocket))
    # create task to write to the socket
    producer_task = asyncio.create_task(producer_handler(websocket))
    # wait at least one task has been terminated
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