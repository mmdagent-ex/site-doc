---
title: 音声対話をためす (Python)
slug: dialog-test-python
---
# 音声対話をためす (Python)

「[音声対話をためす (fst)](../dialog-test-fst)」では MMDAgent-EX の .fst スクリプトだけで簡易な音声対話機能を追加する方法を紹介しました。ただし、.fst はインタラクション記述のための仕組みであり、複雑な対話を記述するには向いていません。

MMDAgent-EX は様々な外部プログラムと連係動作できます。ここでは例として、Python で構築したテキスト対話プログラムを MMDAgent-EX と接続する方法を簡単な例をもとに説明します。

## 準備

.fst に対話の部分が入っていると二重になるので消しておきましょう。

{{<fst>}}0 LOOP:
    &lt;eps&gt; STAGE|images/floor_green.png,images/back_white.png
    &lt;eps&gt; MODEL_ADD|0|gene/gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    &lt;eps&gt; CAMERA|0,15.25,0|4.5,0,0|22.4|27.0
{{</fst>}}

## テキスト対話プログラムの例

以下は「こんにちは。」という入力に対して「よろしくお願いします！」を返すサンプルプログラムです。`generate_reponse` が入力に対して応答を生成する関数です。現在は単純な実装になっています。入力無しで Enter だけ押すと終了します。

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

このプログラムはメッセージを標準入力から受け取ります。また、標準出力は MMDAgent-EX にメッセージとして投げ込まれます。なので、以下のように入力されるメッセージに認識結果 (`RECOG_EVENT_STOP`) が含まれていたときに、そこから認識文章を抽出して応答を生成し、結果を音声合成メッセージ (`SYNTH_START`) として出力するようにします。

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
