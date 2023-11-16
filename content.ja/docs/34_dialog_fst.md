---
title: 音声対話をためす (fst)
slug: dialog-test-fst
---
# 音声対話をためす (fst)

音声認識と音声合成が動けば、音声応答を作ることができます。スクリプト (.fst) を使った簡単な音声応答を試してみましょう。

{{< hint warning >}}
さきに[音声認識](../asr-setup)と[音声合成
](../tts-test)のセットアップを済ませてください。
{{< /hint >}}

## FST とは

MMDAgent-EX に標準のスクリプト (.fst) の仕組みと書き方を解説します。.fst は状態と動作の集合からなる有限状態オートマトンで、「あるメッセージが来たらこのメッセージを出力する」を1動作として状態ごとに動作を定義します。また、状態は動作によって遷移します。ここでは簡単な概要を説明します。

{{< hint info >}}
全ての仕様を知りたい方は[リファレンスの書式解説](../fst-format)をご覧ください。
{{< /hint >}}

### 基本形

.fst では1行ごとに動作を (1) 状態名、(2) 遷移先状態名、(3) 遷移条件、(4) 出力 で記述します。例えば、『状態 `Hoge` において、`KEY|1` メッセージが来たら「こんにちは！」と話して状態 `Foo` へ移行する』という動作は以下のように書きます。

{{<fst>}}
Hoge Foo  KEY|1 SYNTH_START|0|mei_voice_normal|こんにちは！
{{</fst>}}

### 複数の動作

同じ状態で複数の動作を記述すると、どの状態においてそれらは同時に評価され、満たしたほうが実行されます。例えば以下のようにすると、状態 `Hoge` では `KEY|1` と `KEY|2` の入力を待ち、どちらかが来たらそれぞれの動作を行います。

{{<fst>}}
Hoge Foo  KEY|1 SYNTH_START|0|mei_voice_normal|こんにちは！
Hoge Foo  KEY|2 SYNTH_START|0|mei_voice_normal|いかがですか？
{{</fst>}}

### 連続した動作

遷移先の状態からさらに遷移を書くことで、連続した動作を書くことができます。

{{<fst>}}
Hoge foo1  KEY|1 SYNTH_START|0|mei_voice_normal|こんにちは！
foo1 foo2  SYNTH_EVENT_STOP|0 SYNTH_START|0|mei_voice_normal|いかがですか？
{{</fst>}}

上記の例では、1行目で音声合成の開始メッセージを出したあとに状態 `Foo` で、その音声合成の終了イベント `SYNTH_EVENT_STOP|0` を条件とすることで音声合成終了を待っています。各モジュールは並列動作しており、.fst はメッセージを発行したら、発行したメッセージの結果を見ずに即座に次の状態へ遷移するので、何かの動作を待ちたい場合は、このようにメッセージを遷移条件として書きます。

### &lt;eps&gt;

空語 `<eps>` を条件にすると、その動作は条件なしで即座に実行されます。以下のように、音声合成とモーションを同時に再生開始することができます。

{{<fst>}}
Hoge foo1  KEY|1 SYNTH_START|0|mei_voice_normal|こんにちは！
foo1 foo2  <eps> MOTION_ADD|0|greet|motions/action/ojigi.vmd
{{</fst>}}

また出力のほうに `<eps>` を使うことで出力を行わないこともできます。

### ブロックによる記述

.fst スクリプトではしばしば、一連のメッセージを処理させるために連続した状態遷移を記述することがあります。以下は起動時（初期状態 "`0`"）から背景を設定し、モデルをロードし、モーションを設定してカメラを設定する、という一連のコマンドを .fst で記述したものです。

{{<fst>}}
0  s1  <eps> STAGE|images/floor_green.png,images/back_white.png
s1 s2  <eps> MODEL_ADD|0|gene/Gene.pmd
s2 s3  MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
s3 ss  <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0
{{</fst>}}

これは MMDAgent-EX では以下のようにブロックで記述することができます。1行目にはこのブロックの最初と最後の状態名を書き、続けてインデントして記述します。

{{<fst>}}
0  ss:
    <eps> STAGE|images/floor_green.png,images/back_white.png
    <eps> MODEL_ADD|0|gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0
{{</fst>}}

## 一問一答を作ってみる

Example の `main.fst` を編集して、簡単な一問一答を作ってみましょう。

Example の `main.fst` をテキストエディタで開き、末尾に以下を新たに追加してください。これは「音声認識結果を含む `RECOG_EVENT_STOP` メッセージが発行されたら、音声合成の実行を指示する `SYNTH_START` メッセージを発行する」という、一問一答の最も簡単な形です。

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|こんにちは。 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！
{{</fst>}}

{{< hint info >}}
.fst はインデントに意味があります。ブロックの１行目はインデントなし、２行目以降はインデントありにしてください。インデントの幅は自由です。
{{< /hint >}}

編集後、コンテンツを起動して「こんにちは」と話しかけてみてください。エージェントから「こんにちは、よろしくね」と返ってくれば成功です。

<img width="480" alt="snapshot" src="/images/example_2.png"/>

## 表情をつける

発話に表情をつけてみましょう。発話の開始と同時に表情モーションを再生します。先ほど追加した部分に、以下のように末尾の行を新たに追加してみてください。

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|こんにちは。 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE</b>
{{</fst>}}

`.fst` を保存して試して見ましょう。MMDAgent-EX を閉じてもう一度起動するか、あるいは `Shift+r` キーでリロードします。もういちど「こんにちは」と話しかけ、応答しながら笑顔になることを確かめてください。

## 表情と動作を並行して行う

表情と一緒に動作も行うようにしてみます。先ほど追加した行の上に、以下の太字の行を追加してください。 

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|こんにちは。 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE</b>
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{</fst>}}

保存してリロードしたら話しかけて、笑顔になりながらお辞儀を行うのを確かめてください。

無条件実行である `<eps>` を使うことで、１つ目の `MOTION_ADD` と２つ目の `MOTION_ADD` が時間差なしに連続して MMDAgent-EX へ渡されます。MMDAgent-EX では、複数のモーションを同時に重ね合わせて再生できます。

## .fst の概要

ここで .fst について簡単に紹介します。 .fst は有限状態オートマトン（正確には有限状態トランスデューサー）として動作を記述するスクリプトで、簡単に言えば「何が起きたらどうするか」を順に記述するものです。

現在の .fst は以下のようになっており、例えば冒頭の５行目までのブロックでは

- 起動後、床と背景の画像を設定し
- モデルを読み込み
- 読み込みが終わったら、待機モーションをループ再生し
- カメラ位置を設定する
- 上記が終わったら "LOOP" という名前の状態へ移動

という一連の処理を定義しています。

{{<fst>}}
0 LOOP:
    <eps> STAGE|images/floor_green.png,images/back_white.png
    <eps> MODEL_ADD|0|gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0

LOOP LOOP:
    KEY|1 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！

LOOP LOOP:
    RECOG_EVENT_STOP|こんにちは。 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{< / fst>}}

MMDAgent-EXでは命令コマンドやイベント通知をすべてメッセージングで行なっています。.fst では、条件を満たすメッセージが来るまで待機（ブロック）し、条件を満たすメッセージが来たら対応するメッセージを発行して次の行に移動する、というのが基本的な仕組みです。同じ状態名から始まるブロックが複数ある場合、条件を先に満たしたブロックが実行されます。また、"`<eps>`" は「指定なし」を表し、条件部では何も待たずに即座にメッセージを発行して次へ行く、という表記です。

.fst はオートマトンベースでさまざまなインタラクションを記述できます。ここでの解説はここまでとしますが、.fst について詳しくは [FST書式](../fst-format) を参照してください。

{{< hint info >}}
VS Code で .fst の編集を助けるための [VS Code 用の .fst ファイル拡張](https://marketplace.visualstudio.com/items?itemName=MMDAgent-EX.dialogue-fst-editing-support) を公開しています。併せてご利用ください。
{{< /hint >}}

## 追加：スクリプトを拡張してみる

.fst スクリプトの機能を使って実現できる範囲で、もう少し対話をうまく記述する方法を紹介します。

### OR条件の設定

「こんにちは」だけでなく「ハロー」と言っても同じ応答が返ってくるようにしてみましょう。複数の条件にマッチさせたい場合は、 "`+`" を使って並列ノードを追加定義します。

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|こんにちは。 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！
    +RECOG_EVENT_STOP|ハロー。</b>
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{< / fst>}}

このように "`+`" に続いて条件項だけを書くことで、その直前の行の条件に、OR で条件を追加することができます。どちらにマッチしても最初の行のメッセージ項目（例では `SYNTH_START`）が実行され、次の行に移動します。

"`+`" の行に条件だけでなく発行メッセージも記述すると、発行メッセージも並列にできます。以下は「こんにちは」で「こんにちは！よろしくね！」、「ハロー」で「ハロー、ありがとうございます！」と返すようにする例です。どちらも実行後は次のモーション再生の行へ移動します。

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|こんにちは。 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！
    +RECOG_EVENT_STOP|ハロー。 SYNTH_START|0|mei_voice_normal|ハロー、ありがとうございます！</b>
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{< / fst>}}

"`+`" 行は複数個書くことができます。以下は「こんにちは」「ハロー」に加えて「ボンジュール」と言った場合にも同じ応答を返すよう拡張した例です。

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|こんにちは。 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！
    +RECOG_EVENT_STOP|ハロー。
    +RECOG_EVENT_STOP|ボンジュール。
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{< / fst>}}

完全に別の処理としたい場合は個別のブロックに分けるとよいでしょう。以下は「こんにちは」はそのままで、「ハロー」というと「ハロー、ありがとうございます！」と言いながら手を振るようにしたものです。同じ状態から始まるブロックを定義することで、各ブロックの１行目の条件でどのブロックが動作するかが分かれます。

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|こんにちは。 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE

LOOP LOOP:
    RECOG_EVENT_STOP|ハロー。 SYNTH_START|0|mei_voice_normal|ハロー、ありがとうございます！
    <eps> MOTION_ADD|0|action|motions/action/wavehands.vmd|FULL|ONCE
    <eps> MOTION_ADD|0|emote|gene/motion/10_impressed.vmd|PART|ONCE
{{< / fst>}}

### 連続した動作

.fst を用いて連続した一連の動作を記述する例を示します。以下は「こんにちは」に対する反応を、

1. 「こんにちは」と返しながらお辞儀する
2. お辞儀が終わってから笑顔でhappy声で「よろしくね」

の順で２段階に分けて実行するようにしたものです。

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|こんにちは。 SYNTH_START|0|mei_voice_normal|こんにちは！
    <eps> MOTION_ADD|0|action|motions/action/ojigi.vmd|FULL|ONCE
    MOTION_EVENT_STOP|0|action</b> SYNTH_START|0|mei_voice_happy|よろしくね！
    <eps> MOTION_ADD|0|emote|gene/motion/03_smile.vmd|PART|ONCE
{{< / fst>}}

ポイントはお辞儀モーションの終了を待つ部分です。
お辞儀モーション終了時にMMDAgent-EX は `MOTION_EVENT_STOP|0|action` を発行するので、この .fst では `MOTION_EVENT_STOP|0|action` を待ってから次の動作を行うように記述しています。

このように、任意のイベントを待って、任意のイベントを出力する、という手順の積み重ねでインタラクションを記述していくのが .fst の基本です。

## 正規表現を使う

条件判定は完全一致で、記述内容とメッセージのテキストが一致する場合にのみマッチしますが、正規表現を使うことでより柔軟なマッチングを記述できます。正規表現を使う場合、条件項を "`@`" で囲みます。例えば、上記で

{{<fst>}}
LOOP LOOP:
    RECOG_EVENT_STOP|こんにちは。 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！
    +RECOG_EVENT_STOP|ハロー。
{{< / fst>}}

のように書いた部分は、正規表現を使って以下のように書くこともできます。条件項が正規表現の場合、メッセージがその正規表現にマッチするかどうかで判定されます。

{{<fst>}}
LOOP LOOP:
    @RECOG_EVENT_STOP¥|(こんにちは|ハロー)。@</b>  SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！
{{< / fst>}}

特殊な用途ですが、以下のように書くことで、認識結果のおうむ返しも記述できます。発行メッセージ項にある "`${1}`" は、正規表現の中でマッチする最初の括弧内の文字に対応する文字で置き換えられます。

{{<fst>}}
LOOP LOOP:
    @RECOG_EVENT_STOP¥|(.*)@</b>  SYNTH_START|0|mei_voice_normal|${1}
{{< / fst>}}

正規表現は全体マッチです。

### 重なる場合の処理

複数の条件にマッチする場合、前の方で定義されたものが優先されます。
