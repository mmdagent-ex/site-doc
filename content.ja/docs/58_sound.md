---
title: サウンド再生
slug: sound
---
{{< hint info >}}
サウンド再生はプラグイン Plugin_Audio, 音声ファイルのリップシンク付き再生は Plugin_Remote が提供しています。利用時はこれらのプラグインが有効になっているか確かめてください。
{{< /hint >}}

# サウンド再生

任意のオーディオファイルを再生できます。また、音声ファイルをリップシンク付きで再生することも可能です。

## 準備

既定の音声出力デバイスからサウンド再生します。あらかじめ、音を再生するサウンドデバイスを既定の出力デバイスとして設定してください。

## サウンド再生

.mp3 と .wav 形式のオーディオファイルを再生できます。

オーディオファイル再生は **SOUND_START** メッセージを使います。再生開始時に **SOUND_EVENT_START** が出力されます。

{{<message>}}
SOUND_START|(sound alias)|(sound file name)
SOUND_EVENT_START|(sound alias)
{{</message>}}

再生を中断するには **SOUND_STOP** メッセージを使います。

{{<message>}}
SOUND_STOP|(sound alias)
{{</message>}}

オーディオの再生が終わったとき（or 中断したとき） **SOUND_EVENT_STOP** が出力されます。

{{<message>}}
SOUND_EVENT_STOP|(sound alias)
{{</message>}}

## 音声再生 with リップシンク

人の声が入ったオーディオファイルを、再生しながらモデルにリップシンクさせることで、あたかもそのキャラクターが喋っているかのように再生することができます。オーディオファイルは合成音声でも問題ありません。

### 準備

.shapemap で以下を定義。ジェネ・うかでは設定済み。

```text
#### リップシンク用モーフ名
LIP_A あ
LIP_I い
LIP_U う
LIP_O お
#### リップシンク中に０にリセットするモーフ名のリスト
#### 上記で指定した以外の、口を開けるモーフを全て指定する
NOLIP え,おお~,ワ,えー,ああ,いい,叫び,あーれー,口わらい,mouth_a_geo_C,mouth_i_geo_C,mouth_u_geo_C,mouth_e_geo_C,mouth_o_geo_C,mouth_oh_geo_C,mouth_smile_geo_C,mouth_surprise_geo

```

**SPEAK_START**

音声ファイルを指定モデルに喋らせる。再生と同時にリップシンクが行われる。再生開始時に **SPEAK_EVENT_START** が、再生終了時に **SPEAK_EVENT_STOP** が発行される。.shapemap 設定が必要。

```text
SPEAK_START|(model alias)|(audio file)
SPEAK_EVENT_START|(model alias)
SPEAK_EVENT_STOP|(model alias)
```
