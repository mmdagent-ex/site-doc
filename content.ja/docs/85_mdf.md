---
title: mdf設定項目一覧
slug: mdf
---
# .mdf で設定可能なパラメータの一覧

## しくみ

- MMDAgent-EXは.mdfファイルを指定してコンテンツを起動する
  - .mdf ファイルはコンテンツのトップディレクトリにある。
- .mdf ファイルの中身はテキストファイル。
  - MMDAgent-EXの動作パラメータを指定できる
- MMDAgent-EX の実行バイナリと同じディレクトリにある `MMDAgent-EX.mdf` はシステム設定
  - 全ての起動時に最初に読み込まれる
  - コンテンツの.mdfと設定が重なる場合、コンテンツ側が優先される
- `％ENV{名前}` のように記述することで任意の環境変数の値を取り込める。

## 注意事項

- 以下の一覧において、値は基本的にデフォルトの値
- 3D空間の座標はおおよそ 1.0 ≒ 8cm と考えてよい（MMDスケール）

# 設定項目一覧

## 入出力

ログをファイルに出力する。デフォルトは空白（＝出力しない）。

{{<mdf>}}
log_file=
{{</mdf>}}

{{< hint ms >}}
## Webカメラ

`TEXTAREA_SET` でWebカメラを開くときのWebカメラの解像度を指定する。

{{<mdf>}}
Plugin_TextArea_Camera_Size=1280x720
{{</mdf>}}

`TEXTAREA_SET` で長いテキストを指定したときに自動折り返しを有効にし、その1行当たりの文字数を指定する (>0) もしくは自動折り返しを無効にする(<=0)。

{{<mdf>}}
Plugin_TextArea_MaxLineLen=40
{{</mdf>}}

{{< /hint >}}

## プラグイン

プラグインの有効・無効を指定。

{{<mdf>}}
disablePlugin=ALL
enablePlugin=Audio,VIManager
{{</mdf>}}

右辺の値は、以下の文字列が指定可能

- **`ALL`** : 全てのプラグインにマッチ
- **`NONE`** : 何にもマッチしない
- **プラグイン名**： `Plugins` ディレクトリ以下にある `Plugin_xxxx.dll` あるいは `Plugin_xxxx.so` の `xxxx` の部分の名前を指定。上記の例では Plugin_Audio.dll （あるいは.so）と Plugin_VIManger.dll（あるいは.so）のみ有効にしている。複数ある場合はカンマ区切りで。

評価は `enablePlugin` → `disablePlugin` の順でなされる。.mdf 内の記述順には関わらない。

例１：プラグイン `A`, `B`, `C` のみ有効でそれ以外は無効にする場合：

{{<mdf>}}
enablePlugin=A,B,C
disablePlugin=ALL
{{</mdf>}}

例２：プラグイン `D`, `E` を無効にしてそれ以外は有効にする場合：

{{<mdf>}}
disablePlugin=D,E
{{</mdf>}}

※ 以下の旧バージョンでの書き方（無効にするプラグインを1つずつ指定）も使える

{{<mdf>}}
exclude_Plugin_Audio=yes
{{</mdf>}}

{{< hint ms >}}

## フォント

システムフォントを変更する。フォントファイル（.otf もしくは .ttf ファイル）を `AppData/Noto_Fonts/` フォルダ以下へ置き、そのファイル名を以下のように指定する。

{{<mdf>}}
systemFontFile=フォントファイル名
{{</mdf>}}

{{< /hint >}}

## ネットワーク

※ Plugin_Remote 利用時に有効

※ このセクションのみ値はデフォルト値ではなくサンプル値

### WebSocketサーバを使う場合

WebSocket の接続先のホスト名・ポート番号・パスを指定

{{<mdf>}}
Plugin_Remote_Websocket_Host=localhost
Plugin_Remote_Websocket_Port=9000
Plugin_Remote_Websocket_Directory=/chat
{{</mdf>}}

### TCP/IP サーバ

TCP/IP クライアントになってサーバへ接続する場合

{{<mdf>}}
Plugin_Remote_EnableClient=true
Plugin_Remote_Hostname=localhost
Plugin_Remote_Port=50001
{{</mdf>}}

TCP/IP サーバになる場合

{{<mdf>}}
Plugin_Remote_EnableServer=true
Plugin_Remote_ListenPort=50001
{{</mdf>}}


### 共通の設定

接続失敗時に自動リトライする回数を指定（デフォルトは 0）

{{<mdf>}}
Plugin_Remote_RetryCount=60
{{</mdf>}}

## 音声再生 (SPEAK_START) (v1.0.4)

**SPEAK_START** において再生モードをv1.0.3以前の同期保証16kHz変換再生にする（未指定あるいは false の場合、v1.0.4以降の高音質再生を使う）

{{<mdf>}}
Plugin_Remote_Speak_16k=true
{{</mdf>}}

## 画面

ウィンドウの初期サイズ（横,縦）

{{<mdf>}}
window_size=600,600
{{</mdf>}}

起動時にフルスクリーンにする（`F`キーで起動後に切り替え可能）

{{<mdf>}}
full_screen=false
{{</mdf>}}

起動時に左上の動作状態を表示（`S`キーで起動後に切り替え可能）

{{<mdf>}}
show_fps=true
{{</mdf>}}

(Windows) 透明ウィンドウの有効・無効を指定する。`true` 時、ウィンドウが透過される。透過部分へのクリックは、その下のアプリケーションへ抜ける。

デフォルトでは色ベースの透過が行われる。レンダリング時には特別な「透過色」が背景のキャンパスカラーにセットされて描画され、描画結果上でその透過色と同じ色のピクセルが透過する。デフォルトの透過色はグリーン (0.0,1.0,0.0) であるが、`transparent_color` で変更できる。

`transparent_pixmap` を `true` にすることで、遅いが精度の高いピクスマップベースの透過法を使うことができる。描画結果のピクスマップの持つアルファチャネル（透過チャネル）の値がそのままウィンドウの透過値として用いられる。この方法は色ベースの透過に比べて常に自然で良いクオリティの透過が行えるが、一方で処理が遅くなり、特に大きな画面ではフレームレートが大きく低下する。

なお透過中はステージ背景のイメージは描画されない。

{{<mdf>}}
transparent_window=false
{{</mdf>}}

(Windows) 色ベースの透過において用いられる透過色を指定・変更する。デフォルトはグリーン (0.0,1.0,0.0)。

{{<mdf>}}
transparent_color=0.0,1.0,0.0
{{</mdf>}}

(Windows) `true` にすることで、色ベースの透過ではなくピクスマップベースの透過法を有効にする。`transparent_pixmap` を `true` にすることで、遅いが精度の高いピクスマップベースの透過法を使うことができる。描画結果のピクスマップの持つアルファチャネル（透過チャネル）の値がそのままウィンドウの透過値として用いられる。この方法は色ベースの透過に比べて常に自然で良いクオリティの透過が行えるが、一方で処理が遅くなり、特に大きな画面ではフレームレートが大きく低下する。

{{<mdf>}}
transparent_pixmap=false
{{</mdf>}}

## 3-Dモデル

いちどに表示するモデルの最大数。最小は1、最大は1024。

{{<mdf>}}
max_num_model=10
{{</mdf>}}

トゥーンエッジの太さ（`K`, `Shift+K` で起動後に変更可能）

![bold edge](/images/edge1.png)
![thin edge](/images/edge2.png)

{{<mdf>}}
cartoon_edge_width=0.35
{{</mdf>}}

トゥーンエッジを光源方向に合わせて調整する機能(v1.0.5以降)をOFFにしてMMD互換に戻す

{{<mdf>}}
light_edge=false
{{</mdf>}}

スキニングに使用する並列スレッド数。通常はデフォルトの1で問題ないが、頂点数の多い巨大なモデルでレンダリングが遅くなってしまう場合は `2` や `4` を指定する。メッセージであとで変更できる。

{{<mdf>}}
parallel_skinning_numthreads=1
{{</mdf>}}


## 視点（カメラ）

初期カメラパラメータ。上から順に位置、回転量(度)、カメラ距離、視野角(度)。

{{<mdf>}}
camera_transition=0.0,13.0,0.0
camera_rotation=0.0,0.0,0.0
camera_distance=100.0
camera_fovy=16.0
{{</mdf>}}

## CG描画

アンチエイリアス (MSAA) 強度。大きいほど線が滑らかに表示されるが重くなる。0で機能をOFFにする。設定可能な最大値は 32。

{{<mdf>}}
max_multi_sampling=4
{{</mdf>}}

背景画像と床画像の3D空間での大きさ。パラメータ(x,y,z)は x=幅の半分, y=床の奥行, z=背景の高さ。

![stage image](/images/stage.png)

{{<mdf>}}
stage_size=25.0,25.0,40.0
{{</mdf>}}

キャンパスカラー（空間背景色） (R,G,B)

{{<mdf>}}
campus_color=0.0,0.0,0.2
{{</mdf>}}

光源の到来方向 (x,y,z,w), 強さ (0.0～1.0)、色 (R,G,B) 。到来方向と色は起動後にメッセージでも変更可能。

{{<mdf>}}
light_direction=0.5,1.0,0.5,0.0
light_intensity=0.6
light_color=1.0,1.0,1.0
{{</mdf>}}

ディフュージョンフィルター： `diffusion_postfilter=true` で有効化

※ Windows, Linux のみ　macOS では利用不可

{{<mdf>}}
diffusion_postfilter=false
diffusion_postfilter_intensity=0.6
diffusion_postfilter_scale=1.0
{{</mdf>}}

## 影

起動時の影表示の初期設定（`Shift+S` で起動後に切り替え可能）

{{<mdf>}}
use_shadow=true
{{</mdf>}}

起動時にシャドウマッピングをONにする（`X` で起動後に切り替え可能）

{{<mdf>}}
use_shadow_mapping=false
{{</mdf>}}

Doppel Shadow エフェクトのON/OFF（デフォルトはOFF）とパラメータ

![doppel_shadow](/images/doppel_shadow.png)

{{<mdf>}}
# doppel shadow を on
doppel_shadow=true
# 二重影の色
doppel_shadow_color=r,g,b
# 二重影のオフセット
doppel_shadow_offset=x,y,z
# 影の濃さ（デフォルト 0.5）
shadow_density=0.5
{{</mdf>}}

## 物理演算

物理演算のシミュレーション解像度(fps)。30, 60, 120 が指定可能。値を小さくすると
処理が軽くなるが、剛体の抜けが生じやすくなる。

{{<mdf>}}
bullet_fps=120
{{</mdf>}}

## 外部操作

外部操作中のリップシンクをリモート音声からマイク入力に切りかえる（`yes` 指定時）

{{<mdf>}}
Plugin_Remote_EnableLocalLipsync=no
{{</mdf>}}

上記が `yes` のとき、さらに以下を `yes` を指定するとマイク入力を音声出力へパススルーする

{{<mdf>}}
Plugin_Remote_EnableLocalPassthrough=no
{{</mdf>}}

リップシンクの音声を指定ディレクトリ以下に発話単位で録音する。録音時間の上限を分で指定可能（デフォルト: 120分）

{{<mdf>}}
Plugin_Remote_Record_Wave_Dir=directory
Plugin_Remote_Record_Wave_Limit=120
{{</mdf>}}

**MOTIONCAPTURE_START** メッセージでモーションを保存する際の最大持続時間（単位：分）

{{<mdf>}}
motion_capture_max_minutes=10
{{</mdf>}}

{{< hint ms >}}

リップシンクに連動した頭部上下動 (speech2headmotion) 機能における上下動作の大きさと速度の調整係数。値が大きいほど大きく・速く動くようになる。デフォルトは 1.0。

{{<mdf>}}
Plugin_Remote_Speech2Head_Angle_Coef=1.0
Plugin_Remote_Speech2Head_Speed_Coef=1.0
{{</mdf>}}

WebSocket 経由の接続に対してパスワードを要求する

{{<mdf>}}
Plugin_Remote_WebSocket_Password=パスワード
{{</mdf>}}

操作が一定時間行われないときに **AVATAR_EVENT_IDLE|START** メッセージが発行されるが、その一定時間（デフォルトでは15秒）を指定した秒数に変更する。

{{<mdf>}}
Plugin_Remote_Idle_Timeout_Second=秒数
{{</mdf>}}

{{< /hint >}}

## 音声認識

**Plugin_Julius_conf**, **Plugin_Julius_lang**

音声認識エンジンの設定名と言語名。

デフォルト指定は無し。モデルを準備し、これらの有効な組み合わせを .mdf で指定することで Plugin_Julius が有効化される。

デフォルトのモデルがサポートする組み合わせ：

- dnn, ja
- dnn, en
- gmm, ja

{{<mdf>}}
Plugin_Julius_conf=dnn
Plugin_Julius_lang=en
{{</mdf>}}

**Plugin_Julius_wordspacing**

認識結果の出力において、単語を区切るかどうかを指定。

- `no`: 単語間に何も入れずに詰める（`ja` 時のデフォルト）
- `yes`: 単語間に空白を入れる（`ja` 以外のデフォルト）
- `comma`: 単語間にカンマを入れる（旧MMDAgentと互換）

{{<mdf>}}
Plugin_Julius_wordspacing=yes
{{</mdf>}}

**Plugin_Julius_logfile**

Julius エンジンの内部ログをファイルに出力させる。

{{<mdf>}}
Plugin_Julius_logfile=log.txt
{{</mdf>}}

**show_caption**

字幕を表示する。画面左側に音声認識結果が、右側に音声合成内容（**SYNTH_START** で与えられた文章）がそれぞれ表示される。

{{<mdf>}}
show_caption=true
{{</mdf>}}

## その他の調整項目

### HTTP サーバ

HTTPサーバ機能を無効化する（デフォルト：有効）

{{<mdf>}}
http_server=false
{{</mdf>}}

ポート番号を変更する（デフォルト：50000）

{{<mdf>}}
http_server_port=50000
{{</mdf>}}

### レンダリング関連

カートゥーンレンダリングを使用

{{<mdf>}}
use_cartoon_rendering=true
{{</mdf>}}

MMD互換の色付けを使う

{{<mdf>}}
use_mmd_like_cartoon=true
{{</mdf>}}

被選択モデルのエッジ色 (R,G,B,A、値は 0.0～1.0)

{{<mdf>}}
cartoon_edge_selected_color=1.0,0.0,0.0,1.0
{{</mdf>}}

物理演算で y = 0 に床平面を入れるかどうか。

{{<mdf>}}
bullet_floor=true
{{</mdf>}}

重力係数

{{<mdf>}}test
gravity_factor=10.0
{{</mdf>}}

モデルの内部コメントをロード時に表示する長さ（秒）。0で表示しない。

{{<mdf>}}
display_comment_time=0
{{</mdf>}}

シャドウマッピング用テクスチャの一辺のサイズ

{{<mdf>}}
shadow_mapping_texture_size=1024
{{</mdf>}}

シャドウマッピング時にモデルに落とす影の濃さ

{{<mdf>}}
shadow_mapping_self_density=1.0
{{</mdf>}}

シャドウマッピング時に床に落とす影の濃さ

{{<mdf>}}
shadow_mapping_floor_density=0.5
{{</mdf>}}
シャドウマッピングのレンダリング順：true で明→暗、false で暗→明の順

{{<mdf>}}
shadow_mapping_light_first=true
{{</mdf>}}

### 表示関連

ボタン定義時、ボタンを起動時に画面に表示（`Q`キーで起動後に切り替え可能）

{{<mdf>}}
show_button=true
{{</mdf>}}

簡易ログ表示位置（サイズ・位置・スケール）

{{<mdf>}}
log_size=80,30
log_position=-17.5,3.0,-20.0
log_scale=1.0
{{</mdf>}}

モーション再生タイミング微調整（単位：秒、最大値 10.0）

{{<mdf>}}
motion_adjust_time=0.0
{{</mdf>}}

自動リップシンクで生成されるリップモーションの再生時の優先度

{{<mdf>}}
lipsync_priority=100.0
{{</mdf>}}

### ユーザインタフェース関連

キー・マウス操作時の感度調整：カメラ回転・カメラ移動・距離・視野角

{{<mdf>}}
rotate_step=4.5
translate_step=0.5
distance_step=4.0
fovy_step=1.0
{{</mdf>}}

`K`, `Shift+K` キーでエッジの太さを変更する際のステップ倍数

{{<mdf>}}
cartoon_edge_step=1.2
{{</mdf>}}

{{< hint ms >}}
### フェイストラッキング関連パラメータ[MS]

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
# 左右反転
Plugin_Remote_EnableMirrorMode=false
{{</mdf>}}

{{< /hint >}}
