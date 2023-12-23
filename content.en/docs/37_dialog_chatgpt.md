---
title: Connecting with ChatGPT
slug: dialog-test-chatgpt
---

# Connect with ChatGPT

{{< hint warning >}}
Please complete the setup for [voice recognition](../asr-setup) and [speech synthesis
](../tts-test) first.
{{< /hint >}}

## Basic Example

Here is a simple program, `chatgpt.py`, that uses the OpenAI chat completion API for dialogue.

{{< hint warning >}}
The examples provided here use very simple prompts, so the scope of the conversation is quite limited. This page does not cover how to use and optimize chatGPT. The following sample is only for demonstrating integration with MMDAgent-EX.
{{< /hint >}}

The following is a simple Python script that uses a fixed prompt to chat using the OpenAI chat completion API. The operation is as follows:

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

## Enable streaming

OpenAI's chat completion has a streaming mode, which allows you to receive responses token by token, not waiting for the whole response to made. With this streaming mode, responses can start before the entire sentence comes, so it can be used to reduce response latency.

Here is a version of the above program that is adapted to streaming more. The highlights of this program is:

- Connect in streaming mode and sequentially receive response characters from the server in token units.
- As the received tokens are combined, voice synthesis of the obtained parts begins when "。", "？", or "！" appears, judging that as the end of the sentence.
- Since continuous sentences come out, you need to control "waiting for the end event of the voice synthesis that was put out first before starting the next sentence".
- Therefore, stream reception and voice synthesis control need to be parallelized using thread processing. The following makes the reception operate in a separate thread.

```python
# chatgpt.py --- streaming version
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

Furthermore, I will present an example of estimating the emotion in text and playing the corresponding action.

1. Estimate the emotion of the speech. There are various methods, but a simple one is to write a prompt for ChatGPT that includes emotion estimation. Here, we assign numbers to the following types of emotions. This way, for example, ChatGPT might respond with "1 Hello!".

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

2. Specify motions corresponding to the emotions. There are sample motions in the `motion` folder of each model, so you can use it.

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

3. Modify the main loop to find if the output of ChatGPT begins with a number, and generate the corresponding motion command.
 
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
