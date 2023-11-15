---
title: 音声対話をためす (Python)
slug: dialog-test-python
---
# 音声対話をためす (Python)

「[音声対話をためす (fst)](../dialog-test-fst)」では .fst スクリプトだけで簡易な音声対話を作る方法を説明しました。ただし、.fst はインタラクション記述のための仕組みであり、複雑な対話を記述するには向いていません。

MMDAgent-EX は様々な外部プログラムと連係動作できます。ここでは例として、Python で構築したテキスト対話プログラムをサブモジュールとして MMDAgent-EX に組み込む方法を、簡単な例をもとに説明します。

{{< hint warning >}}
さきに[音声認識](../asr-setup)と[音声合成
](../tts-test)のセットアップを済ませてください。
{{< /hint >}}

## 準備

マシンに Python の実行環境を用意してください。ここでは基本的な機能しか使わないのでバージョン等は問いません。

また、「[音声対話をためす (fst)](../dialog-test-fst)」を実行した人は、.fst に対話の部分が入っていると二重になるので、以下の手順を始める前に該当部分を消しておきましょう。`main.fst` から以下の部分だけを残し、あとは削除してください。

{{<fst>}}
0 LOOP:
    <eps> STAGE|images/floor_green.png,images/back_white.png
    <eps> MODEL_ADD|0|gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0
{{</fst>}}

## 事前テスト

まずは確認のため、簡単な Python スクリプトを MMDAgent-EX に組み込むテストをしてみましょう。以下のプログラムを `example` の下に `test.py` として保存してください。これは "`TEST|aaa`" という文字列を1秒ごとに出力するプログラムです。

```python
#### example/test.py
import time
while(1):
    print("TEST|aaa")
    time.sleep(1)
```

念のためターミナル（あるいはコマンドプロンプト）で動作を確かめてみましょう。（停止するには `CTRL+C` を押します。）

```shell
% python example/test.py
TEST|aaa
TEST|aaa
...
```

確認できたら、このプログラムを MMDAgent-EX のサブモジュールとして起動するよう設定します。`example/main.mdf` を開き、以下の1行を追加してください。（`python` の部分は自分の環境に合わせて適宜変更してください。）

{{< mdf>}}
Plugin_AnyScript_Command=python -u test.py
{{< / mdf >}}

ファイルを保存して、MMDAgent-EX を起動してください。起動後、ログに1秒おきに `TEST|aaa` が出力されれば接続成功です。次へ進んでください。うまく動かない場合は[詳しい説明](../submodule/)を参考にしてください。

```shell
./Release/MMDAgent-EX.exe ./example/main.mdf
```


## テキスト対話プログラムの例

以下は「こんにちは。」という入力に対して「よろしくお願いします！」を返す Python のサンプルプログラム `example/sample-dialog.py`です。

- 関数 `generate_reponse` が、入力テキストに対して応答を返す対話のメインとなる関数です。現在は「こんにちは。」にだけ「よろしくお願いします！」と返し、それ以外は「わかりません。」と返すものになっています。
- 入力無しで Enter だけ押すと終了します。

```python
#### example/sample-dialog.py
# 応答を返す
def generate_response(str):
    if str == "こんにちは。":
        return "よろしくお願いします！"
    return "わかりません。"

# メイン
def main():
    while True:
        instr = input().strip()
        if not instr:   # 入力が無ければ終了
            break
        outstr = generate_response(instr)
        print(outstr)

if __name__ == "__main__":
    main()
```

これを `example` フォルダ以下に作成してください。キーボードから適当な文を入力して動作を確かめてみましょう。

```shell
$ python example/sample-dialog.py
何ですか？　　　　←キーボード入力
わかりません。
こんにちは。　　　←キーボード入力
よろしくお願いします！
```

## MMDAgent-EX 向けに変更

MMDAgent-EX のサブモジュールとして動作するとき、この Pythonスクリプトの標準入出力と MMDAgent-EX のキューは、以下のように接続されます。

- MMDAgent-EX に流れる全てのメッセージが、このスクリプトの標準入力へ逐次入力される
- 標準出力へ出したテキストは、そのまま MMDAgent-EX メッセージとして発行される

メッセージのフォーマットに合わせて、さきほどの `example/sample-dialog.py` を以下のように変更してみます。

- 入力メッセージに認識結果 (`RECOG_EVENT_STOP`) が含まれていたとき、そこから認識文を抽出
- 応答を生成
- 生成した応答テキストを音声合成メッセージ (`SYNTH_START`) として出力

```python
#### example/sample-dialog.py
import re
# 応答を返す
def generate_response(str):
    if str == "こんにちは。":
        return "よろしくお願いします！"
    return "わかりません。"

# メイン
def main():
    while True:
        instr = input().strip()
        if not instr:
            break
        # 入力が RECOG_EVENT_STOP かどうか調べる
        utterance = re.findall('^RECOG_EVENT_STOP\|(.*)$', instr)
        if utterance:
            # 発話内容をメッセージから抽出して応答文を生成
            outstr = generate_response(utterance[0])
            # 生成された応答文を SYNTH_START メッセージとして出力
            print(f"SYNTH_START|0|mei_voice_normal|{outstr}")

if __name__ == "__main__":
    main()
```

## サブモジュールとして実行

このプログラムをサブモジュールとして起動してみましょう。.mdf に以下のように、サブモジュールとして起動するコマンドを記述します（さきほどのテストコマンドを上書きしてください）。

パスの指定に注意してください。子プロセスのカレントディレクトリはその .mdf のあるディレクトリ（ここでは `./example`）になるので、ここでは `sample-dialog.py` となります。

{{< hint warning >}}
サブモジュールに Python を指定する場合、バッファリングが有効になっていると出力したメッセージがすぐに MMDAgent-EX に流れません。以下のように `-u` オプションを必ずつけて出力のバッファリングを無効化してください。
{{< /hint >}}

{{< mdf>}}
Plugin_AnyScript_Command=python -u sample-dialog.py
{{< / mdf >}}

設定後に MMDAgent-EX を起動すれば、起動時に指定したプログラムが起動します。ためしに「こんにちは。」と話してみてください。

```shell
./Release/MMDAgent-EX.exe ./example/main.mdf
```

## 拡張

出力テキストはすべてメッセージとして MMDAgent-EX へ送り込まれるので、例えば `MOTION_ADD` メッセージを送ればモーションが再生できる、といったように、様々な制御をスクリプトから送り込むことができます。