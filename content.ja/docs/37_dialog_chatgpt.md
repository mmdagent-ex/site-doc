---
title: ChatGPTと繋ぐ
slug: dialog-test-chatgpt
---
# ChatGPTと繋ぐ

{{< hint warning >}}
さきに[音声認識](../asr-setup)と[音声合成
](../tts-test)のセットアップを済ませてください。
{{< /hint >}}

MMDAgent-EX を対話システムのフロントエンドとして利用することができます。ここでは OpenAI の GPT モデルを使った対話システムを題材に、MMDAgent-EX へ対話モジュールをサブモジュールとして繋ぐ簡単な作例をサンプルと共に紹介します。

## LLMベース対話文生成を MMDAgent-EX に繋ぐ

OpenAI の chat completion API を使って対話を行うシンプルなプログラムを作成し、それを MMDAgent-EX のサブモジュールとして起動する手順を以下に示します。

{{< hint warning >}}
以下の例では非常に簡単なプロンプトしか使っておらず、実際に会話できる内容は非常に限定的です。本ページでは chatGPT の使いこなしや工夫に関する部分は使っておりません。以下は MMDAgent-EX とつなぐサンプルプログラムとしてご参照ください。
{{< /hint >}}

以下の `chatgpt.py` は、OpenAI chat completion API で会話するシンプルなPythonスクリプトです。最後の `main()` の部分以外は通常のテキストチャットのコードです。`main()` ではその入出力を MMDAgent-EX のサブモジュールとして動かすために以下のような動作を行うよう実装されています。

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

## ストリーミングへの拡張

LLMベースの対話システムでは応答文の生成に数秒から数十秒かかるものもあり、その応答遅延が問題となります。OpenAI の chat completion をはじめとしたLLMにはストリーミングモードを提供しており、生成文を溜めずにトークン単位でストリームとして受信することができます。このストリーミングモードを用いて、生成テキストを漸次的に受け取りながら適当な音声合成単位の区切りを検出し、区切りが見つかった区間から生成終了を待たず逐次的に音声合成を行うことで、応答開始までの遅延を低減することができます。この方法は LLM 対話における遅延低減の方法の一つとして広く試みられています。

上記のプログラム例をストリーミングに対応させたバージョンを以下に示します。区切りの判定方法は速さと音声合成精度のトレードオフがあり、さまざまな手法がありますが、ここでは単純に「句読点記号が出てきたら区切る」方法を使います。また、再生において合成音声が順番に重なりなく再生するための制御が必要であり、これが文生成の受信速度と異なるため、スレッドやキューを用いたタイミング制御が必要になります。以下、動作の概要です。

- ストリーミングモードで接続し、サーバからの応答文字をトークン単位で順次受信します。
- 受信したトークンを結合しつつ、「。」「？」「！」が出てきたらそこを文の切れ目と判断して得られた部分の音声合成を開始します。
- 連続した文が出てくるため、「先に出した音声合成の終了イベントを待ってから次の文を開始する」という制御を行う必要があります。
- このため、ストリーム受信と音声合成制御はスレッド処理を使用して並列する必要があります。以下では受信を別スレッドで動作するようにしています。

```python
# chatgpt_streaming.py
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

## 感情推定およびアクションの追加

発話文に合わせてCGアバターが感情やしぐさ等のアクションを表出することでより効果的な対話システムとなります。ここでは例として、生成文に感情ラベルを付与するとともに、その感情に従って発話と同時にCGアバターがアクションを行うよう発展させてみましょう。

1. 発話文に対する感情の推定を行います。発話に伴う感情やアクションの推定は様々な方法がありますが、ここでは簡単に試すために、ChatGPT へ、文生成と同時にの文に付随する感情ラベルも同時に推定するようプロンプトに記述してみます。感情セットとして、以下の種類の感情を番号で付けて指定してみます。これによって例えば「1 こんにちは！」のように ChatGPT から応答させます。

```python
chatgpt_prompt= '''
あなたの名前はジェネと言います。明るく中性的な20歳ぐらいの男の子で、会話好きのナイーブな少年です。
1回の発話は1文だけで、短く、明るい雰囲気で話してくださ

また、1文ごとに適切な感情を以下の感情リストから選び、文の直前に番号と空白をつけて話してください。

感情リスト:
1 joy,happy
2 amusement
3 smile,calm
4 surprise
5 disgust
6 contempt
7 frustration
8 anger
9 sad
'''
```

2. 付与された感情ラベルとCGアバターのマッピングを指定します。各モデルの `motion` フォルダ以下にサンプルモーションがあるのでそれを指定します。ここでは上記の感情番号に合わせて以下のように定義することにします。

```python
emotion_list = [
    "gene/motion/00_normal.vmd",
    "gene/motion/01_happy.vmd",      # joy,happy
    "gene/motion/02_laugh.vmd",      # amusement
    "gene/motion/03_smile.vmd",      # smile,calm
    "gene/motion/08_surprise.vmd",   # surprise
    "gene/motion/21_disgust.vmd",    # disgust
    "gene/motion/25_sharpeyessuspicion.vmd", # contempt
    "gene/motion/32_frustrated.vmd", # frustrated
    "gene/motion/33_angry.vmd",      # anger
    "gene/motion/34_sad.vmd",        # sad
]
```

3. main の処理部で、もしChatGPTの出力結果の冒頭に数字がある場合、対応するモーションを同時に生成するようにします。上記の例の出力部分を以下のようにします。

```python
        # Check if input line begins with "RECOG_EVENT_STOP"
        utterance = re.findall('^RECOG_EVENT_STOP\|(.*)$', instr)
        if utterance:
            # extract user utternace from message and generate response
            outstr = generate_response(utterance[0])
            # extract emotion
            ss = re.findall('^.*(\w+) +(.*)$', outstr)
            # output message to utter the response
            if ss:
                # action
                emotion_id = int(ss[0][0])
                outstr = ss[0][1]
                print(f"MOTION_ADD|0|action|{emotion_list[emotion_id]}|PART|ONCE")
            print(f"SYNTH_START|0|mei_voice_normal|{outstr}")
```

## 音声認識・音声合成を Python で行い MMDAgent-EX をフロントエンドとする

以上の例は「MMDAgent-EX をメインモジュールとして対話部分を組み込む」形で説明しましたが、逆に 「Python 側をメインモジュールと考えて、MMDAgent-EX は使役されるフロントエンド・インタフェース」という考え方での統合も可能です。以下、典型的なケースを示します。

- 音声認識・応答文生成を Python で行い、結果の出力テキストや動作コマンドをメッセージで送って MMDAgent-EX のCGアバターに話させる
- 音声合成まで Python で行い、[合成音声データを流し込む](../remote-speech/)ことで MMDAgent-EX のCGアバターに話させる
- 音声認識・合成・再生まで全部 Python で行い、MMDAgent-EX へは[リップシンク情報を送り込んで口パクさせ](../remote-speech) たりモーション起動を行うコマンドを送信するなどして、動きのみコントロールする

応用や目的にあわせて自由にお使いください。
