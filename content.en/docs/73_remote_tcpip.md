

---
title: Connection Using TCP/IP
slug: remote-tcpip
---
{{< hint info >}}
The TCP/IP connection is provided by Plugin_Remote. Please ensure that this plugin is enabled when in use.
{{< /hint >}}

# Communication Using TCP/IP

We also support [connection and control](../remote-control) using TCP/IP. With TCP/IP, **MMDAgent-EX can act as either a client or a server**. Once a connection is established, the behavior of both is the same, with all of MMDAgent-EX's messages being sent to the server, and text sent from the other party is issued as a message within MMDAgent-EX.

{{< hint danger >}}
WebSocket and TCP/IP cannot be set up simultaneously. When using TCP/IP, please omit the WebSocket settings from the .mdf file.
{{< /hint >}}

## Case 1: When MMDAgent-EX serves as the server

Here are the settings and program example when MMDAgent-EX launches as a server and accepts connections from clients.

### Launching MMDAgent-EX as a TCP/IP Server

In the .mdf file, set `Plugin_Remote_EnableServer=true`, and the port number to listen on.

{{<mdf>}}
Plugin_Remote_EnableServer=true
Plugin_Remote_ListenPort=50001
{{</mdf>}}

### Client Script Example: Receiving

Here's an example of a script connecting to the MMDAgent-EX server and receiving messages.

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

Here's an example of a script connecting to the MMDAgent-EX server and sending messages.

```python
import socket

server = ("127.0.0.1", 50001)
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect(server)
tcp_client.send(b"MESSAGE|aaa|bbb\n")
tcp_client.close()
```

## When MMDAgent-EX serves as the client

Here are the settings and program example when an external program serves as the server, and MMDAgent-EX connects as a client.

### Launching MMDAgent-EX as a TCP/IP Client

In the .mdf file, set `Plugin_Remote_EnableClient=true` and the hostname and port number of the server to connect to.

{{<mdf>}}
Plugin_Remote_EnableClient=true
Plugin_Remote_Hostname=localhost
Plugin_Remote_Port=50001
{{</mdf>}}

### Server Script Example: Receiving

This is an example of a script operating as a server, receiving messages from MMDAgent-EX that connects to it.

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

This is an example of a script operating as a server, sending messages to MMDAgent-EX that connects to it.

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
