---
title: 外部API
slug: api
---

{{< hint ms >}}
！本ページの以下の内容は、すべてムーンショット版のみの内容です。
{{< /hint >}}

# 外部API

外部プログラムからソケット通信を介して MMDAgent-EX を直接制御できます。[標準的なメッセージ送受信による制御](../remote-control/)に加えて、MS版ではCGエージェントをアバターとして利用するための外部APIが追加定義されており、利用することができます。以下、使い方を解説します。

## MMDAgent-EX へ接続する

外部のプログラムから外部APIを使う場合、外部プログラムから MMDAgent-EX へソケットで接続します。
ソケット接続の方法については、[ソケット接続で制御する](../remote-control/)のページを見てください。

{{< hint warning >}}
WebSocket 接続を使ってください。TCP/IP 接続では一部の機能が未対応です。
{{< /hint >}}

## 送信仕様とコマンドメッセージ一覧

外部プログラムからメッセージを MMDAgent-EX のソケットへ送信することで制御します。送信可能なメッセージの一覧と、送信の仕方については以下のとおりです。

- メッセージの末尾に必ず "\n" をつけて送信してください。
- 1回の送信で複数のメッセージをまとめて送る場合は "メッセージ1\nメッセージ2\n" のように各メッセージの末尾に "\n" をつけてください。
- WebSocket の送信モードが指定できる場合は、バイナリモードを使ってください。
- メッセージで行った各種設定はソケット切断時にリセットされます。次回の接続には引き継がれません。
- これら以外のメッセージが送られた場合、MMDAgent-EX はそれらを外部APIではなく通常のメッセージとして受け取りキューへ投げ込みます。

```text
__AV_SETMODEL,model_alias_name
__AV_AUTOCALIBRATE,{true|false}
__AV_AUTORETRACT,{true|false}
__AV_START
__AV_END
__AV_RECALIBRATE
__AV_ACTION,idx
__AVCONF_ALLOWFARCLOSEMOVE,{true|false}
__AV_TRACK,x,y,z,rx,ry,rz,eyeLrx,eyeLry,eyeLrz,eyeRrx,eyeRry,eyeRrz,flag
__AV_ARKIT,shape=rate,shape=rate,…
__AV_AU,num=rate,num=rate,…
__AV_EXBONE,name,x,y,z,rx,ry,rz,name,x,y,z,rx,ry,rz,…
__AV_EXBONEQ,name,x,y,z,rx,ry,rz,rw,name,x,y,z,rx,ry,rz,rw,…
__AV_EXMORPH,name=rate,name=rate,…
__AVCONF_DISABLEAUTOLIP,{NO|ARKIT|AU|ARKIT+AU|ALWAYS}
SNDSTRM
SNDFILE
SNDBRKS
SNDxxxx(body)
AVATAR_LOGSAVE_START|logfile.txt
AVATAR_LOGSAVE_STOP
AVATAR_EVENT_IDLE|START
AVATAR_EVENT_IDLE|STOP
```

## トラッキングにおける基礎仕様

トラッキングメッセージ（**__AV_TRACK**, **__AV_ARKIT**, **__AV_AU**, **__AV_EXBONE**, **__AV_EXMORPH**）で表情や動きのトラッキングを行う際の、各メッセージ共通の基礎仕様です。

- **__AV_SETMODEL** でセットしたモデルに対して制御を実施します。
- **__AV_START** で制御を開始し、**__AV_END** で制御を終了します。終了中のトラッキングメッセージは無視されます。
- 制御中は、トラッキングによる動作が自律動作を上書きします。ただし、上書きするのはトラッキングで制御対象となっているボーン・モーフのみで、対象でないものはトラッキング中も自律による動作が継続します。
- トラッキングメッセージは単発でも連続でも送れます。連続の場合、最大で 60 fps程度の頻度で送信されることを想定しています。
- デフォルトでは自動補正が有効になっており、最初の10回の **__AV_TRACK** を使って顔の向きの正面を補正します。このため、自動補正有効時は最初の10回の **__AV_TRACK** は反映されず、以降はこの10回の平均が顔の正面として補正されます。この自動補正のっ有効・無効は **__AV_AUTOCALIBRATE** で変更できます。
- デフォルトでは自動退避（オートリトラクト）が有効になっており、トラッキングメッセージがしばらく（デフォルトでは1秒）送られなければトラッキング制御が一時停止して自律制御に戻ります（送信を再開すれば戻ります）。自動退避を無効化すれば、**__AV_END** を送るまでトラッキング状態を常に維持するようになります。自動退避の有効・無効は **__AV_AUTORETRACT** で変更できます。
- MMDAgent-EX側では動作のスムージングが行われます。このため、指定した状態になるまで多少ディレイがあります。
- 外部プログラムからのメッセージが 15秒間 途絶えたとき、MMDAgent-EX は **AVATAR_EVENT_IDLE|START** メッセージを発行します。再びメッセージが外部プログラムから届いたとき、 **AVATAR_EVENT_IDLE|STOP** を発行します。

## 各メッセージ解説

### 開始・終了・設定・ログ

#### AV_SETMODEL,エイリアス名

外部APIによる操作の対象とするモデルを指定します。外部APIの全てのコマンドは、このメッセージで指定されたモデルに適用されます。接続後、トラッキングを開始する前に必ず行ってください。

{{<message>}}
__AV_SETMODEL,0
{{</message>}}

- モデルはエイリアス名を指定します。
- 指定されたエイリアス名のモデルがない場合、このメッセージは無視されます。
- トラッキング制御中でも対象モデルを随時変更することが可能です。
- 同時に操作対象にできるモデルは1体のみです。

#### __AV_AUTOCALIBRATE

顔の向き・位置の自動補正機能の ON/OFF を設定します。

顔の向きの自動補正機能は、フェイストラッキングにおいてWebカメラと操作者の顔の向きを補正するための機能です。この機能が ON であるとき、開始直後に送信される **__AV_TRACK** メッセージの最初の10回分を適用せずに保存し、その平均を顔の正位置として、以降の **__AV_TRACK** メッセージで送られるパラメータを補正して用います。OFFにした場合、自動補正機能は解除され、**__AV_TRACK** で送られた値がそのまま適用されることになります。

有効な場合、最初の10回の **__AV_TRACK** メッセージは補正のためのパラメータ推定に用いられ、アバターには適用されないことに注意してください。

以下のメッセージでON/OFFを変更できます。

{{<message>}}
__AV_AUTOCALIBRATE,true
{{</message>}}

自動補正機能を ON にする。

{{<message>}}
__AV_AUTOCALIBRATE,false
{{</message>}}

自動補正機能を OFF にする。

#### __AV_AUTORETRACT

オートリトラクト機能の ON/OFF を設定します。

オートリトラクト機能は、運用において不意にCGアバターがフリーズするのを自動回避するための機能です。この機能が ON であるとき、トラッキング制御中にしばらく（デフォルトでは1秒）トラッキングメッセージが送られないときに、MMDAgent-EXは一時的にトラッキング制御を止めて自律制御に戻ります。その後、何らかの新たなトラッキングメッセージが送信されたら、トラッキング状態へ自動復帰します。OFFにした場合、この自動回避は機能せず、トラッキング制御中は常に最後に指示されたトラッキング姿勢が維持されます。

トラッキングメッセージを連続して送り続ける運用の場合、この機能を ON にしておくことで通信エラーやトラッキングミスの際にアバターがフリーズするのを避けることができます。逆に、姿勢制御を離散的に行う運用では、ON だと姿勢を指示した1秒後に制御が切れてしまうので、その場合は OFF することで最後の姿勢を維持できます。

デフォルトではオートリトラクト機能はONで、自動回避までの時間は1秒です。以下のメッセージでON/OFFや自動回避までの待ち時間を変更できます。

{{<message>}}
__AV_AUTORETRACT,true
{{</message>}}

オートリトラクト機能を ON にする。

{{<message>}}
__AV_AUTORETRACT,数字
{{</message>}}

オートリトラクト機能を ON にし、かつ、自動回避までの待ち時間を指定した秒に設定する。値は > 0 であること。デフォルトは 1.0 である。機能を OFF にしたい場合、0 ではなく false を指定すること。

{{<message>}}
__AV_AUTORETRACT,false
{{</message>}}

オートリトラクト機能を OFF にする。

#### __AV_START

トラッキング制御を開始します。このメッセージ以降、外部APIモジュールはCGアバターの身体動作の一部を奪い、トラッキングメッセージ（**__AV_TRACK**, **__AV_ARKIT**, **__AV_AU**, **__AV_EXBONE**, **__AV_EXMORPH**）によるアバター操作を開始します。自律動作と重なる部分はトラッキングが優先されます。

{{<message>}}
__AV_START
{{</message>}}

- 受信時、MMDAgent-EX はイベントメッセージ **AVATAR|START** を発行し、KeyValue値 `Avatar_mode` を `1.0` にセットします。
- 以降、**__AV_TRACK**, **__AV_ARKIT**, **__AV_AU**, **__AV_EXBONE**, **__AV_EXMORPH** が有効となります。
- トラッキングの操作対象のモデルは **__AV_SETMODEL** で事前に指定してください。

#### __AV_END

トラッキング制御を終了します。外部APIによる身体動作制御はOFFになり、自律動作に戻ります。OFFになっている間に送られたトラッキングメッセージ（**__AV_TRACK**, **__AV_ARKIT**, **__AV_AU**, **__AV_EXBONE**, **__AV_EXMORPH**）は無視されます。

{{<message>}}
__AV_END
{{</message>}}

- 受信時、MMDAgent-EX はイベントメッセージ **AVATAR|END** を発行し、同時に KeyValue値 `Avatar_mode` の 値を `0.0` にセットします。

#### AVATAR_LOGSAVE_START, AVATAR_LOGSAVE_STOP

外部APIからのメッセージログを MMDAgent-EX 側でファイルに保存させます。**AVATAR_LOGSAVE_START** で指定ファイルへの保存を開始し、**AVATAR_LOGSAVE_STOP**で終了します。

{{<message>}}
AVATAR_LOGSAVE_START|logfile.txt
AVATAR_LOGSAVE_STOP
{{</message>}}

#### __AV_RECALIBRATE

ヘッドトラッキングにおける顔の向きの補正を実行します。MMDAgent-EX は **__AV_START** を受け取った直後に顔の向きの補正を実行しますが、このメッセージは、そのキャリブレーションの再実行を通知するものです。

{{<message>}}
__AV_RECALIBRATE
{{</message>}}

### 対話アクション再生

#### __AV_ACTION,アクション番号

指定した番号の対話アクションを再生します。番号として 0 以上の整数値を指定できます。トラッキング制御中でなくても動作します。

{{<message>}}
__AV_ACTION,3
{{</message>}}

- 指定した番号に対応するモーションが[部分モーション](../motion-layer)として再生されます。
- 開始されたモーションは、そのモーションファイルで定義された時間だけ再生を行ったあとに消えます（ループしません）。
- **__AV_ACTION** によるモーション再生中にさらに **__AV_ACTION** を送った場合、新しいモーションが古いモーションを即時に上書きして開始されます。
- トラッキング中に対話アクション再生を行った場合、制御が重なるボーン・モーフについてはトラッキング側が優先されます。

指定番号に対するモーションはモデルの[.shapemap ファイル](../shapemap)で定義されています。
shapemap ファイルが存在しない、あるいは指定された番号のアクションが未定義の場合、**__AV_ACTION** メッセージは無視されます。CG-CA モデルでは、以下の 39 種のアクションがデフォルトで定義されています。（0 のノーマルはデフォルト状態に戻すための指定です）

```text
アクション番号 内容
 0  ノーマル/ normal
 1  喜び/ joy, happy
 2  笑い/ laugh, amusing
 3  笑顔/ smile
 4  微笑/ little smile, agreement
 5  固い笑顔/ graceful smile
 6  照れ笑い/ embarassed smile
 7  困り笑い/ annoyed smile
 8  驚き・ショック/ surprise
 9  意外/ unexpected
10  感動/ impressed, excited
11  感心/ admired
12  期待・興味/ expectant, interested
13  納得・理解/ convinced
14  きりっと/ crisp, prepared
15  キメ顔/ proud, confident
16  考え中/ thinking
17  とんでもない/ no thank you (with smile)
18  同情・気遣い/ compassion, caring
19  ドヤ顔/ triumphant
20  困った/ in trouble, annoyed
21  軽い拒否・叱り/ no, accuse, disgust
22  謝り/ apology
23  緊張/ stressed
24  恥ずかしい/ embarassing
25  ジト目/ sharp eyes, suspicion
26  くやしい/ mortifying
27  煽り/ provoking
28  眠い/ sleepy
29  焦り・怖ろしい/ impatience, fear, terrible
30  呆然・唖然/ stunned, devastated
31  落胆/ disappointed
32  イライラ/ irritated, frustrated
33  怒り/ anger, furious
34  哀しみ/ sad
35  怖い/ afraid
36  不安・心のざわつき/ anxious
37  感傷的/ sentimental
38  恥じ入る/ ashamed
```

新たなアクション番号と対応モーションの定義を .shapemapファイルに追記できます。番号は 00 から 99 まで使えます。例えば、新たに 40番にお辞儀モーション (ojigi.vmd) を追加する場合、以下のように .shapemap に書きます。ここで .vmdファイルのパスはカレントディレクトリではなくモデルファイル(.pmd)からの相対パスで指定することに注意してください。

```text
ACT40 somewhere/ojigi.vmd
```

以下のようにその番号を指定することで再生させることができます。

{{<message>}}
__AV_ACTION,40
{{</message>}}

### ヘッドトラッキング

#### __AV_TRACK,x,y,z,rx,ry,rz,eyeLrx,eyeLry,eyeLrz,eyeRrx,eyeRry,eyeRrz,flag

アバターの頭部の目標とする姿勢情報を送信します。このメッセージが送信されるたび、MMDAgent-EXは対象モデルの頭部と上半身のボーンの姿勢をそれに合わせてセットします。連続で送信することでリアルタイムのヘッドトラッキングが行えます。

- **x,y,z**: 頭部の移動量（mm）
- **rx,ry,rz**: 頭部の回転量：x軸,y軸,z軸 (radian)
- **eyeLrx,eyeLry,eyeLrz**: 左目の回転量 (radian)
- **eyeRrx,eyeRry,eyeRrz**: 右目の回転量 (radian)
- **flag** 目の回転量のグローバル(1), ローカル(0)を指定

移動量の単位はミリメートルです。

頭部の回転量は、x軸、y軸、z軸のローカル回転量をラジアンで表します。回転表現は全て左手系 (left-handed) です。

目の回転量は、x軸、y軸、z軸の回転量をラジアンで与えます。ローカル回転量（頭の正面に対する相対回転量）で与える場合は **flag** を 0 に、グローバル回転量（世界座標に対する絶対回転量）で与える場合は **flag** を 1 に指定します。OpenFace が出力するトラッキング情報を使う場合、OpenFaceはグローバル回転量を出力するので 1 を、Apple ARKit のヘッドトラッキング情報を使う場合、ARKit はローカル回転量を出すので 0 を指定してください。

また、特別な処理として、**flag** が 1 の場合、MMDAgent-EXは右目と左目の回転量をそのままそれぞれの目に適用せず、代わりにその平均の回転量を「両目」ボーンに適用するようになっています。この措置は OpenFace において視線検出のブレによって左右の目の視線が揃わない状態を避けるための実装です。

接続直後の情報を使って、顔の位置と向きの補正が MMDAgent-EX 側で行われます。この補正は **__AV_START** を送った直後に送信されるトラッキングパラメータ10回分を使って行われます。操作中にずれた場合は **__AV_RECALIBRATE** を送信することで MMDAgent-EX へ再補正を要求できます。

CGらしい強調された動作を行うため、MMDAgent-EXは送信された頭部動作パラメータに基づいて頭部以外の複数のボーンを制御します。受け取ったメッセージに対してMMDAgent-EXが実際にどのボーンを動かすかは、モデル側の[.shapemap](../shapemap) ファイルにおいて `TRACK_HEAD`, `TRACK_NECK`, `TRACK_LEFTEYE`, `TRACK_RIGHTEYE`, `TRACK_BOTHEYE`, `TRACK_BODY`, `TRACK_CENTER` で指定します。CG-CA ではデフォルトで以下の設定がされています。ほとんどの入手可能な MMD モデルではこれらのボーンは共通で実装されているので、この設定をそのまま流用して問題ありません。
以下の `TRACK_BODY` のように複数のボーン名を指定した場合、左から順にモデル上でボーンの有無が調べられ、最初に見つかったボーンが採用されます（一般のMMDモデルでは上半身を司るボーン名に表記の揺れがあるため、このような書式が許されるようになっています。）

```text
TRACK_HEAD 頭
TRACK_NECK 首
TRACK_LEFTEYE 左目
TRACK_RIGHTEYE 右目
TRACK_BOTHEYE 両目
TRACK_BODY 上半身2,上半身２,上半身1,上半身
TRACK_CENTER センター
```

目の適切な回転量は使用するモデルによって異なります。目が動かなさすぎる、あるいは動きすぎる場合は .shapemap 内の以下の係数を調整してください。

```text
EYE_ROTATION_COEF 0.4
```

受け取った頭部動作パラメータに対して、各ボーンを実際にどの程度動かすかは、予め内部で定義されていますが、.mdf で個別に変更・調整することが可能です。以下は設定項目とデフォルト値です。もっと大きく動かしたい、あるいは動きを抑制したい等あれば、これらを参考に値を変更してみてください。

{{<mdf>}}
# 頭部回転に対する「上半身2」ボーンの回転係数
Plugin_Remote_RotationRateBody=0.5
# 頭部回転に対する「首」ボーンの回転係数
Plugin_Remote_RotationRateNeck=0.5
# 頭部回転に対する「頭」ボーンの回転係数
Plugin_Remote_RotationRateHead=0.6
# 頭部回転から上下移動への変換スケール
Plugin_Remote_MoveRateUpDown=3.0
# 頭部回転から左右移動への変換スケール
Plugin_Remote_MoveRateSlide=0.7
{{</mdf>}}

デフォルトでは操作者の左右がそのままCGアバターの左右として伝達されます。左右の動きを反転したい場合は、.mdf に以下の設定を記述してください。

{{<mdf>}}
# 左右反転
Plugin_Remote_EnableMirrorMode=true
{{</mdf>}}

#### AVCONF_ALLOWFARCLOSEMOVE,値

操作者の前後の動きをトレースするかどうかを指定します。 `true` なら前後の動きもアバターへトレースし、それ以外なら操作者の前後の動きは無視します。デフォルトは `true` です。

{{<message>}}
__AVCONF_ALLOWFARCLOSEMOVE,true
{{</message>}}

### フェイシャルトラッキング：Apple AR Kit

#### __AV_ARKIT,name=rate,name=rate,...

シェイプと設定値 ([0.0-1.0]) の集合を送ります。MMDAgent-EX は、送られてきた情報に従ってアバターのモーフを制御します。連続で送信することでリアルタイムのフェイシャルトラッキングが行えます。

MMDAgent-EX は送信されたシェイプ情報をモデルのモーフに適用します。**__AV_ARKIT** で送信されるシェイプ名と操作対象のCGモデルのモーフの対応は、モデルの [.shapemap](../shapemap) に予め記述されている必要があります。.shapemap でマッピングが定義されていないシェイプ名は無視されます。

例として、モデルのまばたきを制御する簡単な例を示します。**__AV_ARKIT** で使用するシェイプ名として `blink` を使用することにしましょう。一方、操作対象の CG モデルではまばたきのモーフは「まばたき」という名前で定義されています。このため、.shapemap ファイルでは以下のようにシェイプ名とモーフ名の対応を記述しておきます。

```text
blink まばたき
```

**__AV_ARKIT** では以下のようにシェイプ名 `blink` とその設定値を送ることでまばたきを制御できます。

{{<message>}}
__AV_ARKIT,blink=1.0
{{</message>}}

上記は簡単な例ですが、実際にフェイシャルトラッキングを行う場合は、顔の各部のフェイシャル情報をもとにCGモデルの顔の様々なパーツを動かす必要があります。CG-CAは [Apple ARKit] (https://developer.apple.com/documentation/arkit/) のフェイストラッキング結果として得られる [blendShape](https://developer.apple.com/documentation/arkit/arfaceanchor/2928251-blendshapes) を想定し、ARKit の52個の blendShape すべてに1対1で対応するモーフをあらかじめ仕込んであります。

{{< details "CG-CA に付属の .shapemap で定義されているマッピングの詳細" close>}}
```
# iFacialMocapシェイプ名 モデル上のモーフ名
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

Action Unit 形式のトラッキング（**__AV_AU**）と併用すると動作が重なるため、どちらかを使うようにしてください。

### フェイシャルトラッキング：Action Unit (AU)

#### __AV_AU,num=rate,num=rate,...

[Action Unit](https://en.wikipedia.org/wiki/Facial_Action_Coding_System) の番号（1～46）とその強度 [0..1] の情報を送信し、それに従って表情を制御します。MMDAgent-EX は、送られてきた Action Unit 情報に基づいてアバターのモーフ値を制御します。連続で送信することでリアルタイムのフェイシャルトラッキングが行えます。

`num=rate` の部分には、Action Unit の番号（1から46）とその強度を指定します。強度は 0 以上 1 以下であり、1より大きい値は 1 として扱われます。カンマで区切って複数の Action Unit の値を指定できますので、参照する Action Unit の値を列挙して送信してください。

Action Unit は表情筋の動きをエンコードするものであり、その値はモデルの表情モーフとは一対一に対応しません。__AV_AU で送られる各 Action Unit の値に対して、実際にモデルのどのモーフをどのようにセットするかを、shapemap ファイルで定義する必要があります。以下のように、受信する Action Unit に対して、モーフへのマッピング設定を１つずつ記述します。この例では、AU番号6 (cheek raiser) を笑った目のモーフである「笑い」モーフへ、AU番号1 (inner brow raiser) を眉を挙げるモーフ「上」へ、AU番号4 (brow lowerer) を、眉を困った形にする「困る」モーフへマッピングしています。

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

Apple ARKit 形式によるトラッキング（**__AV_ARKIT**）と併用すると動作が重なるため、どちらかを使うようにしてください。

### ボーン個別制御

#### __AV_EXBONE, __AV_EXBONEQ

任意のボーンを外部から制御します。これらによるボーン制御では、自動補正は行われません。

**__AV_EXBONE** を使ってボーンの回転量を x軸, y軸, z軸の回転量（3要素）で与えます。あるいは **__AV_EXBONEQ** を使えば回転量をクオータニオン（４要素）で与えることができます。

{{<message>}}
 __AV_EXBONE,name,x,y,z,rx,ry,rz,rw,name,x,y,z,rx,ry,rz,rw,...**
{{</message>}}

- **name**: 制御名
- **x,y,z**: 移動量（mm）
- **rx,ry,rz**: x軸, y軸, z軸回転量 (radian)

{{<message>}}
 __AV_EXBONEQ,name,x,y,z,rx,ry,rz,rw,name,x,y,z,rx,ry,rz,rw,...**
{{</message>}}

- **name**: 制御名
- **x,y,z**: 移動量（mm）
- **rx,ry,rz,rw**: 回転量のクォータニオン (radian)

このメッセージで指定する制御名 **name** と、実際に操作するモデル上のボーン名の対応は、shapemap 内で定義します。この定義には、以下のように "EXBONE_name ボーン名" の書式を使います。

{{<message>}}
EXBONE_name ボーン名
{{</message>}}

例えば、モデルの右腕と左腕を制御する場合は、.shapemap で

```text
EXBONE_RUarm 右腕
EXBONE_LUarm 左腕
```

のようにマッピングを定義し、捜査の際は **__AV_EXBONE** メッセージで以下のように送信します。

{{<message>}}
__AV_EXBONE,RUarm,0,0,0,0,0.8,0,LUarm,0,0,0,0,0.8,0
{{</message>}}

name とボーン名の対応は1対1で、重複や多重化はできません。複数のボーンを制御する場合、それぞれ異なる name を付けて送信してください。

原理上は任意のボーンに対して任意の移動量と回転量を指定できますが、ボーンの種類によっては挙動が変わることがあります。特に「IKボーン」（足回り）や「物理演算ボーン」（揺れもの）はMMDAgent-EX側で演算によって自動制御されるため、本メッセージで指定しても指定通りの動作にならないことがある点に注意してください。

### モーフ個別制御

#### __AV_EXMORPH,name=rate,name=rate,...

任意のモーフを外部から制御します。

- **name**: 制御名
- **rate**: モーフ値（0.0～1.0）

このメッセージで指定する制御名 **name** と、実際に操作するモデル上のモーフ名の対応は shapemap 内で定義します。以下のように "EXMORPH_name モーフ名" で記述します。

{{<message>}}
EXMORPH_name モーフ名
{{</message>}}

name とモーフ名の対応は1対1で、重複や多重化はできません。複数のモーフを制御したい場合、それぞれ異なる name を付けて送信してください。

### 音声伝送

音声波形データをソケット経由で流し込み、リップシンク付きで再生させます。トラッキング制御中でなくても動作します。音声波形データは 16kHz, 16bit, mono のみ扱えます。

音声伝送のモードとして、ファイルモードとストリーミングモードの2種類のモードがあります。

ファイルモードでは、音声データは上記のとおり短いチャンクに区切って送信し（全体を1つの大きなチャンクとして一度に送信することも可能）、最後に発話終端信号を送ります。MMDAgent-EX は、1つ目のチャンクの受信終了と同時に音声の再生を開始して、送信された音声データを出力し、発話終端に達したらセッションの終了とリップシンクの口閉じを行います。

ストリーミングモードでは、音声送信は短チャンクごとに行う必要があります。明示的な発話終端は与えられないため、MMDAgent-EX 側で無音部分の検出から発話区間の区切りが行われます。

デフォルトはストリーミングモードです。ファイルモードにするには、まず先に `SNDFILE\n` を送信してモードを切り替えてから、ファイルの中身を逐次 `SND` で転送します。その際、ファイルの終端まで送信し終えたら `SNDBRKS\n` を送って入力終了をMMDAgent-EXに伝えます。ストリーミングモードに戻すには `SNDSTRM\n` を送信します。

#### SNDxxxx(body)

音声データを送信します。`xxxx` は4桁の数字で、そのあとに続くデータ本体のバイト長を10進数4桁で表します。長い音声を一括で送信すると遅延が発生するので、なるべく40ms分 (1280 Bytes) ぐらいの短いセグメントで区切って逐次送信してください。このメッセージのみ、末尾に `\n` は不要です。

以下はオーディオセグメントを送信する Python コードの例です。

```python
async def send_audio(chunk_data, chunk_bytes):
    header = ("SND" + f"{chunk_bytes:04}").encode('ascii')
    payload = bytearray()
    payload = header + chunk_data
    await websocket.send(payload)
```

#### SNDFILE

音声伝送モードをファイルモードにします。

- MMDAgent-EX 側で無音検出・発話区間区切りは行われません。
- 1発話分の音声伝送が終了したら `SNDBRKS` を送ってください

{{<message>}}
SNDFILE
{{</message>}}

#### SNDBRKS

ファイルモード時に１発話の終了を伝達します。

{{<message>}}
SNDBRKS
{{</message>}}

#### SNDSTRM

音声伝送モードをストリーミングモードにします。

- MMDAgent-EX 側で無音検出・発話区間区切りが行われます。

{{<message>}}
SNDSTRM
{{</message>}}

#### __AVCONF_DISABLEAUTOLIP,{NO|ARKIT|AU|ARKIT+AU|ALWAYS}

フェイシャルトラッキングと音声伝送を併用する際に、自動リップシンクによって算出される口形と、フェイシャルトラッキングによって指定される口形が、競合するケースがあります。**__AVCONF_DISABLEAUTOLIP** は、この競合時における音声からの自動リップシンクの扱いを設定するメッセージです。

以下のいずれかを指定します。指定しない場合のデフォルトは `NO` です。

- **NO**: 常に自動リップシンクを行います。競合する場合、リップシンクとフェイシャルトラッキングの両者の口形が加算されて表示されます。
- **ARKIT**: **__AV_ARKIT** メッセージを受信している間、音声による自動リップシンクをストップします。
- **AU**: **__AV_AU** メッセージを受信している間、音声により自動リップシンクをストップします
- **ARKIT+AU**: **__AV_ARKIT** あるいは **__AV_AU** のどちらかのメッセージを受信している間、自動リップシンクをストップします。
- **ALWAYS**: 自動リップシンクの機能を OFF にします。
