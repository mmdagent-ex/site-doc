import socket
import pyaudio

server = ("localhost", 50001)
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect(server)

tcp_client.send(bytearray("__AV_START\n".encode('ascii')))
tcp_client.send(bytearray("__AV_SETMODEL,0\n".encode('ascii')))
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
    tcp_client.send(payload)
