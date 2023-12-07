---
title: 音声対話をためす (Python)
slug: dialog-test-python
---
# 音声対話をためす (Python)

「[音声対話をためす (fst)](../dialog-test-fst)」では .fst スクリプトで簡易な音声対話を作る方法を説明しましたが、.fst はプリミティブな言語で、複雑な対話シナリオを記述するのに向いていません。高度な対話の制御は外部プログラムで行うべきです。

以下、このページでは、

- 音声認識結果のメッセージを標準入力から受け取り
- それに対応した応答メッセージを標準出力へ出力する

ような Python プログラムを作り、それによって外部から対話を制御できることを説明します。

{{< hint warning >}}
このページでは音声認識と音声合成を使います。まだの場合は、さきに[音声認識](../asr-setup)と[音声合成
](../tts-test)のセットアップを済ませてください。
{{< /hint >}}

## 準備

Python の実行環境を用意してください。以下の説明は バージョン 3.7 以降を想定しています。

「[音声対話をためす (fst)](../dialog-test-fst)」を既に試した人は、.fst に対話の部分が入っていると二重になるので、以下を始める前に該当部分を消しておきましょう。`main.fst` から以下の部分だけを残し、あとは削除してください。

{{<fst>}}
0 LOOP:
    <eps> STAGE|images/floor_green.png,images/back_white.png
    <eps> MODEL_ADD|0|gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0
{{</fst>}}

## 接続テスト

まずはダミーのプログラムで接続テストをしてみましょう。

### test.py を作る

以下は "`TEST|aaa`" という文字列を1秒ごとに標準出力へ出力する Python プログラムです。これを
`example` の下に作成して `test.py` というファイル名で保存してください。

```python
#### example/test.py
import time
while(1):
    print("TEST|aaa")
    time.sleep(1)
```

保存したらいちどターミナル（あるいはコマンドプロンプト）で動作を確かめます。（停止するには `CTRL+C` を押します。）

```shell
% python example/test.py
TEST|aaa
TEST|aaa
...
```

### test.py を起動するコマンドを .mdf でセットする

この test.py を MMDAgent-EX のサブモジュールとして起動するよう設定してみます。サブモジュール起動コマンドは .mdf ファイルで指定します。`example/main.mdf` をテキストエディタで開き、以下の1行を末尾に新たに追加してください。

{{< mdf>}}
Plugin_AnyScript_Command=python -u test.py
{{< / mdf >}}

`=` から右が起動コマンドです。シェルから起動するときと同じコマンドをそのまま記述してください。また Python では `-u` オプションを付けます。

ファイルを保存したら、その .mdf を指定してMMDAgent-EX を起動します。起動後、内部で自動的に指定したコマンドがサブプロセスとして起動され、MMDAgent-EXのメッセージストリームと接続されます。起動後、`d` キーを押してログを表示し、1秒おきに `TEST|aaa` が出力されているのを確認できれば接続成功です。次へ進んでください。

```shell
./Release/MMDAgent-EX.exe ./example/main.mdf
```

うまく動かない場合は以下の対処を試してみてください。

{{< details "うまく動かない場合のチェックポイント" close >}}
### 実行バイナリ

起動コマンド（上記の場合 `python -u test.py`）においてコマンドは通常のコマンドプロンプト（ターミナル）とほぼ同様に解釈されます。

- パス無しの場合、設定されている実行パスに従って実行コマンドが探され、実行されます。
- フルパスで指定した場合、その指定されたパスのファイルを実行します。

コマンドがうまく指定できない場合は実行ファイルをフルパスで指定してみてください。

### カレントディレクトリ

実行時のカレントディレクトリは、その .mdf の置いてあるフォルダです。ファイルパスを与えるプログラムでは注意してください。

### 文字コード

テキストは UTF-8 でやりとりします。Python スクリプトの標準入出力が UTF-8 になるよう注意してください。

### -u オプション

標準出力のバッファリングが有効だとメッセージを出力しても MMDAgent-EX に即座に出力されないことがあります。できるかぎり標準出力のバッファリングを無効にしてください。Python では `-u` オプションをつけることで無効化できます。

その他、うまく動かない場合は[詳しい説明](../submodule/)を参考にしてください。
{{< /details >}}

## テキスト対話プログラムの例

次の例に進みます。「こんにちは。」という入力に対して「よろしくお願いします！」を返す Python のサンプルプログラム `example/sample-dialog.py` を試してみます。これは以下のような動作を行うプログラムです。

- 標準入力（＝MMDAgent-EX のメッセージストリーム）からテキストを読み込み続ける
- 認識結果のメッセージ (`RECOG_EVENT_STOP`) があれば認識結果部分を抽出し、関数 `generate_response()` へ渡す
- `generate_response()` は認識文に対して応答を返す。ここでは「こんにちは。」に「よろしくお願いします！」と返し、それ以外は「わかりません。」と返すだけのものになっている。
- 得られた応答文を音声合成メッセージ (`SYNTH_START`) として標準出力（＝メッセージストリーム）へ出力する

```python
#### example/sample-dialog.py
import re

# 入出力の文字列を UTF-8 にする
import sys
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

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

先ほどの test.py と同じように、このプログラムをサブモジュールとして設定しましょう。.mdf に以下のように記述します（さきほどのテストコマンドを上書きしてください）。

{{< mdf>}}
Plugin_AnyScript_Command=python -u sample-dialog.py
{{< / mdf >}}

設定後に MMDAgent-EX を起動し、ためしに「こんにちは。」と話してみてください。

```shell
./Release/MMDAgent-EX.exe ./example/main.mdf
```

## 拡張

出力テキストはすべてメッセージとして MMDAgent-EX へ送り込まれるので、例えば `MOTION_ADD` メッセージを送ればモーションが再生できる、といったように、様々な制御をスクリプトから送り込むことができます。
