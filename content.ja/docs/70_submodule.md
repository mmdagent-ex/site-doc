---
title: サブモジュールの組み込み
slug: submodule
---
{{< hint info >}}
サブモジュール組み込み機能は Plugin_AnyScript が提供しています。利用時はこのプラグインが有効になっているか確かめてください。
{{< /hint >}}

# サブモジュールの組み込み

Python スクリプトを含む任意のアプリケーションをサブモジュールとして MMDAgent-EX に組み込んでMMDAgent-EX の能力を拡張することができます。アプリケーションは子プロセスとして MMDAgent-EX 起動時に起動され、終了と同時に終了します。[音声対話をためす (Python)](../dialog-test-python)のページ、および[ChatGPTを組み込む例](../dialog-test-chatgpt)で用いたのはこの方法です。

ここではサブモジュールとして組み込む方法について概説します。

## Plugin_AnyScript

サブモジュールの組み込みは Plugin_AnyScript で実現されています。
Plugin_AnyScript プラグインはアプリケーションを子プロセスとして起動・接続するプラグインです。Plugin_AnyScript によって起動された子プロセスは、標準入出力がMMDAgent-EX のメッセージキューと直接接続されます：

- 子プロセスの標準出力は、そのままメッセージとして MMDAgent-EX へ発行する
- MMDAgnet-EX から発行されるメッセージは、全て子プロセスの標準入力に与えられる

[音声対話をためす (Python)](../dialog-test-python)で示したのは対話を制御する使い方でしたが、そのほかにも、

- **他の音声合成エンジンを使う**: プロセスは `SYNTH_START` メッセージを標準入力から受け取り、音声合成を行ってオーディオ出力する（デフォルトの Plugin_Open_JTalk は disable する）
- **他の音声認識エンジンを使う**：プロセスは音声認識を行い、その結果を `RECOG_EVENT_STOP|認識結果` の形で標準出力へ出力する（デフォルトの Plugin_Julius は disable する）
- カメラを追加する：カメラの検出結果に従って `MOTION_ADD` メッセージを標準出力へ送ることで、カメラに反応するモーションを挟み込む

といったような拡張が可能です。

{{< hint warning >}}
### プログラム作成上の注意

アプリケーションやスクリプトをサブモジュールとして組み込む際は、必ずそのプロセスの **標準出力のバッファリングを OFF にしてください**。バッファリングが ON になっていると、出力したメッセージが即座に MMDAgent-EX に吐き出されず、処理が行われなかったり遅延したりします。

Python スクリプトの場合、起動時オプションに `-u` をつけることでバッファリングをOFFにできます。それ以外の場合は、１行出力するごとに明示的に出力をフラッシュするようプログラムを作成してください。
{{< /hint >}}

## サブモジュール登録

サブモジュールは .mdf で登録します。サブモジュールとして起動するコマンドを以下のように指定します。なお、実行時のカレントディレクトリは、コンテンツのディレクトリではなく、MMDAgent-EX.exe の置いてあるフォルダである点に注意してください。`=` から行末までの全てが起動コマンドとして使われるので、空白があっても問題ありません。

{{<mdf>}}
Plugin_AnyScript_Command=C:\Program Files\Python310\python.exe -u test.py
{{</mdf>}}

複数のモジュールを指定する場合は以下のように書いてください。最大で10個まで指定できます。

{{<mdf>}}
Plugin_AnyScript_Command1=...
Plugin_AnyScript_Command2=...
{{</mdf>}}

## 起動時の動作

サブモジュールとして指定されたアプリケーションは、MMDAgent-EX 起動時に MMDAgent-EX の子プロセスとして起動されます。また、MMDAgent-EX の終了と同時に終了します。

## 標準入力に送られるメッセージの選択

サブモジュールの標準入力には、MMDAgent-EX 内を流れるすべてのメッセージが送られます。送られるメッセージの種類の選択等はできません。モジュール側で必要に応じてメッセージを取捨選択・処理するよう処理を記述してください。

なお、デフォルトでは標準入力で受け取れるのは「メッセージ」のみですが、加えてすべての動作ログまで受け取りたい場合は、以下を .mdf に指定してください。

{{<mdf>}}
Plugin_AnyScript_AllLog=true
{{</mdf>}}

## 動作例

以下は天気予報を取得して答えるモジュールの作成例です。音声認識結果の `RECOG_EVENT_STOP` メッセージは MMDAgent-EX 本体だけでなく全てのモジュールにも送られるので、仮に .fst スクリプトが「天気」という発話に答えられない場合でも、このようにサブモジュールが応答するよう作ることができます。

```python
def query_weather():
    # 天気予報を取得する
    # 取得した予報をもとに応答文を作る
    return(response)

if __name__ == "__main__":
    while True:
        input_line = input().strip()
        if input_line.startswith("RECOG_EVENT_STOP|天気"):
            response = query_weather()
            print(f"SYNTH_START|0|mei_voice_normal|{response}")
```
