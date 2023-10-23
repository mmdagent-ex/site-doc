---
title: ChatGPTと繋ぐ
slug: dialog-test-chatgpt
---
# ChatGPTと繋ぐ

{{< hint warning >}}
さきに[音声認識](../asr-setup)と[音声合成
](../tts-test)のセットアップを済ませてください。
{{< /hint >}}

ChatGPT を使って対話を行うシンプルなプログラムの例 `chatgpt.py` を以下に示します。このプログラムでは固定のプロンプトを使ってユーザの発話ごとに応答を ChatGPT から得ます。会話の履歴はトークン数の上限まで保持するようになっています。`openai.api_key` に OpenAI の API キーを設定して使ってください。

```python
# chatgpt.py
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

単体で起動して動作を確認したら、これを[Pythonでのつなぎ方](../dialog-test-python) と同じ方法でサブモジュールとして起動するよう設定します。

{{< mdf>}}
Plugin_AnyScript_Command=python.exe -u chatgpt.py
{{< / mdf >}}