---
title: Control via Socket Connection
slug: remote-control
---
{{< hint info >}}
Socket-based control is provided by the Plugin_Remote plugin. Make sure this plugin is enabled before use.
{{< /hint >}}

# Control via Socket Connection

You can connect to a running MMDAgent-EX process via a socket and control MMDAgent-EX externally.

- Text sent to the socket is forwarded to MMDAgent-EX as a message.
- All messages emitted by MMDAgent-EX are sent to the socket.

This implementation is somewhat more complex than the [submodule integration approach](../submodule), but:

1. It offers greater independence from MMDAgent-EX.
2. It allows connections from applications that don't use standard input/output.
3. It can run on a different machine than MMDAgent-EX (for example, a GPU machine).

## Methods

MMDAgent-EX supports two types of communication: WebSocket and TCP/IP. See the explanations and samples for each.

- [WebSocket-based connection](../remote-websocket)
- [TCP/IP-based connection](../remote-tcpip)