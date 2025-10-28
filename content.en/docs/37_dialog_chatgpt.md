---
title: Connect to ChatGPT
slug: dialog-test-chatgpt
---
# Connect to ChatGPT

{{< hint warning >}}
Please complete the setup for [speech recognition](../asr-setup) and [speech synthesis](../tts-test) first.
{{< /hint >}}

You can use MMDAgent-EX as the front end for a conversational system. This page shows a simple example of connecting a dialogue module as a submodule to MMDAgent-EX using OpenAI's GPT models, with a sample program you can try.

## Connecting LLM-based response generation to MMDAgent-EX

Below are the steps to create a simple program that uses OpenAI's chat completion API for conversation and run it as a submodule of MMDAgent-EX.

{{< hint warning >}}
The examples below use very simple prompts, so the conversational behavior is extremely limited. This page does not cover advanced prompt engineering or optimization for chatGPT. Use the following only as sample code for integrating with MMDAgent-EX.
{{< /hint >}}

The `chatgpt.py` below is a simple Python script that converses with the OpenAI chat completion API. Except for the final `main()` section, it is a standard text-chat implementation. In `main()` the input/output is adapted to run as a MMDAgent-EX submodule and performs the following actions:

- Reads messages from standard input.
- Extracts the recognized speech text from the input.
- Obtains a system response from the OpenAI API for that recognized text.
- Outputs a speech-synthesis-start message to standard output.

This sample was tested with OpenAI's Python library version 1.3.9.

You need an OpenAI API key to run it. Replace `YOUR_API_KEY` with your API key.

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
            print(f"SYNTH_START|0|mei_voice_normal|{outstr}")

if __name__ == "__main__":
    main()

```

Configure MMDAgent-EX to start this script as a submodule using the method described in [Connecting with Python](../dialog-test-python). For example, on Windows where the Python executable is "python.exe":

{{< mdf>}}
Plugin_AnyScript_Command=python.exe -u chatgpt.py
{{< / mdf >}}

On macOS or Linux, write the same command line you would use in the terminal. Example:

{{< mdf>}}
Plugin_AnyScript_Command=python -u chatgpt.py
{{< / mdf >}}

Start MMDAgent-EX and try conversing with ChatGPT.

## Extending to streaming

LLM-based response generation can take several seconds to tens of seconds to produce an answer, which introduces latency. Many LLMs, including OpenAI's chat completion API, offer a streaming mode that streams generated tokens as they are produced. By receiving tokens incrementally, detecting suitable synthesis boundaries, and starting speech synthesis for each segment without waiting for the full response, you can reduce the perceived response latency. This approach is commonly used to lower delay in LLM-driven dialogue.

Below is a version of the previous program adapted for streaming. The method for detecting chunk boundaries is a trade-off between speed and TTS quality; here we simply split when sentence-ending punctuation appears. Also, synthesized audio playback must be coordinated so segments play in order without overlap, which typically requires thread and queue-based timing control. The outline of operation:

- Connect in streaming mode and receive response text token by token.
- While accumulating tokens, treat punctuations as sentence boundaries and start synthesis for the segment obtained so far.
- Because multiple sentences may be produced, wait for the previous synthesis's completion event before starting the next one.
- Therefore, streaming reception and synthesis control run in parallel threads. The example below runs reception in a separate thread.

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
            part += token.strip()
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
                print(f"SYNTH_START|0|slt_voice_normal|{item}")
                wait_till_synth_event_stop()
    thread1.join()

if __name__ == "__main__":
    main()

```

## Adding emotion estimation and actions

Having the CG avatar express emotions and gestures alongside speech makes the dialogue more effective. As an example, let's have the generated text include an emotion label and trigger avatar actions accordingly.

1. Estimate the emotion associated with the generated utterance. There are many ways to infer emotions or actions from text; for a simple experiment, instruct ChatGPT (via the prompt) to include an emotion label together with the generated sentence. Use the following emotion set and have ChatGPT prepend the corresponding number and a space to the sentence (e.g., "1 Hello!"):

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

2. Map the assigned emotion labels to avatar motions. Place sample motions under each model's `motion` folder and map the emotion numbers as follows:

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

3. In main(), if the ChatGPT output begins with a number, trigger the corresponding motion at the same time as speech. Replace the output section in the earlier example with:

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

## Performing ASR and TTS in Python with MMDAgent-EX as the front end

The examples above describe using MMDAgent-EX as the main module with the dialogue part embedded. Alternatively, you can make Python the main module and use MMDAgent-EX as a controlled front-end interface. Typical cases:

- Perform speech recognition and response generation in Python, then send the resulting text and action commands to MMDAgent-EX to make the CG avatar speak.
- Perform speech synthesis in Python and pipe the synthesized audio into MMDAgent-EX (see [Injecting synthesized audio](../remote-speech/)) to make the avatar speak.
- Perform recognition, synthesis, and playback entirely in Python, and send only lip-sync data or motion commands to MMDAgent-EX (see [Remote speech]) to control movement.

Use whichever approach suits your application.