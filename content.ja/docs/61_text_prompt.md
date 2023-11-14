---
title: プロンプトによる応答
slug: prompting
---
# プロンプトによる応答

音声対話システムでは音声やジェスチャによるコミュニケーションが主体ですが、選択肢を提示したり、ユーザがどれを望むかを明示的に選択させるような場合には、タッチ（マウスクリック）によるやりとりも有効なモーダルとなりえます。

MMDAgent-EX では、任意のメッセージダイアログを表示できます。単純にメッセージだけを表示して、外部タップで終了させることもできますし、選択肢をユーザに示していずれかの選択反応を受け取ることもできます。

これを使って、ユーザからの反応を得たり、選択肢で処理を分岐させるようなことができます。

## PROMPT_SHOW

プロンプトを出すには **PROMPT_SHOW** メッセージを発行します。`(main text)` が説明、`item text 0`, `item text 1`, ... が選択肢です。各テキストの指定には `""` や `\n` が使えます。

{{<message>}}
PROMPT_SHOW|(main text)|(item text 0)|(item text 1)|...
{{</message>}}

例：

{{<message>}}
PROMPT_SHOW|"main text"|item1|item2|item3
{{</message>}}

![prompt](/images/prompt.png)

**PROMPT_SHOW** を発行したとき、上記のようなプロンプトの表示が開始されます。プロンプトが表示されている間もシステムはバックグラウンドで動き続けます。

ユーザはいずれかの項目をキーもしくはタップで選択するか、ダイアログの外をタップしてキャンセルします。その後、プロンプトは消え、**PROMPT_EVENT_SELECTED** が選択されたアイテムの番号 (0～, キャンセルなら -1）とともに発行されます。

{{<message>}}
PROMPT_EVENT_SELECTED|(selected number or -1 for cancel)
{{</message>}}
