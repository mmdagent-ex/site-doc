---
title: 背景・床・フレーム
slug: scene
---
# 背景・床・フレーム

音声インタラクションにおける主体はもちろんCGキャラクター本体ですが、画面に表示される背景やフレームといった付帯情報もいいかげんにはできません。人が服によって相手に与える印象が変わるように、キャラクターの背景や周囲に何を表示するかは、全体的な印象に影響を与えます。

ここでは MMDAgent-EX の機能のうち、CGキャラクター以外に関連するシーン設定の項目を説明します。

- 空間色
- 背景と床の画像
- 3Dステージ
- 画面フレーム

{{< details "ドラッグ＆ドロップ" close >}}
**Windowsのみ**: エクスプローラから画像ファイルを背景部にドラッグ＆ドロップでも変更できます。

- 背景：画像をドロップ
- 床：画像を `CTRL` を押しながらドロップ
{{< /details >}}

## 空間の色

空間のデフォルトの色（＝何もない空間の色）は .mdf で `campus_color` で指定できます。`r,g,b` は 0.0から1.0で R, G, B の強度を指定します。デフォルトは濃青色（`0,0,0.2`）です。

{{<mdf>}}
campus_color=r,g,b
{{</mdf>}}

## 背景・床

**STAGE** メッセージを発行することで床と背景の画像を設定・変更できます。画像２つを "床画像,背景画像" の順で指定します。.png, .jpg が使えます。

{{<message>}}
STAGE|(floor image file),(back image file)
{{</message>}}

シーン内で床・背景は板で表示されます。この板のサイズは以下のように .mdf で変更できます。

{{<mdf>}}
stage_size=x,y,z
{{</mdf>}}

`x,y,z` はそれぞれ以下の部分の長さを指定します。`x` は幅の半分である点に注意してください。

![stage image](/images/stage.png)

## ステージモデル

ステージ用の3Dモデルを指定してシーン全体を3Dモデルで表現することができます。使用できるのは .pmd 形式 (.pmx形式から変形したものを含む) のみです。**STAGE** メッセージでモデルファイルを指定します。

{{<message>}}
<eps> STAGE|stage/tatami_room/tatami_room.pmd
{{</message>}}

※ステージモデル使用時は床・背景の描画は行われません。

以下は Example の `stage` フォルダ以下にあるサンプルを **STAGE** で指定した場合の例です。

![stage example](/images/stage_example.png)

## 画面フレーム

**WINDOWFRAME** メッセージで任意の PNG 画像を画面の一番手前に全体に貼ることができます。透過PNGに対応しているので、以下のように透過画像を使うことで、画面にフレームを貼るような使い方ができます。**WINDOWFRAME|画像ファイル名** のように使います。以下は利用例です。

![window frame example 1](/images/windowframe_example.png)

![window frame example 2](/images/windowframe_example2.png)

表示された状態で **WINDOWFRAME|別の画像ファイル名** で切り替えることができます。また、**WINDOWFRAME|NONE** とすることで削除して元の状態に戻せます。

複数の画像を重ね合わせたいときは **WINDOWFRAME_ADD** を使います。**WINDOWFRAME_ADD|名前|画像ファイル名** で追加します。異なる名前を使うことで、どんどん足して重ね合わせ表示ができます。同じ名前で別の画像ファイルを指定することで表示中の画像を別のものに入れ替えることができます。

{{<message>}}
<eps> WINDOWFRAME_ADD|frame1|images/frame_trad.png
{{</message>}}

削除するには **WINDOWFRAME_DELETE|名前** で指定した名前のフレームを削除できます。

{{<message>}}
<eps> WINDOWFRAME_DELETE|frame1
{{</message>}}

あるいは **WINDOWFRAME_DELETEALL** ですべてのフレームを一括削除できます。

{{<message>}}
<eps> WINDOWFRAME_DELETEALL
{{</message>}}
