---
title: サウンド再生
slug: sound
---
# サウンド再生

## サウンド再生

**SOUND_START**

サウンドファイルの再生を開始する。mp3, wav が使用可能。再生開始時に **SOUND_EVENT_START** が、終了時に **SOUND_EVENT_STOP** がそれぞれ発行される。

```text
SOUND_START|(sound alias)|(sound file name)
SOUND_EVENT_START|(sound alias)
SOUND_EVENT_STOP|(sound alias)
```

**SOUND_STOP**

再生中のサウンドを強制中断する。中断時に **SOUND_EVENT_STOP** が発行される。

```text
SOUND_STOP|(sound alias)
SOUND_EVENT_STOP|(sound alias)
```

## 音声再生 with リップシンク

**SPEAK_START**

音声ファイルを指定モデルに喋らせる。再生と同時にリップシンクが行われる。再生開始時に **SPEAK_EVENT_START** が、再生終了時に **SPEAK_EVENT_STOP** が発行される。.shapemap 設定が必要。

```text
SPEAK_START|(model alias)|(audio file)
SPEAK_EVENT_START|(model alias)
SPEAK_EVENT_STOP|(model alias)
```
