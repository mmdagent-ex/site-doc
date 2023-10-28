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

「[音声対話をためす (fst)](../dialog-test-fst)」を実行した人は、.fst に対話の部分が入っていると二重になるので、以下の手順を始める前に消しておきましょう。`main.fst` から以下の冒頭部分だけ残して、あとは削除してください。

{{<fst>}}0 LOOP:
    &lt;eps&gt; STAGE|images/floor_green.png,images/back_white.png
    &lt;eps&gt; MODEL_ADD|0|gene/gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    &lt;eps&gt; CAMERA|0,15.25,0|4.5,0,0|22.4|27.0
{{</fst>}}

## テキスト対話プログラムの例

以下は「こんにちは。」という入力に対して「よろしくお願いします！」を返す Python のサンプルプログラムです。

- 関数 `generate_reponse` が、入力テキストに対して応答を返す対話のメインとなる関数です。現在は「こんにちは。」にだけ「よろしくお願いします！」と返し、それ以外は「わかりません。」と返すものになっています。
- 入力無しで Enter だけ押すと終了します。

```python
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

実行して動作を確かめてください。

```shell
$ python test.py
何ですか？　　　　←キーボード入力
わかりません。
こんにちは。　　　←キーボード入力
よろしくお願いします！
```

## MMDAgent-EX 向けに変更

これを MMDAgent-EX のサブモジュールにしてみましょう。サブモジュールとして実行中、Pythonスクリプトの標準入出力と MMDAgent-EX のキューは以下のように接続されます。

- MMDAgent-EX に流れる全てのメッセージが、このスクリプトの標準入力へ逐次入力されます。
- 標準出力へ出したテキストは、そのまま MMDAgent-EX メッセージとして発行されます。

以下のようにプログラムを変更してみましょう。

- 入力メッセージに認識結果 (`RECOG_EVENT_STOP`) が含まれていたとき、そこから認識文を抽出
- 応答を生成
- 生成した応答テキストを音声合成メッセージ (`SYNTH_START`) として出力

```python
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

このプログラムをサブモジュールとして起動します。`Plugin_AnyScript` を使います。.mdf に以下のように、サブモジュールとして起動するコマンドを記述してください。

{{< hint warning >}}
サブモジュールに Python を指定する場合、バッファリングが有効になっていると出力したメッセージがすぐに MMDAgent-EX に流れません。以下のように `-u` オプションを必ずつけて出力のバッファリングを無効化してください。
{{< /hint >}}

{{< mdf>}}
Plugin_AnyScript_Command=python.exe -u test.py
{{< / mdf >}}

設定後に MMDAgent-EX を起動すれば、起動時に指定したプログラムが起動します。ためしに「こんにちは。」と話してみてください。

## 拡張

出力テキストはすべてメッセージとして MMDAgent-EX へ送り込まれるので、例えば `MOTION_ADD` メッセージを送ればモーションが再生できる、といったように、様々な制御をスクリプトから送り込むことができます。