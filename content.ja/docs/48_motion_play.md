---
title: モーションの再生
slug: motion-play
---
# モーションの再生

モデルにモーションファイル (.vmd) を与えることでモーション再生を行うのが基本的な手順です。ここではモーションを再生する基本的なメッセージを紹介します。

## モーションの再生を開始する

**MOTION_ADD** メッセージで再生したいモーションファイル (.vmd) を指定することで、モーション再生を開始します。`(model alias)` には対象モデルのエイリアス名、`(motion_alias)` は新たに開始するモーションに付与するモーションエイリアス名です。

{{<message>}}
MOTION_ADD|(model alias)|(motion alias)|file.vmd
{{</message>}}

モデルが存在しない場合、システムは Warning を出力し、何も実行しません。

指定されたモーションエイリアスと同じ名前のモーションが再生中の場合、そのモーションを新たなモーションで上書きします。

再生を開始した時点で以下の **MOTION_EVENT_ADD** イベントメッセージが発行されます。

{{<message>}}
MOTION_EVENT_ADD|(model alias)|(motion alias)
{{</message>}}

最後まで再生されたらそのモーションは自動的に削除され、**MOTION_EVENT_DELETE** メッセージが発行されます。

{{<message>}}
MOTION_EVENT_DELETE|(model alias)|(motion alias)
{{</message>}}

## 途中で中断する

**MOTION_DELETE** メッセージで再生中のモーションを中断できます。

{{<message>}}
MOTION_DELETE|(model alias)|(model alias)
{{</message>}}

モーションが中断され削除された時点で **MOTION_EVENT_DELETE** メッセージが発行されます。

{{<message>}}
MOTION_EVENT_DELETE|(model alias)|(model alias)
{{</message>}}

## 別のモーションに入れ替える

再生中のモーションを別のモーションに入れ替えるには **MOTION_CHANGE** を使います。入れ替え後、入れ替えたモーションの再生がスタートします。

{{<message>}}
MOTION_CHANGE|(model alias)|(motion alias)|other.vmd
{{</message>}}

入れ替えが成功したら、**MOTION_EVENT_CHANGE** が発行されると同時に、入れ替え後のモーションが最初から再生開始します。

{{<message>}}
MOTION_EVENT_CHANGE|(model alias)|(model alias)
{{</message>}}

## 巻き戻す

再生途中のモーションを巻き戻して最初から再生しなおすには **MOTION_RESET** を使います。

{{<message>}}
MOTION_RESET|(model alias)|(motion alias)
{{</message>}}
