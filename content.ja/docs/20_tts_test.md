---
title: 音声合成を試す
slug: tts-test
---
# 音声合成を試す

MMDAgent-EX には、デフォルトの音声合成エンジンとして日本語の [Open JTalk](https://open-jtalk.sp.nitech.ac.jp/) と英語の [FLite+HTS_Engine](http://flite-hts-engine.sp.nitech.ac.jp/) が組み込まれています。これらは軽量で処理速度が速く遅延が少ないのが特徴です。

{{< hint info >}}
他のエンジンを MMDAgent-EX に組み入れて使うこともできます。別プロセスの合成エンジンを[ソケット接続する方法](../remote-control/) や [サブプロセスとして組み込む](../submodule/) などの方法があります。連携方法については[合成音声を外部プロセスから流し込む方法](../remote-speech/)も参考にしてください。
{{< /hint >}}

Example コンテンツには両エンジン用のボイスモデルが含まれています。以下ではそれらを使って実際に音声合成を試してみる手順を説明します。

## 準備

既定の音声出力デバイスから合成音声を再生するので、あらかじめ音声を再生したいサウンドデバイスを既定の出力デバイスとして設定してください。

## テスト

Example コンテンツの対話スクリプトは、起動語に数字の `1` もしくは `2` キーを押すと音声合成が行われるようあらかじめ設定されています。コンテンツが起動したら、 `1` キーを押して日本語の「こんにちは！よろしくね！」という音声がCGモデルのリップシンクとともに出力されることを確認してください。また、`2` キーで英語で "Hello! My name is gene. How can I help you?" と発話することを確認してください。

{{< details "詳細説明" close >}}
対話スクリプトは、下記のようにモデルやモーションをロードしたあと状態 `LOOP` で待機しており、そこでキーを押すことで音声合成メッセージ **SYNTH_START** が発行される。

日本語のエンジン(Open JTalk)と英語のエンジン（FLite+HTS_Engine）ではそれぞれ異なるボイス名（`mei_voice_*` および `slt_voice_*`）が定義されており、このボイス名の指定でエンジンを振り分けている。これらのボイス名はそれぞれ Example コンテンツの `main.ojt` と `main.fph` でそれぞれ記述されている。

{{<fst>}}
0 LOOP:
    <eps> STAGE|images/floor_green.png,images/back_white.png
    <eps> MODEL_ADD|0|gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0

LOOP LOOP:
    KEY|1 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！

LOOP LOOP:
    KEY|2 SYNTH_START|0|slt_voice_normal|"Hello! My name is gene. How can I help you?"
{{< / fst>}}

{{< /details >}}

## メッセージ

MMDAgent-EX の各種モジュールは[メッセージ](../messages)を通じてやりとりします。以下、音声合成を題材に解説します。

### SYNTH_START メッセージ

音声合成モジュールは MMDAgent-EX のメッセージキューを監視しており、 **SYNTH_START** メッセージが流れたら、それを検知して音声合成を実行します。 このため、.fst 等で以下の **SYNTH_START** メッセージを発行することで、音声合成を実行させることができます。

{{<message>}}
SYNTH_START|モデルエイリアス|ボイス名|テキスト
{{</message>}}

"ボイス名" はボイス定義ファイルで定義されるボイス名を指定します。起動する .mdf ファイルと同じ場所にある `.ojt` ファイルと `.fph` ファイルが読み込まれます。それぞれ、Open JTalk (日本語) 用のボイス名定義と、FLite+HTS_Engine (英語) 用のボイス定義です。Example では `main.ojt` に以下が定義されています。

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

Open JTalk のモジュールは実行ファイルのあるディレクトリの `Plugins` 以下にある `Plugin_Open_JTalk.dll` (or .so) です。FLite+HTS_Engine は `Plugin_Flite_plus_hts_engine.dll` (or .so) です。

ボイスモデルと設定ファイルは、コンテンツ側で用意します。Example では `voice/mei` と `voice/slt` ディレクトリにそれぞれのボイスモデルがあり、設定ファイルは `main.ojt` および `main.fph` です。各設定ファイルではメッセージで指定する「ボイス名」の定義を行っています。
