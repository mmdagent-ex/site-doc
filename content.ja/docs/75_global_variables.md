---
title: グローバル変数を用いた連携
slug: global-variables
---
# グローバル変数を用いた連携

MMDAgent-EX はグローバル変数の格納領域を内部に持っており、.fst スクリプト、.mdf 設定ファイル、あるいはメッセージによって値を代入・変更・参照できます。

グローバル変数はキーと値のペア (key-value pair) の集合です。以下、値の代入・参照方法について解説します。

## .mdf で代入

以下の形で書かれた全てのペアが、key-value 値として起動時にグローバル変数に代入・保持されます。

{{<mdf>}}
KeyName=String
{{</mdf>}}

あとで設定の値を取り出すことができるほか、設定とは無関係の任意の key-value 値を .mdf 内に書いて定義することもできます。

## .fst で参照・代入

.fst 内では、任意の場所でグローバル変数を  `${%KeyName}` の形で値を参照できます。
値は .fst のロード時ではなく、その行を実行するタイミングで評価されます。

以下は **MODEL_ADD** メッセージの第1引数であるモデルエイリアス名として、グローバル変数のキー値 "`ModelName`" の値を代入する例です。（.fst での変数の扱いは[解説のページ](../fst-format)を見てください）

{{<fst>}}
0 LOOP:
    <eps> MODEL_ADD|${%ModelName}|...
{{</fst>}}

以下のように値そのものを条件として用いることも可能です。

{{<fst>}}
LOOP LOOP:
    ${%KeyName}==string SYNTH_START|mei|...
{{</fst>}}

[行末の追加フィールド](../fst-format/#%e3%83%ad%e3%83%bc%e3%82%ab%e3%83%ab%e5%a4%89%e6%95%b0)を使って値の代入も行えます。

{{<fst>}}
0 LOOP:
  ...
  <eps>  MODEL_ADD|mei|... ${%KeyName}=string
{{</fst>}}


## メッセージで代入

`KEYVALUE_SET` メッセージを発行することで値を代入できます。

{{<message>}}
KEYVALUE_SET|(key name)|(value)
{{</message>}}

## MODEL_BINDFACE でバインド

[`MODEL_BINDFACE` メッセージ](../motion-bind/#model_bindface)の別の使い方として、モーフを固定値ではなくグローバル変数にバインド（紐付け）することが可能です。バインドが指定されたモーフは、バインド先のグローバル変数の値で制御されるようになり、変数の値が変更されるたびにモーフが合わせてリアルタイムに追従変化します。

これを利用して、「ある特定のモーフの値を .mdf の設定値から与える」、あるいは「外部から **KEYVALUE_SET** メッセージで値を随時流し込むことで、外部から特定のモーフをリアルタイム制御する」ような使い方ができます。

{{<message>}}
MODEL_BINDFACE|(key name)|(min)|(max)|(model alias)|(morph name)|rate1|rate2
{{</message>}}

`min`, `max` はグローバル変数の値の最小値と最大値、`rate1`, `rate2` がそれぞれに対応するモーフ値の最小値と最大値です。`min` 以下の値は `rate1`に、`max`以上の値は `rate2` にキャップされます。間は線形補間です。図で表すと以下のようになります（横軸がグローバル変数の値、縦軸の1が`rate1`、2が `rate2` の値に対応）。

![BindBone](/images/bindbone.png)

`MODEL_UNBINDFACE` でバインドを解除できます。

{{<message>}}
MODEL_UNBINDFACE|(model alias)|(morph name)
{{</message>}}
