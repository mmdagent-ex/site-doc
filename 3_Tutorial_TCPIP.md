# チュートリアル

端末用と遠隔用の２台のPCを別々に用意し、TCP/IP で直接接続するパターンの動作テスト手順を説明します。２台は直接ポート 60001/tcp で接続するので、ローカルLAN内での接続向けです。

## 動作環境の準備

まず[動作環境](1_Environment.md)をそれぞれのマシンで整えてください。

## 実行キットの入手

以下の Google Drive フォルダに実行キットがあります。

https://drive.google.com/drive/folders/12cTHs72XBD8VzfvMTXKMcqk-pe7bWdcm

以下の２つをダウンロードします。それぞれ最新のものを使ってください。

- 端末マシン用パッケージ  `AvatarSystem_MMDAgentEXxxxxxx.zip` （xxxxは日付）
- 遠隔マシン用パッケージ `AvatarSystem_OpenFacexxxxxxxx.zip` （同上）

前者を端末マシンに、後者を遠隔マシンにそれぞれダウンロードし、適当な場所に展開します。

## 設定

TCP/IP方式では、どちらかがサーバになり、どちらかがクライアントになります。どちらのパターンも実装されていますが、以下では

- 遠隔マシンがサーバとなり、端末マシンからクライアントとして接続

のパターンで説明します。

### 端末マシンを TCP/IP クライアントとして設定

端末マシンの実行キット展開フォルダ以下の `MMDAgent-EX/Release` フォルダを開き、そこにある `MMDAgent-EX.mdf` をテキストエディタで開きます。

以下のパートで設定しています。接続する遠隔マシンのアドレスまたはホスト名を `Plugin_Remote_Hostname` で指定してください。

```text
## クライアントモードを有効化
Plugin_Remote_EnableClient=true
## 遠隔マシンのIPv4アドレスまたはホスト名
Plugin_Remote_Hostname=192.168.1.4
## ポート番号
Plugin_Remote_Port=60001
## 接続失敗時にリトライする回数
Plugin_Remote_RetryCount=60
```

なお、WebSocket モードとの併用はできないので、もし同ファイルに `Plugin_Remote_Websocket_Host=...` の設定がある場合は消すかコメントアウト (`#`) してください。

## 起動

以下の手順で、遠隔マシン→端末マシンの順に起動します。

(1) 遠隔マシンにて：

1. `run_openface.bat` を実行して OpenFace を起動する
2. メニューの `Network > Start Server` でサーバを起動する

(2) 端末マシンにて：

1. 既定の音声出力デバイスを確認（音声はPCの既定の音声出力デバイスから出力される）
2. `run_mmdagent_gene.bat` または `run_mmdagent_uka.bat` を実行 → MMDAgent-EX が起動し、サーバへの接続まで行われる

遠隔マシンの OpenFaceMS の画面で、右の一覧に端末マシンのIPアドレスが表示されたら接続成功です。

画面が小さい場合は ウィンドウサイズを調整してください。 `f` キーで全画面表示にできます（２度押すと戻る）。

## テスト操作

OpenFaceMS に表示されている端末マシンの IP アドレスの横のチェックを入れると、遠隔制御が開始します。チェックを外すと止まります。制御中は OpenFaceMS側で以下の操作が可能です。トラッキング・音声伝送・対話アクションはそれぞれ単独でも同時でも行えます。

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

## その他の操作

MMDAgent-EX はキーやマウスで視点など様々な操作が可能です。 [MMDAgent-EXの操作方法はオフィシャルサイトを参照](https://mmdagent-ex.dev/docs/bindings/)してください。

以上でチュートリアルは終了です。
