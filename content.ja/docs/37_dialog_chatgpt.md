---
title: ChatGPTと繋ぐ
slug: dialog-test-chatgpt
---
# ChatGPTと繋ぐ

{{< hint warning >}}
さきに[音声認識](../asr-setup)と[音声合成
](../tts-test)のセットアップを済ませてください。
{{< /hint >}}

## シンプルな例

OpenAI の chat completion API を使って対話を行うシンプルなプログラムの例 `chatgpt.py` を以下に示します。

{{< hint warning >}}
以下の例では非常に簡単なプロンプトしか使っておらず、実際に会話できる内容は非常に限定的です。本ページでは chatGPT の使いこなしや工夫に関する部分は使っておりません。以下は MMDAgent-EX とつなぐサンプルプログラムとしてご参照ください。
{{< /hint >}}

以下は固定のプロンプトを使って OpenAI chat completion API で会話するシンプルなPythonスクリプトです。動作の概要は以下のとおりです。

- メッセージを標準入力から読み込みます。
- その中から音声認識結果が入ったテキストを抽出します。
- 音声認識結果に対するシステム応答を OpenAI API から得ます。
- 音声合成開始メッセージとして標準出力へ出力します。

このサンプルプログラムは OpenAI の Python ライブラリ バージョン 1.3.9 で動作を確認しています。

動作には OpenAI の API キーが必要です。 `YOUR_API_KEY` の部分を利用する API キーを入れて使ってください。

```python
# chatgpt.py
# tested on openai 1.3.9
#
import re
import openai
from openai import OpenAI

# Make sure to use UTF-8 at stdin/out
import sys
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

# Replace YOUR_API_KEY with your OpenAI API key
api_key = "YOUR_API_KEY"

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
chatgpt_messages = [{"role": "system", "content": chatgpt_prompt}]

# generate response
def generate_response(str):
    # debug output to stderr
    print(f"chatgpt: send: {str}", file=sys.stderr)

    # append the latest user utterance to message holder
    chatgpt_messages.append({"role": "user", "content": str})

    # call ChatGPT API to get answer
    client = OpenAI(api_key=api_key)
    try:
        completion = client.chat.completions.create(model=chatgpt_model, messages=chatgpt_messages)
    except openai.APIError as e:
        print(f"chatgpt: OpenAI API returned an API Error: {e}", file=sys.stderr)
        del chatgpt_messages[-1]
        return
    except openai.APIConnectionError as e:
        print(f"chatgpt: Failed to connect to OpenAI API: {e}", file=sys.stderr)
        del chatgpt_messages[-1]
        return
    except openai.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        print(f"chatgpt: OpenAI API request exceeded rate limit: {e}", file=sys.stderr)
        del chatgpt_messages[-1]
        return

    answer = completion.choices[0].message.content.strip()

    # debug output to stderr
    print(f"chatgpt: received: {answer}", file=sys.stderr)

    # append latest system response to message holder for next call
    chatgpt_messages.append({"role": "assistant", "content": answer})
    # purge oldest history when total token usage exceeds defined limit
    if completion.usage.total_tokens > chatgpt_message_token_max:
        chatgpt_messages.pop(1)
        chatgpt_messages.pop(1)
    return answer

# main
def main():
    while True:
        instr = input().strip()
        if not instr:
            break
        # Check if input line begins with "RECOG_EVENT_STOP"
        utterance = re.findall('^RECOG_EVENT_STOP\|(.*)$', instr)
        if utterance:
            # extract user utternace from message and generate response
            outstr = generate_response(utterance[0])
            # output message to utter the response
            print(f"SYNTH_START|0|mei_voice_normal|{outstr}")

if __name__ == "__main__":
    main()

```

これを[Pythonでのつなぎ方](../dialog-test-python) で説明した方法で、MMDAgent-EX からサブモジュールとして起動するよう設定します。たとえば Windows で Python の実行ファイルが "python.exe" の場合は以下のように書きます。

{{< mdf>}}
Plugin_AnyScript_Command=python.exe -u chatgpt.py
{{< / mdf >}}

macOS や Linux の場合も、コマンドラインと同じコマンドを記述してください。以下は例です。

{{< mdf>}}
Plugin_AnyScript_Command=python -u chatgpt.py
{{< / mdf >}}

MMDAgent-EX を起動し、ChatGPT と会話をしてみましょう。

## ストリーミング

OpenAI の chat completion にはストリーミングモードがあり、応答文をトークン単位で得ることができます。このストリーミングモードでは文全体の出力を待つことなく応答が開始されるため、これを用いることで応答遅延を低減することができます。

上記のプログラム例をストリーミングに対応させたバージョンを、以下に示します。以下、概要です。

- ストリーミングモードで接続し、サーバからの応答文字をトークン単位で順次受信します。
- 受信したトークンを結合しつつ、「。」「？」「！」が出てきたらそこを文の切れ目と判断して得られた部分の音声合成を開始します。
- 連続した文が出てくるため、「先に出した音声合成の終了イベントを待ってから次の文を開始する」という制御を行う必要があります。
- このため、ストリーム受信と音声合成制御はスレッド処理を使用して並列する必要があります。以下では受信を別スレッドで動作するようにしています。

```python
# chatgpt.py
# tested on openai 1.3.9
#
import re
import openai
from openai import OpenAI
import threading
import queue

# Make sure to use UTF-8 at stdin/out
import sys
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

# Replace YOUR_API_KEY with your OpenAI API key
#api_key = "YOUR_API_KEY"
api_key = "YOUR_API_KEY"

# ChatGPT model name to use
chatgpt_model="gpt-3.5-turbo"

# maximum number of tokens for purging dialogue context
chatgpt_message_history_max=20

# static prompt
chatgpt_prompt= '''
あなたの名前はジェネと言います。明るく中性的な20歳ぐらいの男の子で、会話好きのナイーブな少年です。
1回の発話を短くして短い会話を交わし合うスタイルで、明るい雰囲気で話してください。
'''
#######################################################

# queue to hold user input
input_queue = queue.Queue()

# queue to hold synthesis messages to be output
output_queue = queue.Queue()

# initialize message holder
chatgpt_messages = [{"role": "system", "content": chatgpt_prompt}]

# generate response and put them to output queue
def generate_response(str):
    # debug output to stderr
    print(f"chatgpt: send: {str}", file=sys.stderr)

    # append the latest user utterance to message holder
    chatgpt_messages.append({"role": "user", "content": str})

    # call ChatGPT API in streaming mode
    client = OpenAI(api_key=api_key)
    try:
        completion = client.chat.completions.create(model=chatgpt_model, messages=chatgpt_messages, stream=True)
    except openai.APIError as e:
        print(f"chatgpt: OpenAI API returned an API Error: {e}", file=sys.stderr)
        del chatgpt_messages[-1]
        return
    except openai.APIConnectionError as e:
        print(f"chatgpt: Failed to connect to OpenAI API: {e}", file=sys.stderr)
        del chatgpt_messages[-1]
        return
    except openai.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        print(f"chatgpt: OpenAI API request exceeded rate limit: {e}", file=sys.stderr)
        del chatgpt_messages[-1]
        return
    
    # receive stream
    total_answer = ""
    part = ""
    for chunk in completion:
        token = chunk.choices[0].delta.content
        if token:
            # append new token to message holder
            total_answer += token
            part += token.strip()
            # check if the current part sentence delimiter
            mm = re.match(r'(.*(、|！|。|？))(.*)', part)
            if mm:
                # a new sentence has been received
                sentence = mm.group(0)
                # put it to output queue
                output_queue.put(sentence)
                # reset new part
                part = mm.group(3)
    if part:
        output_queue.put(part)

    output_queue.put("***END***")

    # after all chunks have been received, debug output to stderr
    print(f"chatgpt: received: {total_answer}", file=sys.stderr)

    # append latest system response to message holder for next call
    chatgpt_messages.append({"role": "assistant", "content": total_answer})

    # purge oldest history when history length reaches limit
    if len(chatgpt_messages) > chatgpt_message_history_max * 2 + 1:
        chatgpt_messages.pop(1)
        chatgpt_messages.pop(1)

    return

# response generaion thread
def generate_response_run():
    while True:
        item = input_queue.get()
        generate_response(item)
        input_queue.task_done()

# wait till SYNTH_EVENT_STOP comes
def wait_till_synth_event_stop():
    while True:
        instr = input().strip()
        if not instr:
            break
        if re.findall('^SYNTH_EVENT_STOP', instr):
            break

# main
def main():
    thread1 = threading.Thread(target=generate_response_run)
    thread1.start()
    while True:
        # read from stdin
        instr = input().strip()
        if not instr:
            break
        # Check if input line begins with "RECOG_EVENT_STOP"
        utterance = re.findall('^RECOG_EVENT_STOP\|(.*)$', instr)
        if utterance:
            # put it to input queue for generation thread to make response in output_queue
            input_queue.put(utterance[0])
            # watch output queue and output it in turn, each waiting for corresponding SYNTH_EVENT_STOP
            while True:
                item = output_queue.get()
                if (item == "***END***"):
                    break
                print(f"SYNTH_START|0|mei_voice_normal|{item}")
                wait_till_synth_event_stop()
    thread1.join()

if __name__ == "__main__":
    main()

```
