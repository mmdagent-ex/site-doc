# チュートリアル（ローカル版）

以下では単一マシンで動作テストを行う手順を説明します。CG-CAを表示するMMDAgent-EXと、操作を行う OpenFaceMS を同一マシン内で動かします。

動作キットはデフォルトがこの設定になっているので、最小限の手順で実行できます。

## 動作環境の準備

まず[動作環境](1_Environment.md)を整えてください。

## 実行キットの入手

以下の Google Drive フォルダに実行キットがあります。

https://drive.google.com/drive/folders/12cTHs72XBD8VzfvMTXKMcqk-pe7bWdcm

以下の２つをダウンロードします。それぞれ最新のものを使ってください。

- 端末マシン用パッケージ  `AvatarSystem_MMDAgentEXxxxxxx.zip` （xxxxは日付）
- 遠隔マシン用パッケージ `AvatarSystem_OpenFacexxxxxxxx.zip` （同上）

前者を端末マシンに、後者を遠隔マシンにそれぞれダウンロードし、適当な場所に展開します。

## 起動

以下の順番で起動します。

1. 既定の音声出力デバイスを確認（伝送音声は既定の音声出力デバイスから出力される）
2. `run_openface.bat` を実行して OpenFace を起動する
3. メニューの `Network > Start Server` でサーバを起動する
4. `run_mmdagent_gene.bat` または `run_mmdagent_uka.bat` を実行 → MMDAgent-EX が起動し、サーバへの接続まで行われる

遠隔マシンの OpenFaceMS の画面で、右の一覧にローカルアドレス `127.0.0.1` が表示されたら接続成功です。

画面が小さい場合は ウィンドウサイズを調整してください。 `f` キーで全画面表示にできます（２度押すと戻る）。

## テスト操作

OpenFaceMS に表示されている IP アドレスの横のチェックを入れると、遠隔制御が開始します。チェックを外すと止まります。

制御中は OpenFaceMS側から以下の操作が可能です。トラッキング・音声伝送・対話アクションはそれぞれ単独でも同時でも行えます。

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
