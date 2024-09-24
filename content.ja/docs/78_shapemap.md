---
title: Shapemap
slug: shapemap
---

{{< hint ms >}}
本ページの以下の内容は、すべてムーンショット版のみの内容です。
{{< /hint >}}

# Shapemap ファイル

Shapemap ファイル (.shapemap) は、CGアバターで自動リップシンクおよび外部API制御を行うための定義ファイルです。音声からの自動リップシンクや外部APIからのトラッキング命令に対して、CGモデルの「どの部位を」「どのように」対応させて動かすかを指定します。

MMDAgent-EX はデフォルトの shapemap ファイルを持っており、何も指定していないモデルにはデフォルトの shapemap 情報が適用されます。さらに、モデルごとに個別の shapemap を定義することも可能です。

## デフォルトの shapemap ファイル

システムのデフォルト shapemap は `AppData/default.shapemap` にあります。モデルが個別の shapemap を持たない場合、このファイルが shapemap 定義として用いられます。

## ファイル設置場所

モデルごとに個別の shapemap を定義するには、CGアバターのモデルファイル `xxx.pmd` が置いてあるフォルダと同じフォルダに、 `xxx.pmd.shapemap` のようにモデルファイル名の後ろに `.shapemap` を付けたファイル名で shapemap ファイルを置きます。

## 例

Shapemap ファイルはテキストファイルです。`#` で始まる行はコメントで無視されます。以下は CG-CA に付属の shapemap の例です。

{{< details "CG-CA に付属の .shapemap" close>}}

```text
#### リップシンク用モーフ名
LIP_A あ
LIP_I い
LIP_U う
LIP_O お

#### リップシンク中に０にリセットするモーフ名のリスト
NOLIP え,おお~,ワ,∧,はんっ！,えー,にやり,にっこり,口締め,結び,む,ああ,いい,にたり,叫び,あーれー,口わらい,mouth_a_geo_C,mouth_i_geo_C,mouth_u_geo_C,mouth_e_geo_C,mouth_o_geo_C,mouth_oh_geo_C,mouth_smile_geo_C,mouth_surprise_geo

#### ヘッドトラッキング設定
## 制御対象ボーン
TRACK_HEAD 頭
TRACK_NECK 首
TRACK_LEFTEYE 左目
TRACK_RIGHTEYE 右目
TRACK_BOTHEYE 両目
TRACK_BODY 上半身2,上半身２,上半身1,上半身
TRACK_CENTER センター
## 目の回転量の係数
EYE_ROTATION_COEF 0.4

#### プリセットモーション指定。プリセットアクション使用時に設定
## __AV_ACTION に対応するモーションファイル名を指定
ACT0  motion/00_normal.vmd
ACT1  motion/01_happy.vmd
ACT2  motion/02_laugh.vmd
ACT3  motion/03_smile.vmd
ACT4  motion/04_littlesmile.vmd
ACT5  motion/05_gracefulsmile.vmd
ACT6  motion/06_embarassedsmile.vmd
ACT7  motion/07_annoyedsmile.vmd
ACT8  motion/08_surprise.vmd
ACT9  motion/09_unexpected.vmd
ACT10 motion/10_impressed.vmd
ACT11 motion/11_admiration.vmd
ACT12 motion/12_expectant.vmd
ACT13 motion/13_convinced.vmd
ACT14 motion/14_crisp.vmd
ACT15 motion/15_proud.vmd
ACT16 motion/16_thinking.vmd
ACT17 motion/17_nothankyou.vmd
ACT18 motion/18_compassion.vmd
ACT19 motion/19_triumphant.vmd
ACT20 motion/20_introuble.vmd
ACT21 motion/21_disgust.vmd
ACT22 motion/22_apology.vmd
ACT23 motion/23_stressed.vmd
ACT24 motion/24_embarrasing.vmd
ACT25 motion/25_sharpeyessuspicion.vmd
ACT26 motion/26_mortifying.vmd
ACT27 motion/27_provoking.vmd
ACT28 motion/28_sleepy.vmd
ACT29 motion/29_Terrified.vmd
ACT30 motion/30_stunned.vmd
ACT31 motion/31_disappointed.vmd
ACT32 motion/32_frustrated.vmd
ACT33 motion/33_angry.vmd
ACT34 motion/34_sad.vmd
ACT35 motion/35_Afraid.vmd
ACT36 motion/36_Anxious.vmd
ACT37 motion/37_Sentimental.vmd
ACT38 motion/38_Ashamed.vmd

#### 個別制御の設定 それぞれ利用する場合に設定
## __AV_EXBONE で使用される name に対応するボーン名
## ボーンの記述方法は TRACK と同じ
#EXBONE_name ボーン名

## __AV_EXMORPH で使用される name に対応するフェイス名
## モーフの記述方法は AU や ARKIT と同じ
#EXMORPH_name モーフ名

## __AV_AU 用の Action Unit 番号に対応するモーフ名。AU使用時に指定
##  モーフ名 のみの場合、値をそのまま重みにマッピング
##  モーフ名 >閾値 の場合、値 < 閾値 なら 0.0,値 >= 閾値なら 1.0
##  モーフ名 係数 の場合、値に係数倍したものを重みにマッピング（係数はゼロ以上、負はNG）
##  モーフが複数のAUに対応付けられている場合は加算される
##  一つの AU で複数のモーフを動かす場合、対象モーフごとに指定する
##  ここに書かれていないAUは無視される
AU6 笑い >0.7
AU1 上 0.5
AU2 上 0.5
AU4 困る
AU5 見開き
AU12 にこり
AU45 まばたき
## モーフ調律集合：左から優先で重みが合計1になるよう事後調整
## 複数定義可能（最大30個）。1つあたり10種まで。
MORPH_TUNE 笑い まばたき

## __AV_ARKIT用の ARKit シェイプ名に対応するモーフ名。ARKit 使用時に指定
##  モーフ名 のみの場合、値をそのまま重みにマッピング
##  モーフ名 >閾値 の場合、値 < 閾値 なら 0.0,値 >= 閾値なら 1.0
##  モーフ名 係数 xの場合、値に係数倍したものを重みにマッピング（係数はゼロ以上、負はNG）
##  モーフが複数のシェイプに対応付けられている場合は加算される
##  1つのシェイプで複数のモーフを動かす場合、対象モーフごとに指定する
##  ここに書かれていないシェイプは無視される

browDown_L browDownLeft 
browDown_R browDownRight 
browInnerUp browInnerUp 
browOuterUp_L browOuterUpLeft 
browOuterUp_R browOuterUpRight 

cheekPuff cheekPuff 
cheekSquint_L cheekSquintLeft 
cheekSquint_R cheekSquintRight 

eyeBlink_R eyeBlinkRight 
eyeBlink_L eyeBlinkLeft 
eyeLookDown_L eyeLookDownLeft 
eyeLookDown_R eyeLookDownRight 
eyeLookIn_L eyeLookInLeft 
eyeLookIn_R eyeLookInRight 
eyeLookOut_L eyeLookOutLeft 
eyeLookOut_R eyeLookOutRight 
eyeLookUp_L eyeLookUpLeft 
eyeLookUp_R eyeLookUpRight 
eyeSquint_L eyeSquintLeft 
eyeSquint_R eyeSquintRight 
eyeWide_L eyeWideLeft 
eyeWide_R eyeWideRight 

# hapihapi

jawForward jawForward 
jawLeft jawLeft 
jawOpen jawOpen 
jawRight jawRight 

mouthClose mouthClose 
mouthDimple_L mouthDimpleLeft 
mouthDimple_R mouthDimpleRight 
mouthFrown_L mouthFrownLeft 
mouthFrown_R mouthFrownRight 
mouthFunnel mouthFunnel 
mouthLeft mouthLeft 
mouthLowerDown_L mouthLowerDownLeft 
mouthLowerDown_R mouthLowerDownRight 
mouthPress_L mouthPressLeft 
mouthPress_R mouthPressRight 
mouthPucker mouthPucker 
mouthRight mouthRight 
mouthRollLower mouthRollLower 
mouthRollUpper mouthRollUpper 
mouthShrugLower mouthShrugLower 
mouthShrugUpper mouthShrugUpper 
mouthSmile_L mouthSmileLeft 
mouthSmile_R mouthSmileRight 
mouthStretch_L mouthStretchLeft 
mouthStretch_R mouthStretchRight 
mouthUpperUp_L mouthUpperUpLeft
mouthUpperUp_R mouthUpperUpRight

noseSneer_L noseSneerLeft
noseSneer_R noseSneerRight

tongueOut tongueOut
```

{{< /details >}}

## 書式

以下、設定可能な項目についてグループごとに解説します。

### リップシンク

音声からの自動リップシンクで使用する口形モーフを指定します。日本語の「あ」「い」「う」「お」に対応して動かすモーフの名称をそれぞれ `LIP_A`, `LIP_I`, `LIP_U`, `LIP_O` で指定します。

```text
LIP_A あ
LIP_I い
LIP_U う
LIP_O お
```

自動リップシンク実行中は常に 0 にするモーフのリストを `NOLIP` で指定できます。これは、自動リップシンクが対話アクションや自律モーションと重なるときに、上記の4つのモーフ以外のモーフの動きが重なって表現がおかしくなるのを防ぐための機能です。一般的には、モデルに定義されている上記４つのモーフ以外の口の形に関わるモーフを全て指定します。

```text
NOLIP え,おお~,ワ,∧,はんっ！,えー,にやり,にっこり,口締め,結び,む,ああ,いい,にたり,叫び,あーれー,口わらい,mouth_a_geo_C,mouth_i_geo_C,mouth_u_geo_C,mouth_e_geo_C,mouth_o_geo_C,mouth_oh_geo_C,mouth_smile_geo_C,mouth_surprise_geo
```

### 対話アクション

外部APIによる対話アクション再生メッセージ (**__AV_ACTION,番号**) の番号に対応するモーションファイルを指定します。以下のように、`ACT` に続けて1桁～2桁の番号と、対応するモーションファイルへのパスを記述します。相対パスは、カレントからの相対ではなく、この .shapemap ファイルが置かれているフォルダからの相対として解釈されることに注意してください。

```text
ACT0  motion/00_normal.vmd
ACT1  motion/01_happy.vmd
...
ACT38 motion/38_Ashamed.vmd
```

### ヘッドトラッキング

ヘッドトラッキングメッセージ (**__AV_TRACK**) の制御対象となるボーン名を指定します。以下の7つを必ずすべて指定してください。

ボーン名はカンマで区切って複数指定可能です。複数指定した場合、左から順にモデル上を探し、最初に見つかったものを使います。

```text
TRACK_HEAD 頭
TRACK_NECK 首
TRACK_LEFTEYE 左目
TRACK_RIGHTEYE 右目
TRACK_BOTHEYE 両目
TRACK_BODY 上半身2,上半身２,上半身1,上半身
TRACK_CENTER センター
```

また、トラッキングにおいて目の回転量が大きすぎる、または小さすぎる場合は以下の `EYE_ROTATION_COEF` で調整してください。値が大きいほど大きく回転し、小さいほど小さく回転します。

```text
EYE_ROTATION_COEF 0.4
```

### 個別ボーン制御

個別ボーン制御メッセージ (**__AV_EXBONE**) への対応を記述します。このメッセージで指定する制御名 **name** と、実際に操作するモデル上のボーン名の対応を定義します。以下のように `EXBONE_name ボーン名` の書式を使います。

```text
EXBONE_name ボーン名
```

例えば、モデルの右腕と左腕を制御する場合は、.shapemap で

```text
EXBONE_RUarm 右腕
EXBONE_LUarm 左腕
```

のようにマッピングを定義することで、外部APIからの以下のようなメッセージに対して、それぞれの指定動作を上記で定義したボーンに適用させることができます。

{{<message>}}
__AV_EXBONE,RUarm,0,0,0,0,0.8,0,LUarm,0,0,0,0,0.8,0
{{</message>}}

name とボーン名の対応は1対1で、重複や多重化はできません。複数のボーンを制御する場合、それぞれ異なる name を付けてください。

### 個別モーフ制御

個別モーフ制御メッセージ (**__AV_EXMORPH**) への対応を記述します。このメッセージで指定する制御名 **name** と、実際に操作するモデル上のモーフ名の対応を定義します。以下のように `EXMORPH_name モーフ名` で記述します。

```text
EXMORPH_name モーフ名
```

指定においては、上記のようにモーフ名のみのほかに、AUと同様にしきい値指定や係数指定も可能です。

name とモーフ名の対応は1対1で、重複や多重化はできません。複数のモーフを制御したい場合、それぞれ異なる name を付けてください。

### フェイシャルトラッキング: Action Unit

AU (Action Unit) を用いたフェイシャルトラッキング (**__AV_AU**) において、Action Unit の値に対してどのようにモーフを動かすかを定義します。受信する Action Unit に対して、モーフへのマッピング設定を１つずつ記述します。

指定は `AU` に続いて番号と、対応するモーフ、制御方法を1行づつ記述します。以下の例では、AU番号6 (cheek raiser) を笑った目のモーフである「笑い」モーフへ、AU番号1 (inner brow raiser) を眉を挙げるモーフ「上」へ、AU番号4 (brow lowerer) を、眉を困った形にする「困る」モーフへマッピングしています。

```text
AU6 笑い >0.7
AU1 上 0.5
AU4 困る
```

- `AU番号 モーフ名` のみの場合、AUの番号の値を、そのモーフの値としてそのままマッピング
- `AU番号 モーフ名 >閾値` の場合、もし値が閾値未満ならそのモーフの値を 0.0 にし、閾値以上だったなら 1.0 にする。
- `AU番号 モーフ名 係数` の場合、AUの値に係数をかけたものをそのモーフの値として割り当てる。係数はゼロ以上、負はNGとする。

AU番号とモーフ名は相互に複数マッピングが可能です。

- ある AU 番号に対して、モーフのマッピングを複数回記述した場合、そのAUの値が定義したすべてのモーフへ一斉に適用されます。1つの AU 値で複数のモーフを動かしたい場合はこれを使ってください。
- 逆に、複数の異なるAUが同一のモーフへ複数回マッピングされた場合、それらのすべての値が加算された値がモーフへ適用されます。

AUでの制御において過度な加算を抑制する設定を `MORPH_TUNE` で行えます。例えば、「まばたき」と「笑い」はどちらも目の開閉に関するモーフですが、これらを両方とも 1.0 にすると、過度に目をつぶったおかしな表現になってしまいます。この場合、下記のように .shapemap に記述することで、それら複数のモーフの値の制御後の合計が 1.0 を越えないよう制約することができます。

```text
MORPH_TUNE 笑い まばたき
```

`MORPH_TUNE` は繰り返し指定できます。最大30個です。また1つあたりに指定できるモーフの数は 10 種までです。

### フェイシャルトラッキング: ARKit Shapes

上記のどの記述にも当てはまらない行は、フェイシャルトラッキングメッセージ **__AV_ARKIT** で使われるシェイプ名とモデルのモーフ名との対応として解釈されます。**__AV_ARKIT** で指定されているシェイプがここでマッピングを定義されていない場合、そのシェイプ名での操作は無視されます。

CG-CA のモデルでは、[Apple ARKit](https://developer.apple.com/documentation/arkit/) のフェイストラッキング結果として得られる [blendShape](https://developer.apple.com/documentation/arkit/arfaceanchor/2928251-blendshapes) を想定して、ARKit の52個の blendShape すべてに1対1で対応するモーフをあらかじめ仕込んであります。

上記より、CG-CAに付属の .shapemap には、AR Kit に対応した全シェイプ名とそれに対応するモデルのモーフ名が、既に記述されています。なお付属の .shapemap で記述されているシェイプ名は、ARKit 上で定義されている名前そのものではなく、ARKit を用いたフェイシャルキャプチャ情報を送信するアプリ `iFacialMoCap` が出力する名前に合わせて記述されています。

対応するモーフについては1対1対応のほか、AUと同様にしきい値指定や係数指定も可能です。
