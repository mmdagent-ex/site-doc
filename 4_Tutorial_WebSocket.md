# チュートリアル

端末マシンと遠隔マシンを WebSocket サーバ経由で接続する場合の動作テスト手順を説明します。

WebSocket サーバはWebベースの通信であり、ファイヤーウォールを越えた遠隔地との接続に向いています。また、端末マシンの状況と周囲の様子をWebカメラやマイク、スクリーンショットを使って遠隔操作者側へリアルタイム伝送する機能が使えます。遠隔地との接続や、複数の端末マシンを切り替えて用いる用途ではこちらがお勧めです。

## 動作環境の準備

まずそれぞれのマシンで[動作環境](1_Environment.md)を整えてください。

## 実行キットの入手

以下の Google Drive フォルダに実行キットがあります。

https://drive.google.com/drive/folders/12cTHs72XBD8VzfvMTXKMcqk-pe7bWdcm

以下の２つをダウンロードします。それぞれ最新のものを使ってください。

- 端末マシン用パッケージ  `AvatarSystem_MMDAgentEXxxxxxx.zip` （xxxxは日付）
- 遠隔マシン用パッケージ `AvatarSystem_OpenFacexxxxxxxx.zip` （同上）

前者を端末マシンに、後者を遠隔マシンにそれぞれダウンロードし、適当な場所に展開します。

## WebSocket サーバの準備

端末マシンと遠隔マシンは両方ともWebSocketクライアントとしてWebSocketサーバに接続する形になります。サーバは複数の接続を扱えますが、同一のURLパスに接続したツールどうしが通信できます。

事前に WebSocket サーバを起動しておきます。遠隔マシンの実行キットの中に WebSocket サーバの Python スクリプト (Windowsで動作確認）があります。ポート番号等を適宜編集して、適当なWindowsマシンで起動してください（端末マシンや遠隔マシン上で動かしてもかまいません）。

外部向けのサーバを立てる場合、Google App Engine 用の WebSocket サーバスクリプトが参考として同梱されていますので、こちらもご活用ください。

## 設定

端末マシンで、実行キットを展開したフォルダの `MMDAgent-EX/Release` フォルダを開き、そこにある `MMDAgent-EX.mdf` をテキストエディタで編集します。以下の WebSocket 関連の設定のコメントアウトを外して、値を設定します。

```text
## WebSocket サーバのホスト名
Plugin_Remote_Websocket_Host=127.0.0.1
## WebSocket サーバのポート番号
Plugin_Remote_Websocket_Port=9000
## WebSocket サーバ上でこの端末が接続しに行くユニークパス名（/で始まる）
Plugin_Remote_Websocket_Directory=/shop1
## 接続失敗時にリトライする回数
Plugin_Remote_RetryCount=60
```

TCP/IPモードとの併用はできないので、`Plugin_Remote_EnableClient=true` あるいは `Plugin_Remote_EnableServer=true` があればこれらの行をコメントアウトしておいてください。

## 起動

※ 端末マシンと遠隔マシンの起動順序は逆でも問題ありません。

### 端末マシン

1. 既定の音声出力デバイスを確認（音声はPCの既定の音声出力デバイスから出力される）
2. 既定のWebカメラと音声入力デバイスを確認（遠隔地への伝送に用いられる）
3. `run_mmdagent_gene.bat` または `run_mmdagent_uka.bat` を実行 → MMDAgent-EX が起動し、サーバへの接続とパスの登録がで行われる

### 遠隔マシン

1. `run_openface.bat` を実行して OpenFace を起動する
2. メニューの `WebSocket` を押す → 操作ウィンドウが出てくる
3. WebSocketサーバのアドレスとポート番号を入力して `Get Channels` を押す
→ 現在接続中の端末マシン（MMDAgent-EX）の一覧を取得

画面が小さい場合は ウィンドウサイズを調整してください。 `f` キーで全画面表示にできます（２度押すと戻る）。

あとで MMDAgent-EX を起動した場合も `Get Channels` を押せば更新されます。

## テスト操作

OpenFaceMS に表示されているパスの一覧から選択して `Open` ボタンを押すことで、遠隔制御が開始します。 `Close` ボタンで止まります。

・・・で遠隔地にある端末の画面のスクリーンショットが送られてきます。また・・・にチェックを入れて `Open` することでWebカメラの映像と音声も伝送されます。

設定を変える場合はいったん `Close` してから再び `Open` を押してください。

### フェイストラッキング

Webカメラによる簡易トラッキング：

1. メニューの `File > Open Webcam` でウェブカメラを開く → トラッキング開始
2. 下部の `Stop` ボタンで終了

iOS端末と iFacialMocap を使ったトラッキング：

1. iOSデバイスで iFacialMocap を起動
2. 画面に表示される iOSデバイスの IP アドレスを確認
3. 操作者の顔が映るようiOSデバイスを正面に設置
4. メニューの `File > Open iFacialMocap` → から上記の IP アドレスを指定して `Connect` →接続
5. 下部の `Stop` ボタンで終了

### マイク音声のライブ伝送

1. 右上の録音デバイス一覧から使用するデバイスを選択
2. `[Start Sending Audio]` ボタンを押す → 伝送開始
3. その横の `[Stop]` ボタンで終了

### 音声ファイルの送信

任意の音声ファイル (.wav, .mp3 等）を送信して話させることができます。

1. メニューの `Tweak` ボタンから Tweak Panel を開く
2. パネル最下部の `Send Audio File` から音声ファイルを指定して `send to client` →送信

なおファイル形式は wav, mp3 等に対応します。オーディオフォーマットは 16bit, モノラルである必要があります。

◆対話アクションを実行

1. メニューの `Tweak` ボタンから Tweak Panel を開く
2. `Action test` の中のアイテムをクリック → MMDAgent-EX が対応する対話アクションを実行

以上でチュートリアルは終了です。
