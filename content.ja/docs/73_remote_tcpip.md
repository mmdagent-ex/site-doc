---
title: TCP/IP を用いた接続
slug: remote-tcpip
---
{{< hint info >}}
TCP/IP接続は Plugin_Remote が提供しています。利用時はこのプラグインが有効になっているか確かめてください。
{{< /hint >}}

# TCP/IP を用いた通信

TCP/IP を使った[接続・制御](../remote-control)にも対応しています。TCP/IPでは **MMDAgent-EX はクライアントにもサーバにもなれます**。接続が確立したあとの動作はどちらも同じで、MMDAgent-EX のすべてのメッセージがサーバへ送られるとともに、相手から送られたテキストは MMDAgent-EX 内部へメッセージとして発行されます。

{{< hint danger >}}
WebSocket と TCP/IP は同時に設定できません。TCP/IPを利用する際は WebSocket の設定は .mdf から省いてください。
{{< /hint >}}

## ケース1: MMDAgent-EXがサーバとなる場合

MMDAgent-EX がサーバとして起動し、クライアントからの接続を受け付ける場合の設定とプログラム例です。

### MMDAgent-EX をTCP/IPサーバとして起動する設定

.mdf に `Plugin_Remote_EnableServer=true` および listen するポート番号を設定します。

{{<mdf>}}
Plugin_Remote_EnableServer=true
Plugin_Remote_ListenPort=60001
{{</mdf>}}

### クライアントスクリプト例：受信

スクリプトがMMDAgent-EXサーバへ接続してメッセージを受信する例です。

```python
import socket

server = ("127.0.0.1", 60001)
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

### クライアントスクリプト例：送信

スクリプトがMMDAgent-EXサーバへ接続してメッセージを送信する例です。

```python
import socket

server = ("127.0.0.1", 60001)
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect(server)
tcp_client.send(b"MESSAGE|aaa|bbb\n")
tcp_client.close()
```

## MMDAgent-EXがクライアントとなる場合

外部プログラムがサーバとなり、MMDAgent-EX クライアントとして接続しに行く場合の設定とプログラム例です。

### MMDAgent-EX をTCP/IPクライアントとして起動する設定

以下のように .mdf に `Plugin_Remote_EnableClient=true` および接続先のホスト名・ポート番号を設定します。

{{<mdf>}}
Plugin_Remote_EnableClient=true
Plugin_Remote_Hostname=localhost
Plugin_Remote_Port=60001
{{</mdf>}}

### サーバスクリプト例：受信

スクリプトがサーバとして、接続してきた MMDAgent-EX からのメッセージを受け取るプログラム例です。

```python
import socket

server = ("127.0.0.1", 60001)
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

### サーバスクリプト例：送信

スクリプトがサーバとして、接続してきた MMDAgent-EX へメッセージを送信するプログラム例です。

```python
import socket

server = ("127.0.0.1", 60001)
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
