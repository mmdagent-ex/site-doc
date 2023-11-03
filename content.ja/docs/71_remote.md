---
title: ソケット接続による制御
slug: remote-control
---
{{< hint info >}}
ソケット接続による制御の機能は Plugin_Remote が提供しています。利用時はこのプラグインが有効になっているか確かめてください。
{{< /hint >}}

# ソケット接続による制御

実行中の MMDAgent-EX プロセスへソケットを介して接続し、MMDAgent-EX を外部から操作することができます。

- ソケットへ送信されたテキストは、そのままメッセージとして MMDAgent-EX へ発行する
- MMDAgnet-EX から発行されるメッセージは、全てソケットの入力として送られる

実装は[サブモジュールとして組み込むやり方](../submodule)に比べて多少複雑になりますが、

1. MMDAgent-EX からの独立性が高い
2. 標準入出力を扱わないアプリケーションでも接続できる
3. GPUマシン等、MMDAgent-EX を動かすマシンと異なるマシンで動かせる

というメリットがあります。

## WebSocket 通信

WebSocket を使った接続に対応しています。**MMDAgent-EX はクライアント**として、起動直後に .mdf で指定されたWebSocketサーバへ接続を行います。

接続確立後、MMDAgent-EX からサーバへすべてのメッセージが送られます。また、サーバからソケットへ送られたテキストは MMDAgent-EX 内部へメッセージとして発行されます。

.mdf で接続する WebSocket サーバのホスト名、ポート番号、パスを指定することでこの機能がONになります。

{{<mdf>}}
Plugin_Remote_Websocket_Host=localhost
Plugin_Remote_Websocket_Port=9001
Plugin_Remote_Websocket_Directory=/chat
{{</mdf>}}

例えば `wss://foo.bar.com/channel` へ接続するようにするには、以下のようにポート番号として `443` を指定してください。`ws://` は `80` です。

{{<mdf>}}
Plugin_Remote_Websocket_Host=foo.bar.com
Plugin_Remote_Websocket_Port=443
Plugin_Remote_Websocket_Directory=/channel
{{</mdf>}}

## メッセージを受信する

以下は サーバ 側のサンプルです。このプログラムは、WebSocket サーバとして 9001 番ポートで起動したあと、ローカルから接続してきた MMDAgent-EX から受信したメッセージを print します。事前に `asyncio` と `websockets` を `pip install` して下さい。

```python
import asyncio
import websockets

# handler for each connection
async def handle_client(websocket, path):
    print("connected")
    async for message in websocket:
        print(f"Received message: {message}")

# main
async def main():
    async with websockets.serve(handle_client, "localhost", 9001):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
```

上記を起動後、以下の設定を施した .mdf を指定して MMDAgent-EX を起動してください。

{{<mdf>}}
Plugin_Remote_Websocket_Host=localhost
Plugin_Remote_Websocket_Port=9001
Plugin_Remote_Websocket_Directory=/chat
{{</mdf>}}

起動後、通信が確立してから、プログラム側に MMDAgent-EX から受信したメッセージが逐次表示されます。

## メッセージの送信も行う

上記のプログラムを拡張して送信も並列して行えるようにしてみましょう。以下のプログラムは、上記と同じく受け取ったメッセージを print しつつ、2秒に1回 `TEST_MESSAGE` というメッセージを MMDAgent-EX へ流し込むサンプルです。

注意：送信メッセージの末尾に必ず改行（"`\n`"）を付ける必要があることに注意してください。MMDAgent-EX は改行をデリミタとしてメッセージを処理しています。

```python
import asyncio
import websockets
import time

##################################################
# handler for received messages
async def consumer_handler(websocket):
    async for message in websocket:
        print(f"Received message: {message}")

##################################################
# handler to send message: you must append "\n" for each message!
async def producer_handler(websocket):
    while True:
        await asyncio.sleep(2)
        message = "TEST_MESSAGE\n"
        await websocket.send(message)

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

## 音声を送信する

音声データを送る。

音声をストリーミングする。
