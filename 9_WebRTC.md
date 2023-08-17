# WebRTC を用いた遠隔地からの操作 (beta)

WebRTC を用いて MMDAgent-EX をファイヤーウォール越しに操作することが可能です。ツールとして、[時雨堂](https://shiguredo.jp/)の [WebRTC クライアントツール momo](https://momo.shiguredo.jp/) を改造したものを使います。

> オリジナルの momo は画像・音声の伝送およびデータチャネルを用いたシリアルポートのデータ伝送が
> 行えますが、ここではシリアルポートをローカル TCP/IP ソケットに置き換えた改造版を用います。
> 改造版 momo の実行ファイルは MMDAgent-EX のパッケージに含まれています。

以下のように、MMDAgent-EX と制御ツールのそれぞれの TCP/IP 接続先を momo が代替わりし、
momo どうしが WebRTC で通信を行うことで、データ転送を momo が代わりに行う仕組みになっています。
WebRTCは本来音声・映像を伝送する仕組みが主ですが、ここではデータチャネルのみを使って
ソケット通信の内容をそのままデータチャネルに載せて流しています。

```text
端末側：MMDAgent-EX ↔(TCP:60001)↔ 改造momo ↔ (WebRTCプロトコルで遠隔側と接続)
遠隔側：OpenFaceMS ↔(TCP:60001)↔ 改造momo ↔ (WebRTCプロトコルで端末側と接続)
```

momo には[さまざまな通信モードが用意されています](https://momo.shiguredo.jp/#test_mode)が、
これまでテストはローカルLAN内での momo to momo の簡易接続のみでテストされています。
以下、そのテスト手順です。

○端末マシン（MMDAgent-EXが動作するマシン）

1. MMDAgent-EX の接続先を localhost （の momo）に変更する。`MMDAgent-EX/Release/MMDAgent-EX.mdf` をテキストエディタで開いて接続先をローカルホストにする。

```text
Plugin_Remote_Hostname=localhost
```

2. 以下のように momo を起動。「接続先ホスト」に遠隔マシンのIPアドレスを指定。

```shell
.\momo\momo.exe --no-video-device --no-audio-device --local-server --local-port 60001 ayame --signaling-url ws://接続先ホスト:8080/ws --channel-id test
```

1. momo 起動後に MMDAgent-EX を起動 → ローカルの momo に接続される

○遠隔マシン（OpenFaceMS が動作するマシン）

1. 通常通り OpenFaceMS を起動し、メニューの `Network > Start Server` でサーバを起動

2. OpenFaceMS起動後に以下のように momo を起動 → OpenFaceMS に momo が接続される

```shell
.\momo\momo.exe --no-video-device --no-audio-device --local-client test
```

両マシンで起動し終われば、あとは通常通りに通信が行われます。

> **Note**
> WebRTC通信を単一マシンで試したい場合、MMDAgent-EX側の接続ポート番号を 60001 以外に設定してください。
>
> (1) `MMDAgent-EX/Release/MMDAgent-EX.mdf` で以下のようにポートを変更
>
> ```text
> Plugin_Remote_Port=60002
> ```
>
> 同じ値を MMDAgent-EX 側の momo の起動オプションでも指定
>
> ```text
> ... --local-port 60002
> ```

なお、実際にファイアウォールを超えて遠隔地と通信するには、時雨堂が提供する WebRTC シグナリングサーバ Ayame、あるいは WebRTC SFU Sora 等が必要です。momo はこれらの機能を内蔵しているので
サーバ契約等行えば実行できるはずです。現時点では動作を未検証ですので、
どなたか、検証いただいて報告いただけるとありがたいです。
