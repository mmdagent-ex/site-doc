---
title: 画像・テキストの表示
slug: image-and-text
---
{{< hint info >}}
**TEXTAREA_ADD**, **TEXTAREA_SET** の機能は Plugin_TextAreaが提供しています。利用時はこのプラグインが有効になっているか確かめてください。
{{< /hint >}}

# 画像・テキストの表示

音声とともにテキストや画像を使うことで、複合的で効果的なインタラクションを作ることができます。MMDAgent-EX では、画像やテキストを画面内に表示する方法を複数用意しており、対話スクリプトと組み合わせることでマルチモーダルな対話を作ることができます。

- 文章・画像をシーン内に表示
- 画面上に字幕を表示
- ユーザに選択肢を示して選択させるプロンプト提示
- READMEファイルをユーザに読ませるテキストファイル閲覧

以下ではそれぞれの機能の使い方を紹介します。

## 画像・テキストの3D空間内表示 (TEXTAREA)

3D空間内に任意のテキストあるいは画像を表示できます。手順としては以下の2ステップに分かれています。

1. 表示すべき場所（表示エリア）の定義（**TEXTAREA_ADD**）
2. 表示内容の指定（**TEXTAREA_SET**）

### 表示エリア定義

**TEXTAREA_ADD** メッセージで表示エリアを定義します。表示エリアはシーン空間上の「板」であり、その幅・高さ・位置、色、文字といったプロパティを指定します。

- 第1引数：エイリアス名（新規）
- 第2引数：幅と高さ
- 第3引数：文字の大きさ、マージン、行間。それぞれ 1.0 が基本。
- 第4引数：背景色 r,g,b,a　a = 0 で背景無し
- 第5引数：文字色 r,g,b,a
- 第6引数：中心の座標位置

{{<message>}}
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z
{{</message>}}

テキストを表示する場合、`width` あるいは `height` を指定なし(0)とすれば、その方向は制約なしとなり、板のサイズはあとで指定するテキストの内容に合わせて自動伸縮します。0以外を指定した場合、その方向は指定値に固定され、文字が溢れる場合は指定値内に収まるよう自動縮小されます。

画像の場合、 `width` と `height` のどちらかを指定なし(0)にすると、指定なしのほうは画像の縦横比に合わせて自動調整されます。`width` と `height` のどちらかは大きさを指定してください。

上記がデフォルトの使い方ですが、さらに板の回転量、モデルマウント、ボーンマウント等を指定できます。詳しくは[メッセージ一覧](http://localhost:1313/ja/docs/messages/#%e3%83%86%e3%82%ad%e3%82%b9%e3%83%88%e7%94%bb%e5%83%8f%e3%82%ab%e3%83%a1%e3%83%a9%e6%98%a0%e5%83%8f%e3%82%92%e8%a1%a8%e7%a4%ba)のページをご覧ください。

追加が完了した時点で **TEXTAREA_EVENT_ADD** が発行されます。

{{<message>}}
TEXTAREA_EVENT_ADD|alias
{{</message>}}

### 表示内容の指定

表示エリアに対して **TEXTAREA_SET** を使うことで文字列あるいは画像を表示させます。その表示エリアに既に表示がある場合、新たに指定したものに入れ替わります。

**文字列を表示する場合**、その文字列を指定します。文字列は "" で囲むことで空白を含めることができ、"\n" を使って改行もできます。

{{<message>}}
TEXTAREA_SET|(textarea alias)|"このように 文章を指定できます。\nこんにちは"
{{</message>}}

**画像を表示する場合**、その画像ファイルのパスを指定します。画像フォーマットは png, jpg が利用できます。アニメーションpngも利用できます。

{{<message>}}
TEXTAREA_SET|(textarea alias)|somewhere/image.png
{{</message>}}

指定された表示を開始した時に **TEXTAREA_EVENT_SET** が発行されます。

{{<message>}}
TEXTAREA_EVENT_SET|alias
{{</message>}}

### 表示エリア削除

**TEXTAREA_DELETE** でエリアを削除し表示を消します。削除完了時に **TEXTAREA_EVENT_DELETE** が発行されます。

{{<message>}}
TEXTAREA_DELETE|(textarea alias)
TEXTAREA_EVENT_DELETE|alias
{{</message>}}

## テキストキャプション表示

以下の画像のようにテキストをキャプション風に表示できます。上記の TextArea との違い:

- 3D空間上ではなくオンスクリーン表示（視点に寄らず一定位置に表示）
- 指定時間経過後に自動で消える
- 任意のフォント (ttf) を指定可能
- 文字の縁取りが２種まで指定可能

![caption](/images/caption.png)

利用では、まずキャプションのスタイルを定義し（**CAPTION_SETSTYLE**）、そのあと、そのスタイルを参照しながらテキストを与えて表示を行う（**CAPTION_START**）という手順になります。

### キャプションスタイルの定義

**CAPTION_SETSTYLE** でスタイルを定義します。

- 第1引数：スタイルのエイリアス名（新規）
- 第2引数：フォントファイルのパス。"default" でシステムフォントを利用。
- 第3引数：文字の色 r,g,b,a
- 第4引数：1つ目の縁取りの色および大きさ r,g,b,a,thickness。縁取り不要の場合は a あるいは thinkness を 0 に。
- 第5引数：2つ目の縁取りの色および大きさ。指定は上記と同様。
- 第6引数：枠背景の色 r,g,b,a：不要な場合は a に 0 を指定

{{<message>}}
CAPTION_SETSTYLE|style_alias|fontpath|r,g,b,a|edge1|edge2|basecolor
{{</message>}}

定義完了後に **CAPTION_EVENT_SETSTYLE** メッセージが発行されます。

{{<message>}}
CAPTION_EVENT_SETSTYLE|style_alias
{{</message>}}

### キャプション表示開始

**CAPTION_START** で新たなキャプションの表示を開始します。

- 第1引数：エイリアス名（新規）
- 第2引数：使用する定義済みスタイルのエイリアス名
- 第3引数：表示内容のテキスト。空白を含む場合は ""で囲む。"\n" で改行もできる。
- 第4引数：文字の大きさ
- 第5引数：表示の左右位置 CENTER, LEFT, RIGHT のいずれかの文字列を指定
- 第6引数：表示の上下位置 画面の一番下を 0.0、一番上を 1.0 とした相対値
- 第7引数：表示持続時間をフレーム数で（30=1秒）

なお、指定したエイリアス名のテキスト表示が既にある場合、その表示が消されて新たに指定したものに上書き変更されます。

{{<message>}}
CAPTION_START|alias|style_alias|text|size|align|height|duration
{{</message>}}

使用例：

{{<fst>}}
# "1" キーでキャプションをテスト表示
# フォントファイルは rounded-mplus-1c-heavy.ttf を使う。
# テキスト色：オレンジ
# エッジ１：白、太さ４
# エッジ２：黒半透明、太さ６
# 枠背景：描画なし
10 10:
    KEY|1 CAPTION_SETSTYLE|terop|rounded-mplus-1c-heavy.ttf|1,0.5,0,1|1,1,1,1,4|0,0,0,0.6,6|0,0,0,0
    CAPTION_EVENT_SETSTYLE|terop CAPTION_START|test|terop|てすと|3.0|CENTER|0.5|300
{{</fst>}}

表示開始時に **CAPTION_EVENT_START** メッセージが出力されます。

{{<message>}}
CAPTION_EVENT_START|alias
{{</message>}}

### キャプション表示終了

表示中のテキストは指定した時間経過で消えますが、**CAPTION_STOP** メッセージを発行することですぐに削除もできます。

{{<message>}}
CAPTION_STOP|alias
{{</message>}}

表示終了時には **CAPTION_EVENT_STOP** メッセージが出力されます。

{{<message>}}
CAPTION_EVENT_STOP|alias
{{</message>}}
