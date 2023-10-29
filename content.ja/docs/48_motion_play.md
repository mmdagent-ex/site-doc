---
title: モーションの再生
slug: motion-play
---
# モーションの再生

シンプルな一問一答の対話システムでは、お互いが相手の発話が終わってから話すという前提をおくことが多々あります。一方で、よりインタラクティブでリアルな対話を実現するためには、「お辞儀しながら話す」「手を振ってる途中で話しかけられたので手を振るのを止めて聞く」「発話している途中で何かに気づきつつ話を継続する」といった複合的な動作を行える必要があります。

MMDAgent-EX ではこのために、複数のモーションをパーツのように組み合わせて並列再生する機構を備えています。

- 身体の一部だけを動かす「部分モーション」
- 複数のモーションの並列再生およびそれらのリアルタイム重ね合わせ
- モーション間の重ね合わせ状態の制御

これらの機構によって、その場のユーザの反応や状況に合わせてその場でモーションを組み合わせ、リアルタイムに複合的な動きを再生できます。

ここでは手始めに、モデルに対して単一のモーションを再生する手順を紹介します。

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
