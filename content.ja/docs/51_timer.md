---
title: タイマー
slug: timer
---
# タイマー

Plugin_Variable にあるタイマーの使い方を詳しく紹介。


## カウントダウンタイマー

**TIMER_START**

タイマー変数を開始する。値は秒で、0.1 秒が最小解像度。

- タイマーが開始したとき **TIMER_EVENT_START** を発行する
- 指定時間が経過したら **TIMER_EVENT_STOP** を発行、そのタイマー変数は削除される。
- 同名のタイマー変数が既に存在する場合、
  - **TIMER_EVENT_CANCELLED** を発行する
  - 値を上書きする
  - **TIMER_EVENT_START** を発行する

```text
TIMER_START|(count down alias)|(value)
TIMER_EVENT_START|(count down alias)
TIMER_EVENT_STOP|(count down alias)
TIMER_EVENT_CANCELLED|(count down alias)
```

**TIMER_STOP**

動作中のタイマー変数をストップする。

- タイマー変数が存在する場合、 **TIMER_EVENT_STOP** を発行
- タイマー変数が存在しない場合は何もしない（ワーニングを出力するのみ）

```text
TIMER_STOP|(count down alias)
TIMER_EVENT_STOP|(count down alias)
```

**TIMER_CANCEL**

タイマー変数を強制的に中断・削除する。

- 指定したタイマー変数が存在する場合、削除して **TIMER_EVENT_CANCEL** を発行
- 指定したタイマー変数が存在しない場合も **TIMER_EVENT_CANCEL** を発行

```text
TIMER_CANCEL|(count down alias)
TIMER_EVENT_CANCELLED|(count down alias)
```