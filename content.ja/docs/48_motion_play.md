---
title: モーションの再生
slug: motion-play
---
# モーションの再生

モデルに対してモーションを指定することでモーションを再生できます。ここでは基本的な使い方を紹介します。

## モーションの再生を開始する

**MOTION_ADD** メッセージで再生したいモーションファイル (.vmd) を指定します。
`(model alias)` には対象モデルのエイリアス名、`(motion_alias)` は新たに開始するモーションに付与するモーションエイリアス名です。

{{<message>}}
MOTION_ADD|(model alias)|(motion alias)|file.vmd
{{</message>}}

指定されたモデルエイリアスが存在しない場合、あるいはそのモーションエイリアスが既に存在する場合、システムは Warning を出力し、何も実行しません。

再生を開始した時点で以下の **MOTION_EVENT_ADD** イベントメッセージが発行されます。

{{<message>}}
MOTION_EVENT_ADD|(model alias)|(motion alias)
{{</message>}}

最後まで再生されたらそのモーションは自動的に削除されます。その際は以下の **MOTION_EVENT_DELETE** メッセージが発行されます。

{{<message>}}
MOTION_EVENT_DELETE|(model alias)|(motion alias)
{{</message>}}

## 途中で中断する

**MOTION_DELETE** メッセージで再生中のモーションを途中で中断できます。

{{<message>}}
MOTION_DELETE|(model alias)|(model alias)
{{</message>}}

モーションが中断され削除された時点で **MOTION_EVENT_DELETE** メッセージが発行されます。

{{<message>}}
MOTION_EVENT_DELETE|(model alias)|(model alias)
{{</message>}}

## 別のモーションに入れ替える

**MOTION_CHANGE** で再生中のモーションを別のモーションに入れ替えることができます。`(motion alias)` には入れ替えたいモーションエイリアスを指定します。入れ替え成功後、入れ替え後のモーションが最初から再生されます。

{{<message>}}
MOTION_CHANGE|(model alias)|(motion alias)|other.vmd
{{</message>}}

入れ替えが成功したら、**MOTION_EVENT_CHANGE** が発行されると同時に、入れ替え後のモーションが最初から再生開始します。

{{<message>}}
MOTION_EVENT_CHANGE|(model alias)|(model alias)
{{</message>}}

## 巻き戻す

再生中のモーションを最初から再生しなおすには **MOTION_RESET** を使います。

{{<message>}}
MOTION_RESET|(model alias)|(motion alias)
{{</message>}}
