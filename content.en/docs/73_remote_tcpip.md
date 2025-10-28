---
title: TCP/IP Connection
slug: remote-tcpip
---
{{< hint info >}}
TCP/IP connections are provided by Plugin_Remote. Ensure this plugin is enabled before use.
{{< /hint >}}

# TCP/IP Communication

TCP/IP also supports [connection and control](../remote-control). With TCP/IP, **MMDAgent-EX can act as either a client or a server**. After a connection is established the behavior is the same in both cases: all MMDAgent-EX messages are sent to the server, and text received from the peer is posted as messages inside MMDAgent-EX.

{{< hint danger >}}
WebSocket and TCP/IP cannot be configured at the same time. When using TCP/IP, remove any WebSocket settings from the .mdf.
{{< /hint >}}

## Case 1: MMDAgent-EX as Server

Configuration and example programs for when MMDAgent-EX runs as a server and accepts connections from clients.

### Configuration: Start MMDAgent-EX as a TCP/IP Server

In the .mdf, set `Plugin_Remote_EnableServer=true` and the port number to listen on.

{{<mdf>}}
Plugin_Remote_EnableServer=true
Plugin_Remote_ListenPort=50001
{{</mdf>}}

### Client Script Example: Receiving

Example where a script connects to the MMDAgent-EX server and receives messages.

```python
import socket

server = ("127.0.0.1", 50001)
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect(server)

while True:
   try:
      rcvmsg = tcp_client.recv(4096)
      print("[*] received: {}".format(rcvmsg))
   except Exception as e:
      print(e)

tcp_client.close()
```

### Client Script Example: Sending

Example where a script connects to the MMDAgent-EX server and sends a message.

```python
import socket

server = ("127.0.0.1", 50001)
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect(server)
tcp_client.send(b"MESSAGE|aaa|bbb\n")
tcp_client.close()
```

## MMDAgent-EX as Client

Configuration and example programs for when an external program acts as the server and MMDAgent-EX connects as a client.

### Configuration: Start MMDAgent-EX as a TCP/IP Client

In the .mdf, set `Plugin_Remote_EnableClient=true` and specify the hostname and port to connect to, as shown below.

{{<mdf>}}
Plugin_Remote_EnableClient=true
Plugin_Remote_Hostname=localhost
Plugin_Remote_Port=50001
{{</mdf>}}

### Server Script Example: Receiving

Example where a script acts as a server and receives messages from a connecting MMDAgent-EX.

```python
import socket

server = ("127.0.0.1", 50001)
listen_num = 5

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind(server)
tcp_server.listen(listen_num)

while True:
   client, address = tcp_server.accept()
   print("[*] connected: {}".format(address))
   while True:
      try:
         rcvmsg = client.recv(4096)
         print("[*] received: {}".format(rcvmsg))
      except Exception as e:
         print(e)
   client.close()
```

### Server Script Example: Sending

Example where a script acts as a server and sends a message to a connecting MMDAgent-EX.

```python
import socket

server = ("127.0.0.1", 50001)
listen_num = 5

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind(server)
tcp_server.listen(listen_num)

while True:
   client, address = tcp_server.accept()
   print("[*] connected: {}".format(address))
   client.send(b"MESSAGE|aaa|bbb\n")
   client.close()
```