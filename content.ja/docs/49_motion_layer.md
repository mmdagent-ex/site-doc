---
title: モーションの重ね
slug: motion-layer
---
# モーションの重ね

インタラクティブでリアルな対話を実現するためには、会話中に「お辞儀しながら話す」「手を振ってる途中で話しかけられたので手を振るのを止めて聞く」「発話している途中で何かに気づきつつ話を継続する」といった複合的な動作をその場で行える必要があります。MMDAgent-EX ではこのために、複数の部分的なモーションを組み合わせて並列再生する機構を備えています。

以下はモーションの重ね合わせの模式図です。図中の Glance.vmd は頭と顔だけを動かし、Response.vmd は手指と表情を動かすモーション（**部分モーション**）です。全てのモーションは並列に姿勢計算され、重なる部分は優先度の高いモーションが適用されます（ブレンドや加算等も設定次第で可能です）。この仕組みによって、その場のユーザの入力や状況に合わせてその場でモーションを組み合わせながら再生し、リアルタイムに複合的な動きを実現できます。

![motion blending](/images/motion_blending.png)

## Example のモーション重ね合わせデモを動かしてみる

Example の `example_motion` フォルダ内にモーション重ね合わせのデモがあるので動かしてみましょう。

    example/
        |- example_motion/
             |- example_motion.fst         FST script
             |- example_motion.mdf         .mdf file
             |- gaze.vmd                   motion: gaze
             |- onehandwave.vmd            motion: waving a hand
             +- walk.vmd                   motion: walking

`example_motion.mdf` を MMDAgent-EX で起動してください。下記のようにモーション `walk.vmd` がループ再生された状態で起動します。

{{< figure src="/mov/walk.gif" alt="walking gene" width="400px">}}

この状態で `1` キーを押すと、ジェネがこちらに目をやります。これは「左側を向いて見る」だけのモーション `gaze.vmd` を歩きモーションに重ね再生しています。

{{< figure src="/mov/walk-gaze.gif" alt="gazing while walking" width="400px">}}

さらに、`2` キーで手を振るモーション `onehandwave.vmd` が重ね再生されます。`onehandwave.vmd` は笑顔の表情および右腕の動きだけが定義されたモーションで、これを歩きモーションや左を向くモーションと重ねて再生することで、「任意のタイミングでこちらを見て挨拶を行う」ような制御を行える様子を見ることができます。

{{< figure src="/mov/all.gif" alt="walking, gazing, and smiling" width="400px">}}

## モーションエイリアスと一覧表示

上記のデモの .fst スクリプト `example_motion.fst` を見てみると、以下のように、起動後 `1` キーを押されたタイミングで `gaze.vmd`が、`2` キーが押されたタイミングで `onehandwave.vmd` がそれぞれ `MODEL_ADD` で再生されるよう記述されていることが分かります。

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

`walk.vmd` が "base", `gaze.vmd` が "look", `onehandwave.vmd` が "greet" というように、それぞれ異なるモーションエイリアス名をつけます。これらの並行再生されるモーションの管理は互いに独立であり、それぞれ個別に `MOTION_DELETE` や `MOTION_CHANGE` で制御することができます。

動作中に `b` キーを押すことで、現在実行中のモーションの情報を見ることができます。以下は表示例です（もう一度 `b` キーで消えます）。緑色の文字がモデル名です。その下の水色の名前がモーションエイリアス名で、優先順の低いほうから高いほうへ順に表示されます。ピンク色の線は各モーションが再生するボーンの動きの簡易表示です。

![bone debug displays list of motion aliases in priority order](/images/bone.png)

## 重ね合わせ再生の詳細

重ね合わせ再生に関連する `MOTION_ADD` メッセージの詳細な仕様を説明します。

### 部分モーション指定

モーションを重ね再生するときは、あとで重ねる側のモーションを、全身モーションではなく動きのあるパーツだけ制御する「**部分モーション**」として開始する必要があります。

部分モーションとして再生するには、`MOTION_ADD` で以下のように第4引数に "**PART**" を指定します。

{{<message>}}
MOTION_ADD|gene|look|gaze.vmd|**PART**|ONCE
{{</message>}}

部分モーションとして開始されたモーションは、そのモーション内で動きが定義されていない（=0フレーム目だけに定義がある）ボーン・モーフを無視し、動きが定義されている（=1フレーム目以降にキーフレームがある）ボーン・モーフの動きだけが適用されます。

通常の全身モーションとして扱う場合は **FULL** を指定します。省略した場合のデフォルトは FULL です。

### ループ再生指定

通常のモーション再生では、モーションの最終フレームまで再生したらそのモーションは自動的に消えます。これを、最初のフレームに戻ってループ再生するよう指定することができます。

モーションをループ再生したい場合は `MOTION_ADD` の第5引数に **LOOP** を指定します。ループ指定されたモーションは最終フレームまで再生したら０フレーム目に戻り、ずっと再生されます。ループ再生は  `MOTION_DELETE` かモデルを削除することで止まります。

{{<message>}}
MOTION_ADD|gene|base|walk.vmd|FULL|**LOOP**
{{</message>}}

1回のみ再生を明示的に指定するには **ONCE** を指定します。省略した場合のデフォルトは ONCE です。

### スムージングを切り替える

重ね合わせ再生時に継ぎ目の部分でモーションの飛びが発生するのを避けるため、MMDAgent-EX ではモーションの開始時と終了時に自動でモーションスムージングが入ります。何らかの理由でこれを OFF にしたい場合は、第6引数をOFFに指定してください。

{{<message>}}
MOTION_ADD|gene|look|gaze.vmd|PART|ONCE|**OFF**
{{</message>}}
