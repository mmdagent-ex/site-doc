---
title: サウンド再生
slug: sound
---
{{< hint info >}}
オーディオファイル再生は Plugin_Audio, 音声リップシンク再生は Plugin_Remote が提供しています。利用時はこれらのプラグインが有効になっているか確かめてください。
{{< /hint >}}

# サウンド再生

音楽や効果音を効果的に使うことでよりリッチなインタラクションを作ることができます。MMDAgent-EX はオーディオファイルを再生する機能があり、バックグラウンドで音楽を鳴らしたりイベントに合わせて効果音を鳴らすことができます。

また、MMDAgent-EX では録音済み（あるいは合成済み）の音声データをキャラクターにリップシンクさせながら再生する機能も用意しています。あらかじめ録音した音声で返答する、あるいは別の音声合成エンジンで出力した音声ファイルを喋らせる、といった用途に使うことができます。

以下ではサウンドファイルの再生と、音声ファイルのリップシンク付き再生のやり方を解説します。

## 準備

MMDAgent-EX は「既定の音声出力デバイス」からサウンドを再生します。あらかじめ、音を再生するサウンドデバイスを既定の出力デバイスとして設定してください。

macOS, Linux では予め [sox](https://sourceforge.net/projects/sox/) をインストールしてください。

**macOS**:

```shell
brew install sox
```

**Linux**:

```shell
sudo apt install sox
```

## サウンド再生

.wav, .mp3 等のオーディオファイルを **SOUND_START** メッセージで再生できます。

{{< details "対応フォーマットについて" close >}}
**Windows**: 標準で .wav および .mp3 に対応しています。他のオーディオファイル形式を再生するためには、適切なコーデックやドライバをインストールする必要があります。

**macOS, Linux**: [sox](https://sourceforge.net/projects/sox/) の play コマンドを使って再生しており、.wav, .mp3 をはじめほとんどの形式のオーディオファイルに対応しています。
{{< /details >}}

再生を開始したときに **SOUND_EVENT_START** が出力されます。

{{<message>}}
SOUND_START|(sound alias)|(sound file name)
SOUND_EVENT_START|(sound alias)
{{</message>}}

再生中の音を途中で中断するには **SOUND_STOP** メッセージを使います。

{{<message>}}
SOUND_STOP|(sound alias)
{{</message>}}

オーディオの再生が終わったとき（or 中断したとき） **SOUND_EVENT_STOP** が出力されます。

{{<message>}}
SOUND_EVENT_STOP|(sound alias)
{{</message>}}

{{< hint warning >}}
サウンドがならない場合は既定の音声出力デバイスをチェックしてください。また、再生には sox の `play` コマンドを使用していますが、[環境変数で異なるコマンドを指定することができます](../envval/#audio_start-用再生コマンド-play)。
{{< /hint >}}



## 音声再生 with リップシンク

### 準備

リップシンクは、音声ファイルから取り出した音素情報を「あ」「い」「う」「お」の口形のブレンドとしてマッピングすることで表現されます。このため、モデル上のどのモーフが「あ」「い」「う」「お」に対応するかを、あらかじめ .shapemap ファイルで記述しておく必要があります。ジェネ・うかの配布版ではすでに設定されていますが、他のモデルを使う場合は自分で作成する必要があります。

作成する場合は、モデルファイル `xxx.pmd` が格納されているフォルダと同じフォルダに `xxx.pmd.shapemap` というファイル名で、以下のようなテキストファイルを作成・保存してください。`LIP_A` から `LIP_O` はそれぞれに対応するモーフ名を記述します。`NOLIP` には、上記以外の口を開けるモーフを全てカンマ区切りで指定してください。文字コードは UTF-8 である必要があります。

```text
#### リップシンク用モーフ名
LIP_A あ
LIP_I い
LIP_U う
LIP_O お
#### リップシンク中に 0 にリセットするモーフ名のリスト
#### 上記で指定した以外の、口を開けるモーフを全て指定する
NOLIP え,おお~,ワ,えー,ああ,いい,叫び,あーれー,口わらい
```

### 実行

起動後、**SPEAK_START** メッセージで音声ファイルをリップシンク付き再生します。`(model alias)` はリップシンクを行うモデルのエイリアスを指定し、`(audio file)` は再生する音声ファイルです。再生開始時には **SPEAK_EVENT_START** メッセージが出力されます。

{{<message>}}
SPEAK_START|(model alias)|(audio file)
SPEAK_EVENT_START|(model alias)
{{</message>}}

音声ファイルは .wav, .mp3 など、[libsndfile でサポートされるフォーマット](https://libsndfile.github.io/libsndfile/formats.html) が使えます。なお、出力時には 16kHz, モノラルに変換して出力されるのでご注意ください。

再生終了時には **SPEAK_EVENT_STOP** が出力されます。

{{<message>}}
SPEAK_EVENT_STOP|(model alias)
{{</message>}}

再生中の音声を途中で止めたい場合は **SPEAK_STOP** を使います．発行されたとき，音声が停止あるいは既に停止であることが確認されたときに **SPEAK_EVENT_STOP** が出力されます．

{{<message>}}
SPEAK_STOP|(model alias)
{{</message>}}
