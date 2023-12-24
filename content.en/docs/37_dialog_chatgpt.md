---
title: Connecting with ChatGPT
slug: dialog-test-chatgpt
---
# Connect with ChatGPT

{{< hint warning >}}
Please complete the setup for [voice recognition](../asr-setup) and [speech synthesis
](../tts-test) first.
{{< /hint >}}


MMDAgent-EX can be used as a frontend for dialogue systems. Here, we introduce a simple example that connects OpenAI's GPT model.

## Connecting LLM-Based Dialogue Generation to MMDAgent-EX

The following steps show a simple program that conducts dialogues using OpenAI's chat completion API, and how to start it as a submodule of MMDAgent-EX.

{{< hint warning >}}
The examples provided here use very simple prompts, so the scope of the conversation is quite limited. This page does not cover how to use and optimize chatGPT. The following sample is only for demonstrating integration with MMDAgent-EX.
{{< /hint >}}

The `chatgpt.py` below is a simple Python script for making conversation with the OpenAI chat completion API. Except for the last main() part, it is a standard text chat code. In main(), it is implemented to perform the following actions to operate as a submodule of MMDAgent-EX.

- It reads MMDAgent-EX messages from standard input.
- It filters out a message containing speech recognition result.
- Using the OpenAI API, it generates response to the input.
- It writes a message to standard output to tell MMDAgent-EX to start speech synthesis.

This sample program was tested with version 1.3.9 of OpenAI's Python library.

To operate, you need an API key from OpenAI. Please replace `YOUR_API_KEY` with your API key.

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
Your name is Gene. You're a bright and gender-neutral young person around the age of 20, who enjoys conversations and is rather naive.
Please speak in a cheerful tone and keep your remarks to one sentence at a time.
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
            print(f"SYNTH_START|0|slt_voice_normal|{outstr}")

if __name__ == "__main__":
    main()

```

You can set this up to run as a submodule from MMDAgent-EX using the method explained in [Connecting with Python](../dialog-test-python). For example, if the executable file for Python on Windows is "python.exe", you would write it as follows:

{{< mdf>}}
Plugin_AnyScript_Command=python.exe -u chatgpt.py
{{< / mdf >}}

For macOS or Linux, write the same command as you would on the command line. Here is an example:

{{< mdf>}}
Plugin_AnyScript_Command=python -u chatgpt.py
{{< / mdf >}}

Start up MMDAgent-EX and try conversing with ChatGPT.

## Extension to Streaming

In LLM-based dialogue systems, generating response sentences can take from a few seconds to tens of seconds, and this response delay can be problematic. Some LLMs, including OpenAI's chat completion, offer a streaming mode, allowing the reception of generated text as a stream on a token-by-token basis, without accumulating the entire response.

By using this streaming mode to progressively receive generated text and detect appropriate breaks for voice synthesis, it's possible to reduce the delay before starting the response. This method is widely tried as a way to reduce delays in LLM dialogues.

Below is a modified version of the example above that uses streaming mode. There are various approaches about how to efficiently find sentence breaks in a course of streamed sentences, but here we simply use the method of "breaking at punctuation marks".

The synthesized voices should be played in order without overlapping, so threads or queues are required for synthesis timing control. Here's an overview of its operation:

- Connect in streaming mode and sequentially receive response characters from the server in token units.
- As the received tokens are combined, voice synthesis of the obtained parts begins when "。", "？", or "！" appears, judging that as the end of the sentence.
- Since continuous sentences come out, you need to control "waiting for the end event of the voice synthesis that was put out first before starting the next sentence".
- Therefore, stream reception and voice synthesis control need to be parallelized using thread processing. The following makes the reception operate in a separate thread.

```python
# chatgpt_stream.py --- streaming version
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
api_key = "YOUR_API_KEY"

# ChatGPT model name to use
chatgpt_model="gpt-3.5-turbo"

# maximum number of tokens for purging dialogue context
chatgpt_message_history_max=20

# static prompt
chatgpt_prompt= '''
Your name is Gene. You're a bright, gender-neutral boy, around 20 years old, a naive boy who loves to converse.
Have conversations in a bright atmosphere, and keep each utterance short for quick exchanges.
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
            part += token
            # check if the current part sentence delimiter
            mm = re.match(r'(.*(\.|\!|\?|\:))(.*)', part)
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

# response generation thread
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
                print(f"SYNTH_START|0|slt_voice_normal|{item}")
                wait_till_synth_event_stop()
    thread1.join()

if __name__ == "__main__":
    main()

```

## Add emotions and actions

Having the CG avatar express emotions and gestures with spoken sentences makes a dialogue system more effective.

Here we show some modification to the "chatgpt.py" example to add emotion expression.  We are going to annotate emotion id to the output sentence, and tell the CG avatar to perform corresponding actions.

1. Estimate the emotion of system utterance. There may be various approarches, but a simple one is to write a prompt for ChatGPT to also estimate emotion at generation. Here, we give the following list of emotion types, and tell MMDAgent-EX to assign a number from the list.

```python
chatgpt_prompt= '''
Your name is Gene. You're a bright and gender-neutral young person around the age of 20,
who enjoys conversations and is rather naive.  Please speak in a cheerful tone and keep
your remarks to one sentence at a time.

Additionally, please choose the appropriate emotion for each sentence from the following
list of emotions, and speak the sentence with the number and a space before it.

List of emotions:
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

2. Specify the mapping of the assigned emotion labels to the CG avatar's actions. There are sample motions in the `motion` folder of each model, so we'll use those.

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

3. In the main processing part, if the beginning of ChatGPT's output has a number, we'll generate the corresponding motion simultaneously. Modify the output part of the above example as follows.
 
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
            print(f"SYNTH_START|0|slt_voice_normal|{outstr}")
```

## Performing Functions mainly in Python and apply MMDAgent-EX as Frontend

While the above example was explained with "MMDAgent-EX as the main module incorporating the dialogue part," it's also possible to integrate it with the idea of "Python as the main module, with MMDAgent-EX serving as a frontend interface."

Below are typical cases:

- Perform speech recognition and response generation in script, and send the output text and motion commands via a message to MMDAgent-EX to make the CG avatar speak.
- Perform till speech synthesis in Python, and make the MMDAgent-EX CG avatar speak by [streaming synthesized voice data](../remote-speech/).
- Handle all spoken dialogue modules (including synthezied audio playing) within Python script, while sending [lip-sync information](../remote-speech) and any action commands to MMDAgent-EX for multi-modal dialogue.

Please feel free to use this approach as suits your application or purpose.