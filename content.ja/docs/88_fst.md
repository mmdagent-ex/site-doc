---
title: FST書式
slug: fst-format
---
# FST の書式

## はじめに

MMDAgent-EX の動作スクリプトは、条件と動作を状態遷移モデルで記述する。ファイル拡張子は .fst である。

実行時、MMDAgent-EX は常にとある１状態にある。モジュールはMMDAgent内に流れるメッセージ（入力メッセージ）を監視し、現状態において待ち受けている条件のうちどれかに入力メッセージがマッチしたら、対応するメッセージをMMDAgentに出力して、遷移先の状態へ遷移する。これを繰り返して対話シナリオが実行される。

MMDAgent-EX では .fst の仕様がオリジナルの MMDAgent から拡張されたが、互換性は保たれており、オリジナル用の古い .fst もそのまま使用可能である。

MMDAgent では `Shift+f` キーで .fst のデバッグウィンドウが内部に表示される。また `e` キーで実行中の fst ファイルをエディタで開くことができる。動作の確認に活用されたい。

サブFSTの使い方。

## VSCode 拡張

.fst ファイル用の VS Code 拡張をリリースしているので使ってみてください。

https://marketplace.visualstudio.com/items?itemName=MMDAgent-EX.dialogue-fst-editing-support

以下のような機能があります。

- メッセージの仕様や引数を教えてくれる入力アシスト
- 遷移先がない状態、どこからも遷移されない状態などの注意すべき状態の検出
- 状態名を指定してその定義先へ移動する機能
- 状態名へ飛んでくる参照元の一覧表示

## 概要

.fst ファイルはテキストファイル。`#` から始まる行はコメントで無視される。

以下は例。この例では、まず背景画像を設定し、モデルファイルのロードとモーション再生を行い、カメラパラメータをセットしたら、`MAINLOOP` という名前の状態へ遷移するよう書かれている。 `MAINLOOP` 状態では、各種キー入力に対して対応するメッセージを送信してまた `MAINLOOP` 状態に戻るように記述されている。

`<eps>` は FST における空語を表す。すなわち、条件フィールドに `<eps>` がある場合、それは常にTRUEとなり、その行は入力を待たずに次へ進む。また、出力フィールドに `<eps>` がある場合、そこでは何も出力せずに進む。

{{<fst>}}
# initial values
${agentPMD}="Agents/mai/mai.pmd"
${camera_default}="1.7,12.7,0.0|0.0,0.0,0.0|44|16|1"

# begins with state "0"
0 MAINLOOP:
  <eps>                    STAGE|floor.png,back.jpg
  <eps>                    CAMERA|${camera_default}
  <eps>                    MODEL_ADD|0|${agentPMD}
  MODEL_EVENT_ADD|0        MOTION_ADD|0|base|waiting.vmd|FULL|ONCE|OFF|OFF
  MOTION_EVENT_ADD|0|base  <eps>

MAINLOOP MAINLOOP:
  KEY|1 MOTION_ADD|0|ojigi|mei_greeting.vmd|FULL|ONCE|ON|OFF

MAINLOOP MAINLOOP:
  KEY|2 SYNTH_START|0|mei_voice_normal|こんにちは。

MAINLOOP MAINLOOP:
  KEY|9 AVATAR_LOGSAVE_START|log.txt

MAINLOOP MAINLOOP:
  KEY|0 AVATAR_LOGSAVE_STOP
{{</fst>}}

## 基本書式

インデントが重要。状態名の行はインデントなしで、遷移を記述する行はインデントする。これは必須。

状態名は任意の文字列が可能。旧来の MMDAgent では数字だけだったが最新版は任意の文字列を使える。初期状態を表す状態IDは "`0`" （数字のゼロ）で固定。

各フィールドは空白もしくはタブで区切る。パス名等で空白を含む値を指定するときは `""` あるいは `''` を使う。

{{<fst>}}
name1 name2:
    input_message1 output_message2
    input_message2 output_message2
    ...

name2 name3:
    ...
{{</fst>}}

## 遷移の記述の詳細

`name1`, `name2`, ... は状態名であり、１つ目が現状態、２つ目が遷移先状態を表す。その次の行からインデントしている範囲の行が、その2つの状態間の動作定義列を表す。それぞれ `input_message` が遷移条件のフィールド、`output_message` が実行時に出力するメッセージを表すフィールドとなる。

動作定義が複数行にわたってかくことができる。複数行記述されている場合は、上から順に順次サブ状態として処理される。すなわち、上記の例で現状態が `name1` になったとき、まずは `input_message1` 待つ。それが届いたら `output_message2` を出力して、次の行の `input_message2` を待つ。そして `input_message2` に対応するメッセージが来たら `output_message2` を発行して・・・というように順に繋がっていき、そのブロックの最後の行が終わったら `name2` で指定された状態名へ遷移する。

同じ状態名で始まる複数のブロックを定義した場合、.fst ファイル上で先に定義されたほうから評価される。つまり、以下のような例でもし入力が `input_message1` と `input_message1` の両方にマッチしたときは上側が優先される。

{{<fst>}}
name1 name2:
    input_message1 output_message1

name1 name3:
    input_message2 output_message2
    ...
{{</fst>}}

## ローカル変数

.fstごとにローカル変数を定義・代入・参照できる。扱いは .fst ごとに閉じており、他のサブ .fst やプラグインとは共有されない。

.fst ファイルの最初の部分（最初の状態定義より前）で初期値を指定できる。

{{<fst>}}
${agentPMD}="Agents/mai/mai.pmd"
${camera_default}="1.7,12.7,0.0|0.0,0.0,0.0|44|16|1"
{{</fst>}}

条件フィールドと出力フィールドにおいてローカル変数を参照できる。`${変数名}` と書くことで、その部分を実行時に（評価される瞬間に）その時点でのそのローカル変数の値に入れ替えて、評価や実行が行われる。

{{<fst>}}
XXX YYY:
    <eps> MODEL_ADD|mei|${agentPMD}
{{</fst>}}

条件フィールドで、ローカル変数の値を遷移の条件とすることが可能。文字列として一致するかどうかだけ行える。比較演算子は `==` と `!=` のみ。

{{<fst>}}
XXX YYY:
    ${flag}==xxx  MODEL_ADD|mei|...

WWW ZZZ:
    ${flag}!=yyy  MODEL_ADD|mei|...
{{</fst>}}

実行時の値の変更や代入は各遷移の末尾に追加のフィールドとして記述する。変数どうしを参照することも可能。

{{<fst>}}
XXX YYY:
  <eps>            <eps>  ${place}=Nagoya

ZZZ QQQ:
  MODEL_ADD|mei|.. <eps>  ${value}=${src}/${dst}
{{</fst>}}

複数の値を一度に代入することも可能。

{{<fst>}}
XXX YYY:
  <eps>  <eps>  ${src}=Nara,${dst}=Tokyo,${pref}=nozomi
{{</fst>}}

## グローバル変数

`${%グローバル変数名}` のように変数名の冒頭に `%` を付けることで[グローバル変数](./75_global_variables.md)への参照、およびグローバル変数への書き込みが行える。グローバル変数の初期値は .mdf で設定でき、値は他の FST やプラグイン間で共有される。

{{<fst>}}
XXX YYY:
  <eps>            <eps>  ${place}=${%KeyName}
{{</fst>}}

## 環境変数

`${%ENV{環境変数名}}` で環境変数の値を参照できる。 (2025.7.9以降のバージョン)

{{<fst>}}
XXX YYY:
  <eps>            <eps>  ${place}=${%ENV{PLACE_NAME}}
{{</fst>}}

## 条件フィールドの書き方

### プレーンテキスト

下記のどれにも当てはまらない文字列を条件フィールドに書いた場合、それは、それと厳密に一致する入力メッセージにマッチする。

### 変数値

ローカル変数の値を遷移条件にできる。この条件は入力メッセージには依存せず、与えられた式の評価がTRUEの場合に遷移が起こる。比較演算子は `==` と `!=` のみ。

{{<fst>}}
XXX YYY:
    ${flag}==xxx  MODEL_ADD|mei|...

WWW ZZZ:
    ${flag}!=yyy  MODEL_ADD|mei|...
{{</fst>}}

式の評価は、その状態に遷移した直後の1回のみである点に注意。式が成立するかどうかは状態に遷移してきた直後にのみ評価され、状態滞在中に式が成立しても反応しない。

### 正規表現

正規表現によるテキストマッチングを使える。書き方は、条件フィールド全体を `@` でくくる。以下は認識結果 (`RECOG_EVENT_STOP`) に `Station` もしくは `station` を含むメッセージが到来したときに条件マッチする遷移の記述例である。

{{<fst>}}
XXX YYY:
    @RECOG_EVENT_STOP\|.*[Ss]tation.*@  <eps>
{{</fst>}}

`@` で囲まれた範囲は正規文法エンジンにそのまま投げられるので、例のように `|` は `\|` とする必要がある等、注意せよ。正規表現ライブラリは [Google RE2](https://github.com/google/re2) を利用している。書式は[Googleのドキュメント](https://support.google.com/a/answer/1371417?hl=ja)等を参考にすること。

部分マッチではなくフルマッチである点に注意せよ。以下のように一部だけひっかかる正規表現ではマッチしない。メッセージ全体がマッチするように正規表現を書く。

{{<fst>}}
# だめな例
XXX YYY:
    @[Ss]tation@  <eps>
{{</fst>}}

正規表現を評価したあと、括弧でくくられたサブマッチ範囲がローカル変数 `${1}`, `${2}` 等に自動代入される。これを用いてマッチした部分をローカル変数に取り出すことができる。例えば、以下は `MOTION_EVENT_ADD` メッセージからモデルエイリアス名とモーションエイリアス名を `${model}`, `${motion}` に取り出す場合の例。

{{<fst>}}
XXX YYY:
    @MOTION_EVENT_ADD\|(.*)\|(.*)@ <eps> ${model}=${1},${motion}=${2}
{{</fst>}}

## %INCLUDE

.fst 内で

{{<fst>}}
%INCLUDE("ファイル名.fst")
{{</fst>}}

のようにすることで、指定されたファイルをその場所にインクルードできる。

インクルードは .fst を読むときに展開され、中身がそのまんまその場に展開された状態で解釈される。
状態名や変数も特にスコープ処理等は行わっていない。
状態名の競合や処理の整合性には、十分注意すること。

## 並列FST起動（サブFST）

MMDAgent-EX ではメインのFST以外に複数のサブFSTを並列に走らせることができる。サブFSTはメインFSTと同様にメインキューに接続され、その出力はメインキューに投げられる。

サブFSTはメインFSTと並列に起動する。入力はサブFSTにもカスケードされ、サブFSTの出力はメッセージキューに流される。サブFSTはメインFSTとは独立に動く。任意数のサブFSTを起動することができる。

ローカル変数は各 FST ごとに独立である。なお、KeyValue 値は MMDAgent-EX 本体のメモリのため各FST間で共有することができる。

### 起動方法１：静的

メインの FST ファイル が

```text
foobar.fst
```

であるとき、以下のような名前の .fst ファイルを置いておく。

```text
foobar.fst.xxx.fst
```

MMDAgent-EX は起動時、メインのFSTファイルと同じ場所に上記のような名前の .fst ファイルがあるかどうか調べ、ある場合それらすべてをサブFSTとして起動時にメインFSTと同時に開く。

### 起動方法２：動的

メッセージ **SUBFST_START** を発行することで、サブFSTの実行を開始できる。外部からの投げ込みで起動させたり、既存の動作中の FST からイベントに応じて別のサブFSTを起動するようなこともできる。
`alias` は起動するサブFSTに付ける任意のエイリアス名を指定する。

{{<message>}}
SUBFST_START|alias|file.fst
{{</message>}}

上記の指定では指定したファイル `file.fst` が開けない場合はエラーになる。そのファイルの存在を調べ、存在するときだけ起動する場合は **SUBFST_START_IF** を使う。

{{<message>}}
SUBFST_START_IF|alias|file.fst
{{</message>}}

サブFSTが動作を開始したとき、イベント **SUBFST_EVENT_START** が発行される。

{{<message>}}
SUBFST_EVENT_START|alias
{{</message>}}

起動したサブFSTは状態名 `0` から動作を開始する。全てのサブFSTはメインFSTと並列に動作する。

### サブFSTの終了

サブFSTは **次の遷移先が定義されていない状態（終端状態）に到達したとき、即座に動作を終了する**。動作終了時に **SUBFST_EVENT_STOP** メッセージが発行されるため、他のモジュールはこのメッセージを見てモジュールが終了したかどうかを判定できる。

{{<message>}}
SUBFST_EVENT_STOP|alias
{{</message>}}

もしFSTがメッセージ待ちやループ状態等を保ち何らかの終端状態に達さない場合、そのサブFSTは動き続ける。これを止めるには次の **SUBFST_STOP** を使う。

### サブFSTの強制停止

稼働中のサブFSTは **SUBFST_STOP** メッセージを送ることでその場で強制終了できる。この場合も終了時には**SUBFST_EVENT_STOP** メッセージが発行される。

{{<message>}}
SUBFST_STOP|alias
{{</message>}}

### `AT_EXIT` 状態

**SUBFST_STOP** メッセージによる終了命令を受けたとき、そのサブFSTに `AT_EXIT` という名前の状態が定義されている場合は、そのサブFSTは即座に停止せず、代わりに `AT_EXIT` 状態へ強制遷移し、以降の命令を実行する。この `AT_EXIT` を使うことで、例えばサブFSTで表示させたモデルを終了させてから処理を終わる、等、終了時に常に実施する終了処理を記述することができる。

`AT_EXIT` へ遷移後もそのサブFSTは `AT_EXIT` 状態から通常通り動作を行い続ける。そのため、ここで他モジュールからのメッセージを待ったりループ処理を書くと、サブFSTが落ちない要因になりうる。`AT_EXIT` を使う場合、スクリプト制作者は責任をもって `AT_EXIT` から終了状態へ達しサブFSTが終了するよう書くこと。