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

## 方式

MMDAgent-EX は、WebSocket による通信と TCP/IP による通信の2種類をサポートしています。それぞれの解説とサンプルをご覧ください。

- [WebSocketを用いた接続](../remote-websocket)
- [TCP/IPを用いた接続](../remote-tcpip)
