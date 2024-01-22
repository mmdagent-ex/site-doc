---
title: 外部API
slug: api
---

{{< hint ms >}}
！本ページの以下の内容は、すべてムーンショット版のみの内容です。
{{< /hint >}}

# 外部API

外部プログラムから WebSocket または TCP/IP 接続を介して MMDAgent-EX を直接制御できます。[標準的なメッセージ送受信による制御](../remote-control/)に加えて、MS版ではアバターとしての利用のための外部APIが定義されており、利用することができます。

## 仕様一覧

- メッセージは1つごとに改行 "\n" で区切って送信
- WebSocket の場合、ソケットの送信モードとしてテキストモードとバイナリモードのどちらでも動作する。ただし `SNDで始まるコマンド` では音声波形データをテキストエンコードせずバイナリのまま送るので、バイナリモードを使うこと。
- 接続が切断された場合これらのパラメータはリセットされる。次回の接続には引き継がれない。

```text
__AV_START
　外部操作開始フラグ。これを受け取った MMDAgent-EX は、以後 __AV_END が来るまで受信した情報に従ってモデルの操作を行う。

__AV_END
　外部操作終了フラグ。これを受け取った MMDAgent-EX は、以後 __AV_START が来るまで外部操作を中断する。

__AV_SETMODEL,モデルエイリアス
　外部操作の対象とするモデルの名前。これを受け取った MMDAgent-EX は、指定された名前で動作しているモデルを以降の操作対象とする。

__AVCONF_DISABLEAUTOLIP,{NO|ARKIT|AU|ARKIT+AU|ALWAYS}
　音声伝送時の伝送音声からの自動リップシンクを行わない場面の指定。デフォルトは `NO` 、つまりリップシンクを常に行う。

__AV_ACTION,idx
　指定した対話アクションを再生する。アクションは番号(1から)で指定する。モデルでは shapemap で指定した対応モーションが再生される。

__AV_RECALIBRATE
　顔の向きを再キャリブレーションする。__AV_START 時に、その時点の遠隔操作者の顔の向きを正面として向きのキャリブレーションが行われる。このコマンドはそのキャリブレーションのみを再実行する。

__AVCONF_ALLOWFARCLOSEMOVE,値
　体の前後の動きをトレースするかどうかのフラグ。1ならトレースする、0なら無視する。独立に、0なら平均した回転量を両目に適用する。

__AV_TRACK,x,y,z,rx,ry,rz,eyeLrx,eyeLry,eyeLrz,eyeRrx,eyeRry,eyeRrz,flag
　頭部動作のパラメータ。頭の移動量(x,y,z)と回転量(rx,ry,rz)のあと左目と右目の回転量。移動量の単位はミリ、回転量の単位はラジアン。
　flag は目の回転量がグローバルのときに1、ローカルの時に0を指定する（OpenFace の AU の場合1, ARKit の値を使う場合は0）

__AV_ARKIT,shape=rate,shape=rate,...
　ARKit のフェイストラッキングの shape 名とその強度 [0..1] の組の集合。この値と shapemap の内容をもとにアバターの表情が制御される。 __AV_AU とは併用しない。

__AV_AU,num=rate,num=rate,...
　Action Unit の番号（1～46）とその強度 [0..1] の組の集合。この値と shapemap で定義したマッピングをもとにアバターの表情が制御される。__AV_ARKIT とは併用しない。

__AV_EXMORPH,name=rate,name=rate,...
　任意モーフの外部制御。nameで指定した名前に対応するモーフの強度を指定する。値は [0..1]。ここで使われる名前 name と実際に操作するモーフは、shapemap 内で "EXMORPH_name ボーン名" のように対応を指定する必要あり。

__AV_EXBONE,name,x,y,z,rx,ry,rz,rw,name,x,y,z,rx,ry,rz,rw,...
　任意ボーンの外部制御。nameで指定した名前に対応するボーンの移動量と回転量を指定する。単位はそれぞれミリとクォータニオン。ここで使われる名前 name と実際に操作するボーンの対応は、shapemap 内で "EXBONE_name ボーン名" のように指定する必要あり。複数の指定を1回で行える。

__AV_MESSAGE,string
　string をMMDAgent-EXの制御メッセージとして MMDAgent-EX 内へ送る。任意のメッセージを指定可能。

SNDSTRM
　以後のSNDパートを音声ストリームとみなし、VADを有効にする。（デフォルト））

SNDFILE
　以後のSNDパートをファイルチャンクとみなし、VAD を無効にする。音声ファイル送信は(1) SNDFILE送信、(2)SNDパートで音声データ送信、(3) SNDBRKS で終了信号送信、の３段階で行われる。

SNDBRKS
　送られてきている音声をここで区切る。

SNDから始まるパート
　音声データ。仕様は後述

```

## 制御開始・終了・設定

**__AV_START**

外部 API の有効化を宣言します。これを受け取った MMDAgent-EX は、次に **__AV_END** が来るまでの間、受信メッセージに従ってモデルの操作を行います。起動状態のデフォルトでは API は無効化されているため、APIを利用する場合は最初に必ずこれを送る必要があります。

{{<message>}}
__AV_START
{{</message>}}

**__AV_END**

外部 API の無効化を宣言します。これを受け取った MMDAgent-EX は、APIによる操作を終了します。（無効化中に送られたAPIメッセージは無視されます。）

{{<message>}}
__AV_END
{{</message>}}

## モデル選択

**__AV_SETMODEL,エイリアス名**

操作対象とするモデルのエイリアス名を指定します。これを受け取った MMDAgent-EX は、指定されたエイリアス名で動作しているモデルを以降の操作対象とします。

{{<message>}}
__AV_SETMODEL,0
{{</message>}}

- 外部APIで同時に操作できるモデルは1体のみです。
- 指定されたエイリアス名のモデルが MMDAgent-EX 上で動作していない場合、このメッセージは無視されます。
- 利用中にこのメッセージで対象モデルを切り替えることも可能です。

## 対話アクション再生

**__AV_ACTION,アクション番号**

指定した番号の対話アクションを再生します。番号は 0 から指定できます。これを受け取った MMDAgent-EX は、操作対象モデルに対して対応するモーションの再生を開始します。

{{<message>}}
__AV_ACTION,3
{{</message>}}

- アクション番号は数値で指定します。
- 番号と再生モーションの対応は、モデルの[.shapemap ファイル](../shapemap)で定義されています。
- shapemap ファイルが存在しない、あるいは指定番号のアクションが未定義の場合、メッセージは無視されます。
- CG-CA モデルでは、以下のアクションがデフォルトで定義されています。

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

新たなアクション番号と対応モーションを追加登録するには、.shapemapファイルに追記します。例えば、40番としてお辞儀モーション (ojigi.vmd) を追加する場合、以下のように .shapemap に書きます。（.vmdファイルのパスはモデルファイル(.pmd)からの相対パスです）

```text
ACT40 somewhere/ojigi.vmd
```

このアクションは以下のように指示して再生できます。

{{<message>}}
__AV_ACTION,40
{{</message>}}

## ヘッドトラッキング

**__AV_TRACK,x,y,z,rx,ry,rz,eyeLrx,eyeLry,eyeLrz,eyeRrx,eyeRry,eyeRrz,flag**

操作者の頭部動作のパラメータを送ります。

- **x,y,z**: 頭部の移動量（mm）
- **rx,ry,rz**: 頭部の回転量 (Radian)
- **eyeLrx,eyeLry,eyeLrz**: 左目の回転量 (Radian)
- **eyeRrx,eyeRry,eyeRrz**: 左目の回転量 (Radian)
- **flag** 目の回転量のグローバル(1), ローカル(0)を指定

**flag** で目の回転量をグローバル回転量として扱うかローカル回転量として扱うかを指定できます。OpenFace の出力を使う場合は 1 を、Apple ARKit の出力を使う場合は 0 を指定してください。

**__AV_RECALIBRATE**

顔の向きを再キャリブレーションします。MMDAgent-EX は **__AV_START** を受け取った直後の操作者の顔の向きを正面として向きのキャリブレーションが行われます。このコマンドは、そのキャリブレーションのみを再実行するものです。

{{<message>}}
__AV_RECALIBRATE
{{</message>}}

**__AVCONF_ALLOWFARCLOSEMOVE,値**

操作者の前後の動きをトレースするかどうかを指定します。1なら前後の動きもアバターへトレースし、0なら操作者の前後の動きは無視します。デフォルトは 1 です。

{{<message>}}
__AVCONF_ALLOWFARCLOSEMOVE,1
{{</message>}}


## フェイシャルトラッキング

**__AV_ARKIT,shape=rate,shape=rate,...**

ARKit のフェイストラッキングの shape 名とその強度 [0..1] の組の集合。この値と shapemap の内容をもとにアバターの表情が制御される。 __AV_AU とは併用しない。

**__AV_AU,num=rate,num=rate,...**

Action Unit の番号（1～46）とその強度 [0..1] の組の集合。この値と shapemap で定義したマッピングをもとにアバターの表情が制御される。__AV_ARKIT とは併用しない。

## ボーン個別制御

**__AV_EXBONE,name,x,y,z,rx,ry,rz,rw,name,x,y,z,rx,ry,rz,rw,...**

任意ボーンの外部制御。nameで指定した名前に対応するボーンの移動量と回転量を指定する。単位はそれぞれミリとクォータニオン。ここで使われる名前 name と実際に操作するボーンの対応は、shapemap 内で "EXBONE_name ボーン名" のように指定する必要あり。複数の指定を1回で行える。

## モーフ個別制御

**__AV_EXMORPH,name=rate,name=rate,...**

任意モーフの外部制御。nameで指定した名前に対応するモーフの強度を指定する。値は [0..1]。ここで使われる名前 name と実際に操作するモーフは、shapemap 内で "EXMORPH_name ボーン名" のように対応を指定する必要あり。


## 音声伝送

音声データは以下で説明する方法でエンコードして、外部操作と同じソケットへ送り込みます。以下の `xxxx` は4桁の数字で、そのあとに続くデータ本体のバイト長を10進数4桁で表します。16kHz, 16bit, mono のデータのみです。長い音声を一括で送信すると遅延が発生するので、なるべく40ms分 (1280 Bytes) ぐらいの短いセグメントで区切って逐次送信してください。

```text
１パックあたり ヘッダ7byte+本体
   文字列 "SND"   1バイト目～3バイト目
   数値 "xxxx"    4バイト目～7バイト目, decimal
   音声データ本体 8バイト目～(xxxxの値 + 7) バイト目
```

音声伝送のモードとして、ファイルモードとストリーミングモードの2種類のモードがあります。

ファイルモードでは、音声データは上記のとおり短いチャンクに区切って送信し（全体を1つの大きなチャンクとして一度に送信することも可能）、最後に発話終端信号を送ります。MMDAgent-EX は、1つ目のチャンクの受信終了と同時に音声の再生を開始して、送信された音声データを出力し、発話終端に達したらセッションの終了とリップシンクの口閉じを行います。

ストリーミングモードでは、音声送信は短チャンクごとに行う必要があります。明示的な発話終端は与えられないため、MMDAgent-EX 側で無音部分の検出から発話区間の区切りが行われます。

デフォルトはストリーミングモードです。ファイルモードにするには、まず先に `SNDFILE\n` を送信してモードを切り替えてから、ファイルの中身を逐次 `SND` で転送します。その際、ファイルの終端まで送信し終えたら `SNDBRKS\n` を送って入力終了をMMDAgent-EXに伝えます。ストリーミングモードに戻すには `SNDSTRM\n` を送信します。

## リップシンク

**__AVCONF_DISABLEAUTOLIP,{NO|ARKIT|AU|ARKIT+AU|ALWAYS}**

音声伝送時の伝送音声からの自動リップシンクを行わない場面の指定。デフォルトは `NO` 、つまりリップシンクを常に行う。

## その他

**__AV_MESSAGE,string**

string をMMDAgent-EXの制御メッセージとして MMDAgent-EX 内へ送る。任意のメッセージを指定可能。
