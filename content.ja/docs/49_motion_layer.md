---
title: モーションの重ね
slug: motion-layer
---
# モーションの重ね

インタラクティブでリアルな対話を実現するためには、会話中に「お辞儀しながら話す」「手を振ってる途中で話しかけられたので手を振るのを止めて聞く」「発話している途中で何かに気づきつつ話を継続する」といった複合的な動作をその場で行える必要があります。MMDAgent-EX ではこのために、複数の部分的なモーションを組み合わせて並列再生する機構を備えています。

以下はモーションの重ね合わせの模式図です。図中の Glance.vmd は頭と顔だけを動かし、Response.vmd は手指と表情を動かすモーション（**部分モーション**）です。全てのモーションは並列に姿勢計算され、重なる部分は優先度の高いモーションが適用されます（ブレンドや加算等も設定次第で可能です）。この仕組みによって、その場のユーザの反応や状況に合わせてその場でモーションを組み合わせながら再生し、リアルタイムに複合的な動きを実現できます。

![motion blending](/images/motion_blending.png)

## Example のモーション重ね合わせデモを動かしてみる

Example の `example_motion` フォルダ内にモーション重ね合わせのデモがあるので動かしてみましょう。以下のように、`walk.vmd`, `gaze.vmd`, `onehandwave.vmd` の3つのモーションが定義されています。

    example/
        |- example_motion/
             |- example_motion.fst         FST script
             |- example_motion.mdf         .mdf file
             |- gaze.vmd                   motion: gaze
             |- onehandwave.vmd            motion: waving a hand
             +- walk.vmd                   motion: walking

`example_motion.mdf` を MMDAgent-EX で起動してください。下記のようにモーション `walk.vmd` がループ再生された状態で起動します。

{{< figure src="/mov/walk.gif" alt="walking gene" width="400px">}}

この状態で `1` キーを押してください。歩きながらジェネがこちらに目をやります。これは「左側を向く」だけが定義されているモーション `gaze.vmd` が、部分モーションとして再生され、歩きモーションに重ねて再生されています。

{{< figure src="/mov/walk-gaze.gif" alt="gazing while walking" width="400px">}}

さらに、こちらを向いている途中に `2` キーを押してみてください。こちらを見ながら手を振ります。これは上記2つにさらに「手を振る」モーション `onehandwave.vmd` を重ね合わせています。`onehandwave.vmd` は表情と右手の動きだけが定義されており、これを歩きモーションと並行して部分モーションとして再生することで、任意タイミングで挨拶を行うような制御を行うことができます。

{{< figure src="/mov/all.gif" alt="walking, gazing, and smiling" width="400px">}}

## モーションエイリアスと一覧表示

上記のデモの .fst スクリプト `example_motion.fst` を見てみると、以下のように、起動後 `1` キーを押されたタイミングで `gaze.vmd`が、`2` キーが押されたタイミングで `onehandwave.vmd` がそれぞれ `MODEL_ADD` で再生されます。

{{<fst>}}
0 LOOP:
    <eps> STAGE|../images/floor_block.png,../images/back_white.png
    <eps> MODEL_ADD|gene|../gene/gene.pmd
    MODEL_EVENT_ADD|gene  MOTION_ADD|gene|base|walk.vmd|FULL|LOOP
    <eps> CAMERA|0,11.25,0|13.5,-50.0,0|46.4|27.0

LOOP LOOP:
    KEY|1 MOTION_ADD|gene|look|gaze.vmd|PART|ONCE

LOOP LOOP:
    KEY|2 MOTION_ADD|gene|greet|onehandwave.vmd|PART|ONCE
{{</fst>}}

`MOTION_ADD` の際につけるモーションエイリアス名は重ねるモーションごとに異なるものを使います。上の例では、`walk.vmd` が "base", `gaze.vmd` が "look", `onehandwave.vmd` が "greet" というエイリアス名を指定しています。

動作中に `b` キーを押すことで実行中のモーションエイリアス名と各モーションの制御対象ボーンの一覧を以下のように表示します（もう一度 `b` キーで消えます）。緑色の文字がモデル名で、その下の水色の名前が実行中のモーションエイリアス名です。優先順の低いほうから高いほうへ順に表示されます。ピンク色の線は各モーションが制御しようとするボーンの簡易表示です。

![bone debug displays list of motion aliases in priority order](/images/bone.png)

## 重ね合わせ再生の詳細

### 部分モーション

以下のように第4引数に "**PART**" を指定することで、**部分モーション** として再生開始します。モーションを再生中のモデルに別のモーションを重ね再生するときは、常に指定します。

部分モーションは重ね合わせ用のモードで、モーション内で動きが定義されていない（=0フレーム目だけに定義がある）ボーン・モーフを無視して、動きが定義されている（=1フレーム目以降にキーフレームがある）ボーン・モーフだけを制御するようにします。

{{<message>}}
MOTION_ADD|gene|look|gaze.vmd|**PART**|ONCE
{{</message>}}

### ループ再生

モーションをループ再生する場合は `MOTION_ADD` の第5引数に **LOOP** を指定します。ループ指定されたモーションは最終フレームまで再生したら０フレーム目に戻り、ずっと再生されます。ループ再生は  `MOTION_DELETE` かモデルを削除することで止まります。

{{<message>}}
MOTION_ADD|gene|base|walk.vmd|FULL|**LOOP**
{{</message>}}

### スムージング

動いているモデルに途中から別のモーションを再生させると、継ぎ目の部分でモーション飛びが発生します。これを避けるため、MMDAgent-EX では各モーションの開始時と終了時のそれぞれ20フレーム間においてモーションスムージングが自動で行われます。何らかの理由でこれを OFF にしたい場合は、第6引数をOFFに指定してください。

{{<message>}}
MOTION_ADD|gene|look|gaze.vmd|PART|ONCE|**OFF**
{{</message>}}

## 発展：上書き・加算・乗算・ブレンド

複数のモーションが同じボーン・モーフを動かそうとするとき、デフォルトでは最も優先順位が高いモーション（デフォルト：あとで開始したモーション）だけ適用するようになっています。

この「上書き」の挙動は、モーションを追加した後に **MOTION_CONFIGURE** メッセージによって変更できます。デフォルトは `MODE_REPLACE` （上書き）ですが、 `MODE_ADD` を指定すれば、下位のモーションの動きにそのモーションの動きが加算されるようになります。`MODEL_MUL` は下位の動きで算出されたモーフ量に対してこのモーションが示すモーフ値を乗算するようになります（ `MODEL_MUL` はモーフにのみ有効）。

{{<message>}}
MOTION_CONFIGURE|(model)|(motion)|MODE_REPLACE
MOTION_CONFIGURE|(model)|(motion)|MODE_ADD
MOTION_CONFIGURE|(model)|(motion)|MODE_MUL
{{</message>}}

また、ブレンド率を指定することもできます。0.0 から 1.0 の値で、無指定時は 1.0 です。モーションの動きや変化に対して、このブレンド率を乗じてから、上書き・加算等の処理が行われます。それぞれ上記の指定時に追加の引数で指定できるほか、`BLEND_RATE` で随時変更することもできます。

{{<message>}}
MOTION_CONFIGURE|(model)|(motion)|MODE_REPLACE|(rate)
MOTION_CONFIGURE|(model)|(motion)|MODE_ADD|(rate)
MOTION_CONFIGURE|(model)|(motion)|MODE_MUL|(rate)
MOTION_CONFIGURE|(model)|(motion)|BLEND_RATE|(rate)
{{</message>}}

また、上記はモーション全体の指定ですがこれをボーン単位で詳細に設定することもできます。詳しくはリファレンスを見てください。
