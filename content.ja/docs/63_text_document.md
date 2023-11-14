---
title: ドキュメント表示
slug: text-document
---
# ドキュメント表示

長いテキストドキュメントを全画面で表示できます。ユーザは文章をスクロールして読むことができます。また、ボタンを付けてユーザのリアクションを取ることができます。表示中はボタンを押すまでキャンセルできないほか、他の画面操作のほとんどが行えません。コンテンツの README を読ませる、利用規約を読ませる、といった、ユーザに必ず読むべき内容を提示するのに使えます。

## テキストファイルをドキュメント表示

テキストファイルの中身をドキュメント表示できます。以下のように **INFOTEXT_FILE** メッセージを使います。第4引数以降は省略可能です。

- 第1引数：テキストファイルのパス
- 第2引数：タイトルラベル
- 第3引数：選択ボタンラベル カンマで区切る 例："Yes,No,Cancel"
- 第4引数（省略可）：文字スケール（デフォルト：1.0）
- 第5引数（省略可）：背景色 "RRGGBBAA" の16進数で 例：白=FFFFFFFF
- 第6引数（省略可）：文字色 同上

{{<message>}}
INFOTEXT_FILE|(filepath)|(titleLabel)|(buttonLabels)|(scale)|(BACKGROUNDCOLOR)|(TEXTCOLOR)
{{</message>}}

例： README.txt を表示する

{{<message>}}
INFOTEXT_FILE|README.txt|"read me"|OK,NO
{{</message>}}

![infotext](/images/infotext.png)

表示を開始したときに **INFOTEXT_EVENT_SHOW** メッセージが発行されます。

{{<message>}}
INFOTEXT_EVENT_SHOW
{{</message>}}

ユーザが選択ボタンラベルのいずれかを選択すると表示が終了します。そのとき、**INFOTEXT_EVENT_CLOSE** が押されたボタンのラベルとともに発行されます。

{{<message>}}
INFOTEXT_EVENT_CLOSE|(selecteDButtonLabel)
{{</message>}}

## 文字列をドキュメント表示

 ファイルではなくメッセージで表示する内容を指定して表示させることもできます。**INFOTEXT_FILE** の代わりに **INFOTEXT_STRING** メッセージを使います。第1引数に直接表示したい文字列を指定してください。第2引数以降の指定方法は **INFOTEXT_FILE** と全く同じです。

{{<message>}}
INFOTEXT_STRING|textbody|(titleLabel)|(buttonLabels)|(scale)|(BACKGROUNDCOLOR)|(TEXTCOLOR)
{{</message>}}

**INFOTEXT_FILE** と同様、表示開始時に **INFOTEXT_EVENT_SHOW**、終了時に **INFOTEXT_EVENT_CLOSE** が発行されます。
