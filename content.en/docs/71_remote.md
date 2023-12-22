

---
title: Control via Socket Connection
slug: remote-control
---
{{< hint info >}}
Plugin_Remote provides the functionality for control via socket connections. Please make sure this plugin is enabled when using it.
{{< /hint >}}

# Control via Socket Connection

You can connect to a running MMDAgent-EX process via a socket and operate MMDAgent-EX from an external source.

- Text sent to the socket is issued directly as a message to MMDAgent-EX
- All messages issued from MMDAgent-EX are sent as input to the socket

While the implementation is slightly more complex compared to [embedding as a submodule](../submodule), it offers the following advantages:

1. High independence from MMDAgent-EX
2. Can connect even with applications that do not handle standard input/output
3. Can be run on different machines, such as GPU machines, separate from the machine running MMDAgent-EX

## Method

MMDAgent-EX supports two types of communication: via WebSocket and TCP/IP. Please see the explanations and samples for each.

- [Connection using WebSocket](../remote-websocket)
- [Connection using TCP/IP](../remote-tcpip)