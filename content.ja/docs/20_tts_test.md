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
対話スクリプトは、下記のようにモデルやモーションをロードしたあと状態 `LOOP` で待機しており、そこで数字の `1` のキーを押すことで音声合成メッセージ `SYNTH_START` が発行される。

{{<fst>}}
0 LOOP:
    &lt;eps&gt; STAGE|images/floor_green.png,images/back_white.png
    &lt;eps&gt; MODEL_ADD|0|gene/gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    &lt;eps&gt; CAMERA|0,15.25,0|4.5,0,0|22.4|27.0

LOOP LOOP:
    KEY|1 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！
{{< / fst>}}

{{< /details >}}

## しくみの解説

### SYNTH_START メッセージ

MMDAgent-EX では、以下の `SYNTH_START` メッセージを発行することで音声合成が実行されます。

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

### イベントメッセージ

音の出力開始時に `SYNTH_EVENT_START` が、出力終了時に `SYNTH_EVENT_STOP` が出力されます。これを使って、声の開始と同時にアクションを起こしたり、音声が出力し終わるまで待つようなスクリプトを書くことができます。

{{<message>}}
SYNTH_EVENT_START|モデルエイリアス
SYNTH_EVENT_STOP|モデルエイリアス
{{</message>}}

例えば、Exampleの main.fst の末尾部分を以下のように変えて実行することで、異なるスタイルで連続で話すことができます。試してみましょう。

{{<fst>}}
LOOP LOOP:
    KEY|1               SYNTH_START|0|mei_voice_normal|こんにちは！
    SYNTH_EVENT_STOP|0  SYNTH_START|0|mei_voice_happy|よろしくね！
{{< / fst>}}

### 関連ファイル

Open JTalk のモジュールは実行ファイルのあるディレクトリの `Plugins` 以下にある `Plugin_Open_JTalk.dll` (or .so) です。

Open JTalk のボイスモデルと設定ファイルは、コンテンツ側で用意します。Example では `voice/mei` ディレクトリにボイスモデルがあり、設定ファイルは `main.ojt` です。設定ファイルではメッセージで指定する「ボイス名」の定義を行っています。これらを入れ替えることで他の Open JTalk モデルを利用したり声のパラメータの調整等が行えます。