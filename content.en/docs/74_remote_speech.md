---
title: Streaming Audio Data
slug: remote-speech
---
{{< hint info >}}
Lip-syncing for external audio is provided by Plugin_Remote. Make sure this plugin is enabled when using this feature.
{{< /hint >}}

# Streaming Audio Data

You can send audio data from an external module to MMDAgent-EX and play it with lip-sync. Several methods are available to achieve this. The following sections describe each method in order.

## Method 1: Supply via file

Save the synthesized (or recorded) audio to an audio file and tell MMDAgent-EX the file path to play it. Perform the following steps:

- Save the synthesized or recorded audio to an audio file
- Send an **SPEAK** command to MMDAgent-EX (via socket, etc.) with that file path

For details on the **SPEAK** command, see [Play a sound](../sound/#%e9%9f%b3%e5%a3%b0%e5%86%8d%e7%94%9f-with-%e3%83%aa%e3%83%83%e3%83%97%e3%82%b7%e3%83%b3%e3%82%af).

This method is simple and easy, but since it passes file names, the sender process and MMDAgent-EX must run on machines that share the same filesystem. Also, audio can only be provided per file — it cannot be used for continuous audio streams.

## Method 2: Stream audio data over a socket

You can stream audio into MMDAgent-EX from outside using the [socket connection](../remote-control). Socket connections support text messages, but using the specific headers shown below you can also send audio data over the same socket. This works with both [TCP/IP connections](../remote-tcpip) and [WebSocket connections](../remote-websocket).

When sending audio data this way, the audio format must be raw PCM: 16 kHz, 16-bit signed short, mono (no encoding). Do not use other sample rates or formats. Also, the model to be lip-synced must have lip-sync information described in a .shapemap (see [Preparing for sound](../sound/)).

### Communication procedure

Below is the communication procedure. After establishing a socket connection for audio streaming, send the following two messages to MMDAgent-EX before sending audio. The first indicates the start of the operation, and the second specifies the model alias name to lip-sync. Remember to append a newline to the end of each message (for example, "__AV_START\n").

```text
__AV_START
__AV_SETMODEL,model_alias
```

Next, send a message specifying the transfer mode. If you will be sending a continuous audio stream, send `SNDSTRM\n`. If you do not specify this, the default behavior (below) applies. In the default mode, MMDAgent-EX will automatically trim silent sections and detect audio regions. If you are sending pre-segmented audio (e.g., individual files), send `SNDFILE\n`. In SNDFILE mode, MMDAgent-EX will not automatically detect or trim silent sections, so the sender must explicitly indicate the end of the audio (see below).

```text
(streaming)
SNDSTRM
(file transfer)
SNDFILE
```

Then send the audio data in short chunks. Each chunk consists of the ASCII string "SND" followed by a 4-digit decimal chunk length (in bytes), followed immediately by that many bytes of audio waveform data. No newline is required. Send these chunks consecutively for short audio segments (about 1024 bytes each). The chunk size must not exceed 4 KB. For long audio, split it into chunks and send them in order.

```text
SNDxxxxyyyyyyyyyyyyyyyyyyy....
  SND: header
  xxxx: 4-digit ata length (bytes) as a decimal number
  yy...: audio waveform data of the specified length
```

When using `SNDFILE\n`, MMDAgent-EX will not auto-detect the end of audio, so after sending the final chunk you must send `SNDBRKS\n` to indicate end of input.

Do not close the socket immediately after sending. Audio is buffered on the MMDAgent-EX side and played back on another thread, so sending finishes before playback completes. If you close the socket right after sending, playback (including the tail of the audio) may stop. If you need to close the connection after sending, wait for the duration of the audio before closing.

### Samples

Below is a sample script that records from a microphone and streams audio to MMDAgent-EX in real time. Both WebSocket and TCP/IP samples are provided. Prepare a microphone device before running.

{{< tabs "sample_remote_speech" >}}
{{< tab "WebSocket" >}}
### WebSocket method

Add the following to the Example .mdf so MMDAgent-EX connects via WebSocket to localhost:9001. (WebSocket and TCP/IP cannot be used simultaneously; if you have TCP/IP server/client settings, remove or comment them out.)

{{<mdf>}}
Plugin_Remote_Websocket_Host=localhost
Plugin_Remote_Websocket_Port=9001
Plugin_Remote_Websocket_Directory=/chat
{{</mdf>}}

The following is a sample WebSocket server script.

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

```

Run the server script above, then start MMDAgent-EX from Example. Once running, speak into the microphone and the CG agent will play the audio with lip-sync. If it does not work, check your audio device settings.

{{< /tab >}}
{{< tab "TCP/IP" >}}
### TCP/IP method

This is a sample for when MMDAgent-EX runs as a TCP/IP server and a client connects to stream audio. First add the following to the Example .mdf. (WebSocket and TCP/IP cannot be used simultaneously; if you have WebSocket settings, remove or comment them out.)

{{<mdf>}}
Plugin_Remote_EnableServer=true
Plugin_Remote_ListenPort=50001
{{</mdf>}}

After starting MMDAgent-EX, run the script below to connect and start streaming audio. Speak into the microphone and confirm that the CG agent plays the audio with lip-sync. If it does not work, check your audio device settings.

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

Compared with Method 1, this method requires coding and has format restrictions, but it enables continuous audio streaming and works across different machines.

## Method 3: Drive lip movement only

An external process can play the audio locally and instruct MMDAgent-EX only to perform lip movement. In this case, have the external process create a lip-sync message **LIPSYNC_START** and send it to MMDAgent-EX via socket at the times corresponding to the audio playback.

The **LIPSYNC_START** message directs MMDAgent-EX to run lip-sync. The first argument is the model alias name, and the second argument is the lip-sync content: a comma-separated list of phoneme names and durations (in milliseconds).

{{<message>}}
LIPSYNC_START|gene|sil,187,k,75,o,75,N,75,n,75,i,62,ch,75,i,87,w,100,a,87,sil,212
{{</message>}}

The default phoneme set is the one used by Open JTalk. This can be easily changed or extended by editing the lip-sync definition file.

{{< details "About the lip-sync definition file" close >}}

Phoneme names and the mapping from phoneme names to character morphs are defined in the file AppData/lip.txt under the MMDAgent-EX executable directory. A partial example is shown below. By default, the Open JTalk phoneme set is represented as a weighted combination of four morphs corresponding to "あ", "い", "う", and "お". You can edit this file or add phonemes to extend to arbitrary phoneme sequences and morphs.

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

MMDAgent-EX converts the phoneme sequence sent with **LIPSYNC_START** into motions according to the definition and starts playback on the specified model. MMDAgent-EX emits **LIPSYNC_EVENT_START** when lip-sync starts and **LIPSYNC_EVENT_STOP** when it stops.

{{<message>}}
LIPSYNC_EVENT_START|(model alias)
LIPSYNC_EVENT_STOP|(model alias)
{{</message>}}

You can interrupt lip-sync mid-sequence with **LIPSYNC_STOP**.

{{<message>}}
LIPSYNC_STOP|(model alias)
{{</message>}}

Advantages and disadvantages of this method from the perspective of the external process:

Advantages:

- Playback is handled externally, so you are not limited by MMDAgent-EX’s playback quality or device constraints
- You can fully control the lip-sync content
- High extensibility

Disadvantages:

- You must generate the phoneme sequence and duration information yourself to produce lip-sync data