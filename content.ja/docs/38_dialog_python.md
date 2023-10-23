---
title: 音声対話をためす (Python)
slug: dialog-test-python
---
# 音声対話をためす (Python)

「[音声対話をためす (fst)](../dialog-test-fst)」では .fst スクリプトだけで簡易な音声対話を作る方法を説明しました。ただし、.fst はインタラクション記述のための仕組みであり、複雑な対話を記述するには向いていません。

MMDAgent-EX は様々な外部プログラムと連係動作できます。ここでは例として、Python で構築したテキスト対話プログラムを MMDAgent-EX と接続する方法を、簡単な例をもとに説明します。

## 準備

「[音声対話をためす (fst)](../dialog-test-fst)」を実行した人は、.fst に対話の部分が入っていると二重になるので、以下の手順を始める前に消しておきましょう。`main.fst` から以下の冒頭部分だけ残して、あとは削除してください。

{{<fst>}}0 LOOP:
    &lt;eps&gt; STAGE|images/floor_green.png,images/back_white.png
    &lt;eps&gt; MODEL_ADD|0|gene/gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    &lt;eps&gt; CAMERA|0,15.25,0|4.5,0,0|22.4|27.0
{{</fst>}}

## テキスト対話プログラムの例

以下は「こんにちは。」という入力に対して「よろしくお願いします！」を返す Python のサンプルプログラムです。入力テキストに対して応答を生成する部分を関数 `generate_reponse` としています。現在は「こんにちは。」に対応するだけの単純な実装になっています。入力無しで Enter だけ押すと終了します。

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

このプログラムを、プラグインを使って MMDAgent-EX のサブモジュールとして起動するよう調整します。サブモジュールの標準入出力は MMDAgent-EX と結合され、全てのメッセージが標準入力に送り込まれ、その標準出力は MMDAgent-EX にそのままメッセージとして投げ込まれます。以下のようにプログラムを変更してみましょう。入力されるメッセージに認識結果 (`RECOG_EVENT_STOP`) が含まれていたとき、そこから認識文を抽出して、応答を生成した結果を音声合成メッセージ (`SYNTH_START`) として出力するよう変更します。

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

サブモジュールが出力するテキストはすべてメッセージとして MMDAgent-EX へ送り込ませられます。 `MOTION_ADD` メッセージを送ればモーションが再生できます。

## ChatGPT を使う例

ChatGPT を使って対話を行うシンプルなプログラムの例を以下に示します。このプログラムでは固定のプロンプトを使ってユーザの発話ごとに応答を ChatGPT から得ます。会話の履歴はトークン数の上限まで保持するようになっています。`openai.api_key` に OpenAI の API キーを設定して使ってください。

```python
import openai

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = "YOUR_API_KEY"

# ChatGPT model name to use
chatgpt_model="gpt-3.5-turbo"
# maximum number of tokens for purging dialogue context
chatgpt_message_token_max=3000

# static prompt
chatgpt_prompt= '''
あなたの名前はジェネと言います。明るく中性的な20歳ぐらいの男の子で、会話好きのナイーブな少年です。
1回の発話は1文だけで、明るい雰囲気で話してください。
'''
#######################################################

# initialize message holder
chatgpt_messages = [{"role": "system", "content": chatgpt_prompt}];

# generate response
def generate_response(str):
    # append latest user utterance to message holder
    chatgpt_messages.append({"role": "user", "content": str})
    # call ChatGPT API
    response = openai.ChatCompletion.create(model=chatgpt_model, messages=chatgpt_messages)
    # get answer string from response
    answer = response["choices"][0]["message"]["content"].strip()
    print(answer)
    # append latest system response to message holder for next call
    chatgpt_messages.append({"role": "assistant", "content": answer})
    # purge oldest history when total token usage exceeds defined limit
    if response["usage"]["total_tokens"] > chatgpt_message_token_max:
        chatgpt_messages.pop(1)
        chatgpt_messages.pop(1)
    return answer

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