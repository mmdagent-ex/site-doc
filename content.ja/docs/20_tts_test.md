---
title: 音声合成を試す
slug: tts-test
---
# 音声合成を試す

MMDAgent-EX には、デフォルトの音声合成エンジンとして [Open JTalk](https://open-jtalk.sp.nitech.ac.jp/) が組み込まれており、任意の日本語文章を音声で出力できます。Open JTalk は軽量で処理速度が速く遅延が少ないのが特徴です。

Example コンテンツに付属の Open JTalk 用ボイスモデル "mei" を使ってテストしてみましょう。

## 準備

既定の音声出力デバイスから合成音声を再生するので、あらかじめ音声を再生したいサウンドデバイスを既定の出力デバイスとして設定してください。

## テスト

Example コンテンツの対話スクリプトは、起動語に数字の `1` のキーを押すと音声合成が行われるようあらかじめ設定されています。コンテンツが起動したら、数字の `1` キーを押し、CGモデルのリップシンクとともに合成音声が出力されることを確認してください。

{{< details "詳細説明" close >}}
対話スクリプトは、下記のようにモデルやモーションをロードしたあと状態 `LOOP` で待機しており、そこで数字の `1` のキーを押すことで音声合成メッセージ **SYNTH_START** が発行される。

{{<fst>}}
0 LOOP:
    <eps> STAGE|images/floor_green.png,images/back_white.png
    <eps> MODEL_ADD|0|gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0

LOOP LOOP:
    KEY|1 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！
{{< / fst>}}

{{< /details >}}

## メッセージ

MMDAgent-EX の各種モジュールは[メッセージ](../messages)を通じてやりとりします。以下、音声合成を題材に解説します。

### SYNTH_START メッセージ

音声合成モジュールは MMDAgent-EX のメッセージキューを監視しており、 **SYNTH_START** メッセージが流れたら、それを検知して音声合成を実行します。 このため、.fst 等で以下の **SYNTH_START** メッセージを発行することで、音声合成を実行させることができます。

{{<message>}}
SYNTH_START|モデルエイリアス|ボイス名|テキスト
{{</message>}}

"ボイス名" はボイス定義ファイル (`.ojt`)` で定義されるボイス名を指定します。Example では以下が定義されています。

    mei_voice_normal
    mei_voice_angry
    mei_voice_bashful
    mei_voice_happy
    mei_voice_sad
    mei_voice_fast
    mei_voice_slow
    mei_voice_high
    mei_voice_low

テキストは UTF-8 で入れてください。

### SYNTH_EVENT_START, SYNTH_EVENT_STOP メッセージ

音声合成モジュールは処理の開始や終了といった内部状態の変化に合わせてメッセージを出力します。具体的には、音声の出力開始時に **SYNTH_EVENT_START** を、出力終了時に **SYNTH_EVENT_STOP** を出力します。これを監視することで、声の開始と同時にアクションを起こしたり、音声が出力し終わるまで待つような処理を書くことができます。

{{<message>}}
SYNTH_EVENT_START|モデルエイリアス
SYNTH_EVENT_STOP|モデルエイリアス
{{</message>}}

## 試してみよう

[ブラウザを使って](../message-test) **SYNTH_START** メッセージをいろいろ試してみましょう。
MMDAgent-EX が起動している状態で同じマシンで以下のページを開くと、MMDAgent-EX と接続されてテキストボックスが表示されます。

- <a href="http://localhost:50000" target="_blank">http://localhost:50000</a> （←クリックで別ウィンドウで開きます）

テキストボックスに以下のメッセージを貼り付けて Send ボタンを押し、楽しそうな声が出ることを確かめてください。

{{<message>}}
SYNTH_START|0|mei_voice_happy|よろしくね！
{{</message>}}

### 関連ファイル

Open JTalk のモジュールは実行ファイルのあるディレクトリの `Plugins` 以下にある `Plugin_Open_JTalk.dll` (or .so) です。

Open JTalk のボイスモデルと設定ファイルは、コンテンツ側で用意します。Example では `voice/mei` ディレクトリにボイスモデルがあり、設定ファイルは `main.ojt` です。設定ファイルではメッセージで指定する「ボイス名」の定義を行っています。これらを入れ替えることで他の Open JTalk モデルを利用したり声のパラメータの調整等が行えます。