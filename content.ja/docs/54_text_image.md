---
title: 画像・テキストの表示
slug: image-and-text
---
# 画像・テキストの表示


## テキスト・画像・カメラ映像を表示

任意のテキスト、画像、あるいはライブカメラ映像を3D空間内に表示する。

手順は、まず **TEXTAREA_ADD** で表示エリアを定義して、**TEXTAREA_SET** でそこに表示する内容を指定する。 **TEXTAREA_SET** を繰り返すことで同じ場所で内容を変えていける。

**TEXTAREA_ADD**

エリアを新たに追加。大きさ、色、座標、向きを指定する。座標はエリアの中心点で指定。親モデル指定でそのモデルに「載せる」ことが可能。

追加が完了した時点で **TEXTAREA_EVENT_ADD** が発行される。

- 第1引数：エイリアス名（新規）
- 第2引数：幅と高さ
  - 正の値：固定サイズ（内容がはみ出す場合、収まるよう縮小される）
  - 0：可変サイズ：内容に従って自動調整される。画像の場合縦横比は保持される。
- 第3引数：文字の大きさ、マージン、行間。それぞれ 1.0 が基本。
- 第4引数：背景色 r,g,b,a　a = 0 で背景無し
- 第5引数：文字色 r,g,b,a
- 第6引数：中心の座標
- 第7引数（省略可）：向き（回転量）
- 第8引数（省略可）：親モデルのモデルエイリアス
- 第9引数（省略可）：親モデルのマウントするボーン名（省略時は「センター」を使う）

```text
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z|rx,ry,rz
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z|rx,ry,rz|(parent model alias)
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z|rx,ry,rz|(parent model alias)|(parent bone name)
TEXTAREA_EVENT_ADD|alias
```

**TEXTAREA_SET**

エリアに文字あるいは画像を表示する。表示開始時に **TEXTAREA_EVENT_SET** が発行される。既に表示されている場合は入れ替える。

表示内容は第2引数で指定：

- **文字列を記述**すると、その文字列を表示。空白を含む場合は文字列を "" で囲む。"\n" で改行もできる。
- **画像ファイルのパスを記述**すると、その画像を表示。

```text
TEXTAREA_SET|(textarea alias)|(string or image path)
TEXTAREA_EVENT_SET|alias
```

**TEXTAREA_DELETE**

エリアを削除し表示を消す。削除完了時に **TEXTAREA_EVENT_DELETE** が発行される。

```text
TEXTAREA_DELETE|(textarea alias)
TEXTAREA_EVENT_DELETE|alias
```

## テキストキャプション

テキストキャプションを表示する。上記の TextArea との違い:

- 3D空間上ではなくオンスクリーン表示（視点に寄らず一定位置に表示）
- 任意のフォントを指定可能
- 文字の縁取りが２種まで指定可能
- 指定時間経過後に自動で消えるよう指定可能

![caption](/images/caption.png)

**CAPTION_SETSTYLE**

スタイルを定義。定義後に **CAPTION_EVENT_SETSTYLE** を発行する。

- 第1引数：スタイルのエイリアス名（新規）
- 第2引数：フォントファイルのパス "default" でシステムフォントを利用
- 第3引数：文字の色 r,g,b,a
- 第4引数：1つ目の縁取りの色および大きさ r,g,b,a,thickness 縁取り不要の場合は a あるいは thinkness を 0 に
- 第5引数：2つ目の縁取りの色および大きさ 指定は上記と同様
- 第6引数：枠背景の色 r,g,b,a不要な場合は a に 0 を指定

```text
CAPTION_SETSTYLE|style_alias|fontpath|r,g,b,a|edge1|edge2|basecolor
CAPTION_EVENT_SETSTYLE|style_alias
```

**CAPTION_START**

テキスト表示開始。スタイルを指定する。指定エイリアス名のテキスト表示が既にある場合は変更される。**CAPTION_STOP** あるいは `duration` で指定した時間が経過すれば消える。

- 第1引数：エイリアス名（新規）
- 第2引数：使用する定義済みスタイルのエイリアス名
- 第3引数：表示内容のテキスト。空白を含む場合は ""で囲む。"\n" で改行もできる。
- 第4引数：文字の大きさ
- 第5引数：表示の左右位置 CENTER, LEFT, RIGHT のいずれかの文字列を指定
- 第6引数：表示の上下位置 画面の一番下を 0.0、一番上を 1.0 とした相対値
- 第7引数：表示持続時間をフレーム数で（30=1秒）

```text
CAPTION_START|alias|style_alias|text|size|align|height|duration
CAPTION_EVENT_START|alias
CAPTION_EVENT_STOP|alias
```

使用例：

```text
# "1" キーでキャプションをテスト表示
# フォントファイルは rounded-mplus-1c-heavy.ttf を使う。
# テキスト色：オレンジ
# エッジ１：白、太さ４
# エッジ２：黒半透明、太さ６
# 枠背景：描画なし
10 10:
    KEY|1 CAPTION_SETSTYLE|terop|rounded-mplus-1c-heavy.ttf|1,0.5,0,1|1,1,1,1,4|0,0,0,0.6,6|0,0,0,0
    CAPTION_EVENT_SETSTYLE|terop CAPTION_START|test|terop|てすと|3.0|CENTER|0.5|300
```

**CAPTION_STOP**

表示中のテキストを強制削除する。成功時に **CAPTION_EVENT_STOP** を発行する。

```text
CAPTION_STOP|alias
CAPTION_EVENT_STOP|alias
```

## テキストプロンプトを提示しユーザの回答を得る

**PROMPT_SHOW**

メッセージダイアログを表示して、ユーザに選択させる。指定するテキストが空白を含む場合は "" でくくる。

```text
PROMPT_SHOW|(main text)|(item text 0)|(item text 1)|...
```

例：

```text
PROMPT_SHOW|"main text"|item1|item2|item3
```

![prompt](/images/prompt.png)

ユーザがいずれかの項目を選択したら、**PROMPT_EVENT_SELECTED** が選択されたアイテムの番号 (0～）とともに発行され、このダイアログは消える。選択をキャンセル（ダイアログ外をクリックあるいは ESC キー）された場合は -1 が返る。

```text
PROMPT_EVENT_SELECTED|(selected number or -1 for cancel)
```

## ドキュメントを全画面表示しユーザの反応を得る

**INFOTEXT_FILE**

テキストファイルの中身をフルスクリーンで画面表示する。表示開始時に **INFORTEXT_EVENT_SHOW** が発行される。

- 第1引数：テキストファイルのパス
- 第2引数：タイトルラベル
- 第3引数：選択ボタンラベル カンマで区切る 例："Yes,No,Cancel"
- 第4引数（省略可）：文字スケール（デフォルト：1.0）
- 第5引数（省略可）：背景色 "RRGGBBAA" の16進数で 例：白=FFFFFFFF
- 第6引数（省略可）：文字色 同上

表示された文書はドラッグ（スワイプ）でスクロール可能。

下部に第3引数で指定したラベルが表示される。ユーザがいずれか選択すると、表示が終了し、**INFORTEXT_EVENT_CLOSE** が押されたボタンのインデックスとともに発行される。

例： README.txt を表示

```text
INFOTEXT_FILE|README.txt|"read me"|OK,NO
```

![infotext](images/infotext.png)

```text
INFOTEXT_FILE|(filepath)|(titleLabel)|(buttonLabels)
INFOTEXT_FILE|(filepath)|(titleLabel)|(buttonLabels)|(scale)
INFOTEXT_FILE|(filepath)|(titleLabel)|(buttonLabels)|(scale)|(BACKGROUNDCOLOR)|(TEXTCOLOR)
INFOTEXT_EVENT_SHOW
INFOTEXT_EVENT_CLOSE|(selecteDButtonLabel)
```


**INFOTEXT_STRING**

文字列を直接指定して、フルスクリーンで画面に表示する。

- 第1引数：テキストの内容（文字列）
- 第2引数：タイトルラベル
- 第3引数：選択ボタンラベル 例："Yes,No,Cancel"
- 第4引数（省略可）：文字スケール（デフォルト：1.0）
- 第5引数（省略可）：背景色 "RRGGBBAA" の16進数で 例：白=FFFFFFFF
- 第6引数（省略可）：文字色 同上

選択ボタンラベルは画面下部に現れるボタン。カンマで区切って複数指定可能。どれかが押されたら表示が終了する。

表示完了時に **INFORTEXT_EVENT_SHOW**, ボタンが選択されて表示が終了したときに **INFORTEXT_EVENT_CLOSE** が押されたボタンのインデックスとともに発行される。

```text
INFOTEXT_STRING|textbody|(titleLabel)|(buttonLabels)
INFOTEXT_STRING|textbody|(titleLabel)|(buttonLabels)|(scale)
INFOTEXT_STRING|textbody|(titleLabel)|(buttonLabels)|(scale)|(BACKGROUNDCOLOR)|(TEXTCOLOR)
INFOTEXT_EVENT_SHOW
INFOTEXT_EVENT_CLOSE|(selecteDButtonLabel)
```
