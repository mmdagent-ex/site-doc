---
title: Speaking External Voice
slug: remote-speech
---
{{< hint info >}}
The lip-sync functionality for external audio is provided by the Plugin_Remote. Please ensure that this plugin is enabled when using it.
{{< /hint >}}

# Speaking External Speech Data

You can prepare a speech data and make MMDAgent-EX to speak.Several methods are available to achieve this. Each will be explained in order below.

## Method 1: Save to file and pass the path

Save your audio data to file, and tell MMDAgent-EX to play it.

- Your program saves the synthesized speech (or recording) to an audio file.
- Send the command to MMDAgent-EX:

{{<message>}}
SPEAK_START|(model alias)|(audio file path)
{{</message>}}

For detailed instructions on how to use the **SPEAK_START** command, please see [Playing Sound](../sound/#sound-reproduction-with-lip-sync).

While this method is simple and easy, it requires the process and MMDAgent-EX to be running on the same machine, sharing the same filesystem. Also, it cannot be used for continuous audio streams.

## Method 2: Stream audio data via socket

You can stream audio data from an external source over a socket using a [socket connection](../remote-control). Although socket connections allow for text message exchanges, you can also send audio data over the same socket using the specific headers outlined below. This works with both [TCP/IP connections](../remote-tcpip) and [WebSocket connections](../remote-websocket).

**When sending audio data using this method, the audio data format must be unencoded 16kHz, 16bit signed short, mono PCM data**. Please note that other sampling rates and formats are not supported. Also, the model for lip-syncing must have lip-sync information described in the [.shapemap](../sound/#preparation-1).

### The procedures

After establishing a socket connection, you need to send the following two messages to MMDAgent-EX. The first message is to start the operation, and the second is to specify the **model you want to lip-sync with**. Each message should be sent with a newline code at the end, like `__AV_START\n`. 

```text
__AV_START
__AV_SETMODEL, model alias
```

Next, you send a message specifying the transfer mode. If you want to send a continuous voice stream like microphone input, send `SNDSTRM\n`. This is the default if no mode is specified. In this case, MMDAgent-EX will automatically skip silent sections from the stream. If you want to send pre-generated voice data, send `SNDFILE\n`. In this case, MMDAgent-EX will not detect or remove silent sections. With `SNDFILE\n`, the end of the voice data needs to be explicitly specified by the sender (explained later).

```text
(For streaming)
SNDSTRM
(For file transmission)
SNDFILE
```

After that, the audio data should divided into short chunks and sent. One chunk consists of the string "`SND`" followed by a 4-digit (decimal) chunk length (in bytes), followed by the body of the raw waveform data. No newline code is needed.  **The size of each chunk should be less than 4K bytes**. For longer audio data, divide it into the small chunks (less than 4K bytes) and send them in turn.

```text
SNDxxxxyyyyyyyyyyyyyyyyyyy....
  SND: Header
  xxxx: Data length (in bytes) in decimal
  yy... Data length of voice waveform data
```

When `SNDFILE\n` is specified, MMDAgent-EX does not automatically detect the end of the voice, so once you have finished sending up to the end, send `SNDBRKS\n` to notify MMDAgent-EX that input has finished.

**Do not close socket immediately**. The audio playing is threaded, i.e., the sending function will return immediately without waiting for the data to play. If you close the socket immediately after finished sending the data, MMDAgent-EX will terminate the audio play immediately, so the whole audio will not be played. If you wish to close the socket after sending audio, **wait for the duration length of the audio before closing the connection**.

### Sample program

Below is a sample script for "Real-time streaming of voice from a microphone device to MMDAgent-EX". Both WebSocket and TCPIP samples are shown. Please prepare a microphone device before running it.

{{< tabs "sample_remote_speech" >}}
{{< tab "WebSocket" >}}

### WebSocket Method

To have MMDAgent-EX connect to localhost:9001 via the WebSocket protocol, please write the following in the Example .mdf. (It cannot be used simultaneously with the TCP/IP method, so if you have a TCP/IP server or client setting, please delete or comment it out)

{{<mdf>}}
Plugin_Remote_Websocket_Host=localhost
Plugin_Remote_Websocket_Port=9001
Plugin_Remote_Websocket_Directory=/chat
{{</mdf>}}

Below is a sample script for the WebSocket server.

```python
#
# audio streaming example: websocket server
#
#!pip install asyncio
#!pip install websockets
#!pip install pyaudio
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
    # send setup messages.  Example content has model loaded as "0"
    await websocket.send("__AV_START\n")
    await websocket.send("__AV_SETMODEL,0\n")
    # open audio device
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
        # record audio and send to MMDAgent-EX
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

First, execute the above server script, then launch MMDAgent-EX with Example. Once launched, if you speak into the microphone, the CG agent will lip-sync and play back that voice. If it does not work well, please check your audio device settings.

{{< /tab >}}
{{< tab "TCP/IP" >}}

### TCP/IP Method

This is a sample of MMDAgent-EX operating as a TCP/IP server, where a client connects and streams audio. First, please write the following in your `Example.mdf` file. (This cannot be used simultaneously with WebSocket, so please delete or comment out any WebSocket settings if they exist).

```mdf
Plugin_Remote_EnableServer=true
Plugin_Remote_ListenPort=50001
```

After launching MMDAgent-EX, you can connect and start streaming audio by running the script below. Speak into your microphone, and confirm that the CG agent reproduces the sound while lip-syncing. (If it doesn't work, please check your audio device settings).

```python
#
# audio streaming example: tcp/ip client
#
#!pip install pyaudio
import socket
import pyaudio

# connect to localhost:50001
server = ("localhost", 50001)
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect(server)

# send initial setup message: example script starts a model with "0", so specify it
tcp_client.send(bytearray("__AV_START\n".encode('ascii')))
tcp_client.send(bytearray("__AV_SETMODEL,0\n".encode('ascii')))

# open audio for recording
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

# main loop to capture audio and send it to MMDAgent-EX
while True:
    input_data = stream.read(chunk_samples)
    header = ("SND" + f"{chunk_bytes:04}").encode('ascii')
    payload = bytearray(header + input_data)
    tcp_client.send(payload)
```

{{< /tab >}}
{{< /tabs >}}

This method requires more coding compared to Method 1, and it also places restrictions on the format of the audio data. However, it offers the advantages of being able to stream continuous audio and exchange data between the sending process and MMDAgent-EX, even if they are on different machines.

## Method 3: just play externally, only send lip information

You can also make MMDAgent-EX do only the "lip sync" part, while an external process handles everything up to the playback of the sound. In this case, the external process creates a message for lip sync, **LYPSYNC_START**, and sends it to MMDAgent-EX via a socket or similar, timed with the playback of the sound.

The **LIPSYNC_START** message is a command to execute lip sync. The first argument is the alias name of the model to target, and the second argument is the content of the lip sync. The content is a sequence of phoneme names and their durations (in milliseconds), separated by commas.

```markdown
LIPSYNC_START|gene|sil,187,k,75,o,75,N,75,n,75,i,62,ch,75,i,87,w,100,a,87,sil,212
```

The default set of phoneme names is the one used by Open JTalk. This can be easily modified or extended by editing the "Lip Sync Definition File".

{{< details "About the Lip Sync Definition File" close >}}

The definition of phoneme names and the conversion rules from each phoneme name to the character's morph are defined in the `lip.txt` file under the `AppData` folder where the MMDAgent-EX executable file is located. Here is a part of it. By default, it is defined to express the phoneme set of Open JTalk as a weighted combination of the four morphs "a", "i", "u", and "o". You can extend this to any phoneme sequence/morph by editing or adding phonemes.

```text
# number of expressions
4
# expression names
あ
い
う
お
# number of phonemes
69
# phone names and interpolation weight
A   0.2 0.0 0.0 0.0
E   0.1 0.3 0.1 0.0
I   0.0 0.2 0.0 0.0
N   0.0 0.0 0.0 0.0
O   0.0 0.0 0.0 0.2
U   0.0 0.0 0.2 0.0
a   0.5 0.0 0.0 0.0
...
```

{{< /details >}}

MMDAgent-EX converts the phoneme sequence sent with **LIPSYNC_START** into motion according to the definition, and starts playback on the specified model. **LIPSYNC_EVENT_START** is issued at the start of lip sync, and **LIPSYNC_EVENT_STOP** is issued when it ends.

```markdown
LIPSYNC_EVENT_START|(model alias)
LIPSYNC_EVENT_STOP|(model alias)
```

You can also interrupt it partway with **LIPSYNC_STOP**.

```markdown
LIPSYNC_STOP|(model alias)
```

Here are the pros and cons of this method from the perspective of an external process.

Pros:

- You have full control over the sound quality and playback device, etc., as the playback is handled by the external process, not limited by MMDAgent-EX's specification.
- You can control the content of the lip sync.
- High degree of expandability

Cons:

- You need to create the lip sync information yourself from the phoneme sequence and duration information.