---
title: ブラウザを使った動作テスト環境
slug: message-test
---
# ブラウザを使った動作テスト環境

開発をしやすくするために、**Webブラウザ経由でメッセージを簡単に試してみる方法が提供されています**。MMDAgent-EX が起動した状態で、同じマシンでWebブラウザで http://localhost:50000/ を開きます。

- <a href="http://localhost:50000" target="_blank">http://localhost:50000</a> （←クリックで別ウィンドウで開きます）

ブラウザが実行中の MMDAgent-EX と接続して以下のようなページが開きます。

<img alt="test message page snapshot" src="/images/test_message.png"/>

このテキストボックスにメッセージを入力して Send ボタンを押すことで、動作中の MMDAgent-EX へ任意のメッセージを投げ込めます。試しに以下の[プロンプト表示メッセージ](../prompting)を入れてみましょう。

```text
PROMPT_SHOW|"This is test"|Yes|OK|"I got it"
```

Send ボタンを押して以下のようなプロンプトダイアログが出たらOKです。

<img alt="test message prompt snapshot" src="/images/test_message_prompt.png"/>

このように、http://localhost:50000/ に任意のメッセージを動作中の MMDAgent-EX に投げ入れて動作を確認することができますので活用してください。

## 設定

ポート番号は .mdf で変更できます。またこの機能を無効にすることもできます。

{{<mdf>}}
# set to false to disable the internal http server feature
http_server=true

# set port number to listen
http_server_port=50000
{{</mdf>}}