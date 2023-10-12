---
title: Plugin_Remoteによるネットワーク操作の仕様
slug: plugin-remote
---

Plugin_Remote を用いた外部連携について。

## 仕様一覧

- メッセージは1つごとに改行 "\n" で区切ってテキストモードで送信
- `SNDで始まるパート` はパケットの長さを埋め込んでバイナリモードで送信
- 接続断ごとに初期値にリセット → 値設定系メッセージは新規接続ごとに送りなおし

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
　指定した対話アクションを再生する。アクションは番号(1から）で指定する。モデルでは shapemap で指定した対応モーションが再生される。

__AV_EXMORPH,name=rate,name=rate,...
　任意モーフの外部制御。nameで指定した名前に対応するモーフの強度を指定する。値は [0..1]。ここで使われる名前 name と実際に操作するモーフは、shapemap 内で "EXMORPH_name ボーン名" のように対応を指定する必要あり。

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

## 対話アクションの動作

`__AV_ACTION` で実行される対話アクションは、 MMDAgent-EX 内部では以下の条件で重ね合わせ再生されます。

- エイリアス名は `__action`
- 全身ではなく部分モーションとして再生 (`PART`) （フレーム1以降に動作指定があるボーン・モーフのみ適用）
- ループせずに1回のみ再生（`ONCE`）
- スムージングは `ON`、リポジションは `OFF`
- 優先度は `0` （デフォルト）

## 音声伝送の仕様

音声データは以下で説明する方法でエンコードして、外部操作と同じソケットへ送り込みます。以下の `xxxx` は4桁の数字で、そのあとに続くデータ本体のバイト長を10進数4桁で表します。16kHz, 16bit, mono のデータのみです。長い音声を一括で送信すると遅延が発生するので、なるべく40ms分 (1280 Bytes) ぐらいの短いセグメントで区切って逐次送信してください。

```text
１パックあたり ヘッダ7byte+本体
   文字列 "SND"   1バイト目～3バイト目
   数値 "xxxx"    4バイト目～7バイト目, decimal
   音声データ本体 8バイト目～(xxxxの値 + 7) バイト目
```

MMDAgent-EX は、デフォルトでは、送り込まれてくるオーディオをマイク録音等の長時間ストリーミングメディアと想定し、送られてくるオーディオに対して音声区間検出を行って検出された音声区間を単位として処理を行います。音声ファイルを1単位として送り込む場合は、まず先に `SNDFILE\n` を一度送ってモードを切り替えてから、ファイルの中身を逐次 `SND` で転送してください。その際、ファイルの終端まで送信し終えたら `SNDBRKS\n` を送って入力終了をMMDAgent-EXに伝える。

## 外部操作用のモデル設定ファイル (.shapemap)

外部操作を行いたい CG モデル(.pmd）ごとに、具体的にモデル中のどのモーフをリップ信号に対応づけるのか、といった外部操作用設定ファイル（.shapemap）を用意する必要があります。この設定ファイル（.shapemap）はモデルファイル (`xxx.pmd`) と同じフォルダに `xxx.pmd.shapemap` という名前で置きます。外部操作に使うモデルには必ずこの .shapemap を定義してください。

設定ファイル (.shapemap) はテキストファイルで、中身は以下のようになっています。`#` で始まる行はコメントで無視されます。

```text
#### パラメータ

#### リップシンク用モーフ名
LIP_A あ
LIP_I い
LIP_U う
LIP_O お

#### リップシンク中に０にリセットするモーフ名のリスト
#### 上記で指定した以外の、口を開けるモーフを全て指定する
NOLIP え,おお~,ワ,えー,ああ,いい,叫び,あーれー,口わらい,mouth_a_geo_C,mouth_i_geo_C,mouth_u_geo_C,mouth_e_geo_C,mouth_o_geo_C,mouth_oh_geo_C,mouth_smile_geo_C,mouth_surprise_geo

#### プリセットモーション指定。プリセットアクション使用時に設定
## __AV_ACTION に対応するモーションファイル名を指定
ACT0 wait.vmd
ACT1 joy.vmd
ACT38 ashamed.vmd

#### 個別制御の設定 それぞれ利用する場合に設定

## __AV_EXMORPH で使用される name に対応するフェイス名
## モーフの記述方法は AU や ARKIT と同じ
#EXMORPH_name モーフ名

```

## ".pmd.loadmessage" ファイルと ".pmd.deletemessage" ファイル (MSのみ)