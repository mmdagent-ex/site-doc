---
title: タイマー
slug: timer
---
# タイマー

{{< hint info >}}
本機能はプラグイン Plugin_Variables の一部です。利用時は Plugin_Variables が有効になっているか確かめてください。
{{< /hint >}}

「ユーザからの入力が一定時間ないときに何か処理をする」あるいは「モーションと音声の再生タイミングを合わせる」など、対話では所定の時間処理か反応を待つようなことが必要な場面があります。このために、MMDAgent-EX ではウェイト処理を行うための「カウントダウンタイマー」が用意されています。

カウントダウンタイマーは、引数で指定した時間が経過した後に **TIMER_EVENT_STOP** メッセージを出力することで時間経過を通知して終了します。

{{< hint warning >}}
タイマーの解像度は 0.1 秒であることに注意してください。0.1秒より小さい値は指定できません。また、カウントも 0.1 秒単位で行われるため数十msは誤差が生じます。
{{< /hint >}}

タイマーの開始・中断を行うメッセージは、以下のものがあります。

- **TIMER_START** タイマーを新たに開始するメッセージ
- **TIMER_CANCEL** 動作中のタイマーをキャンセルするメッセージ

タイマーの状態が変化したときに出力されるメッセージは、以下のとおりです。

- **TIMER_EVENT_START** タイマーを開始したとき
- **TIMER_EVENT_STOP** タイマーが満了したとき
- **TIMER_EVENT_CANCELLED** タイマーがキャンセルもしくは再設定されたとき

## 基本的な使い方

**TIMER_START** メッセージで新たなタイマーをスタートします。引数の `(count down alias)` は新たに開始するタイマーの名前、 `(value)` はタイマーの時間（秒）です。

{{<message>}}
TIMER_START|(count down alias)|(value)
{{</message>}}

同名のタイマーが既に動いている場合は、まず古いタイマーがキャンセル（**TIMER_EVENT_CANCELLED** メッセージ発行）され、その後同名のタイマーが新たに開始します（**TIMER_EVENT_START** メッセージ発行）。

開始した際に **TIMER_EVENT_START** メッセージが発行されます。

{{<message>}}
TIMER_EVENT_START|(count down alias)
{{</message>}}

タイマーはバックグラウンドで 0.1 秒ごとに値が減っていきます。指定時間が経過して値が 0 になったら終了時です。終了時、**TIMER_EVENT_STOP** メッセージが出力され、タイマーは削除されます。

{{<message>}}
TIMER_EVENT_STOP|(count down alias)
{{</message>}}

## キャンセル

あるタイマーを途中で中断したいときは **TIMER_CANCEL** メッセージを使います。

{{<message>}}
TIMER_CANCEL|(count down alias)|(value)
{{</message>}}

**TIMER_CANCEL** は指定されたタイマーが存在する・しないにかかわらず **TIMER_EVENT_CANCELLED** を発行します。

{{<message>}}
TIMER_EVENT_CANCELLED|(count down alias)
{{</message>}}
