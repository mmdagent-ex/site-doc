---
title: TCP/IP を用いた接続
slug: remote-tcpip
---
{{< hint info >}}
TCP/IP接続は Plugin_Remote が提供しています。利用時はこのプラグインが有効になっているか確かめてください。
{{< /hint >}}

# TCP/IP を用いた通信

TCP/IP を使った[接続・制御](../remote-control)にも対応しています。TCP/IPでは **MMDAgent-EX はクライアントにもサーバにもなれます**。接続が確立したあとの動作はどちらも同じで、MMDAgent-EX のすべてのメッセージがサーバへ送られるとともに、相手から送られたテキストは MMDAgent-EX 内部へメッセージとして発行されます。

## MMDAgent-EX の設定

{{< hint danger >}}
WebSocket と TCP/IP は同時に設定できません。TCP/IPを利用する際は WebSocket の設定は .mdf から省いてください。
{{< /hint >}}

### クライアントになる場合

MMDAgent-EX がクライアントとなって TCP/IP サーバへ接続しに行く場合は、以下のように .mdf に `Plugin_Remote_EnableClient=true` および接続先のホスト名・ポート番号を設定します。

{{<mdf>}}
Plugin_Remote_EnableClient=true
Plugin_Remote_Hostname=localhost
Plugin_Remote_Port=60001
{{</mdf>}}

### サーバになる場合

MMDAgent-EX がサーバとなってクライアントからの接続を受け付ける場合は、.mdf に `Plugin_Remote_EnableServer=true` および listen するポート番号を設定します。

{{<mdf>}}
Plugin_Remote_EnableServer=true
Plugin_Remote_ListenPort=60001
{{</mdf>}}

## 例１：サーバ＋受信

スクリプト側がサーバとなり、クライアント設定の MMDAgent-EX が接続してきたら、MMDAgent-EX から送られてくるメッセージを print するプログラム例です。

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

上記を起動後、以下の設定を施した .mdf を指定して MMDAgent-EX を起動して、サーバ側に MMDAgent-EX 内のメッセージが表示されるのを確認してください。

{{<mdf>}}
Plugin_Remote_EnableClient=true
Plugin_Remote_Hostname=localhost
Plugin_Remote_Port=60001
{{</mdf>}}

## 例２：サーバ＋送信

スクリプト側がサーバとなり、MMDAgent-EX がクライアントとして接続してきたら、メッセージを1つ送信して接続断するプログラムの例です。前半部分は例１と同じです。

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

上記を起動後、以下の設定を施した .mdf を指定して MMDAgent-EX を起動して、MMDAgent-EX 側のログで届いているかを確かめてください。

## 例３：クライアント＋受信

MMDAgent-EX をサーバとして起動しておき、スクリプトがクライアントとして接続するにはプログラムの前半を以下のようにします。

```python
server = ("127.0.0.1", 60001)
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect(server)
```
