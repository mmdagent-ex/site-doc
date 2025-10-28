---
title: Try Voice Dialogue (Python)
slug: dialog-test-python
---
# Try Voice Dialogue (Python)

The "[Try Voice Dialogue (fst)](../dialog-test-fst)" page explained how to create a simple voice dialogue using a .fst script, but .fst is a primitive language and not suitable for describing complex dialogue scenarios. Advanced dialogue control should be handled by an external program.

This page explains how to create a Python program that

- receives speech-recognition result messages from standard input, and
- writes appropriate response messages to standard output

so you can control the dialogue externally.

{{< hint warning >}}
This page uses speech recognition and speech synthesis. If you haven't done so already, please complete the [Speech Recognition](../asr-setup) and [Speech Synthesis](../tts-test) setup first.
{{< /hint >}}

## Preparation

Prepare a Python runtime environment. The instructions below assume Python 3.7 or later.

If you already tried the "[Try Voice Dialogue (fst)](../dialog-test-fst)" example, the dialogue portion in the .fst may duplicate functionality, so remove that part before proceeding. From main.fst, leave only the following section and delete the rest.

{{<fst>}}
0 LOOP:
    <eps> STAGE|images/floor_green.png,images/back_white.png
    <eps> MODEL_ADD|0|gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0
{{</fst>}}

## Connection test

First, let's run a connection test using a dummy program.

### Create test.py

The following Python program prints the string "TEST|aaa" to standard output every second. Create this under the example folder and save it as test.py.

```python
#### example/test.py
import time
while(1):
    print("TEST|aaa")
    time.sleep(1)
```

Save it and run it once in a terminal (press CTRL+C to stop).

```shell
% python example/test.py
TEST|aaa
TEST|aaa
...
```

### Set the command that starts test.py in the .mdf

Now configure MMDAgent-EX to start this test.py as a submodule. Submodule startup commands are specified in the .mdf file. Open example/main.mdf in a text editor and add the following line at the end.

{{< mdf>}}
Plugin_AnyScript_Command=python -u test.py
{{< / mdf >}}

The text to the right of '=' is the startup command. Enter the same command you would use in a shell. For Python, include the -u option.

Save the file and start MMDAgent-EX with that .mdf. After startup, the specified command will be launched automatically as a subprocess and connected to MMDAgent-EX's message stream. After starting, press the `d` key to show the log; if you see `TEST|aaa` printed every second, the connection is successful. Proceed to the next step.

```shell
./Release/MMDAgent-EX.exe ./example/main.mdf
```

If it doesn't work, try the following checks.

{{< details "Troubleshooting checklist" close >}}
### Executable

The startup command (e.g. `python -u test.py`) is interpreted similarly to a normal terminal command.

- If the command is specified as a full path starting with `/`, that exact path is executed.
- Otherwise, the command is searched for according to the configured execution PATH and then executed.

If the command cannot be found, try specifying the executable with a full path.

### Current working directory

The runtime working directory is the folder containing the .mdf. Be careful when using relative file paths.

### Character encoding

Text is exchanged in UTF-8. Ensure your Python script's standard input/output use UTF-8.

### -u option

If standard output is buffered, messages may not appear immediately in MMDAgent-EX. Disable stdout buffering if possible. In Python, use the `-u` option to disable buffering.

For other issues, see the detailed explanation: [../submodule/](../submodule/)
{{< /details >}}

## Example text-based dialogue program

Next example: try the Python sample program example/sample-dialog.py, which responds to "Hello" with "Nice to meet you!". The program behaves as follows:

- Continuously read text from standard input (MMDAgent-EX's message stream)
- When a recognition result message (`RECOG_EVENT_STOP`) is received, extract the recognized text and pass it to the function `generate_response()`
- `generate_response()` returns a response for the recognized text. Here it replies "Nice to meet you!" to "Hello", and "I don't understand" to anything else.
- Output the generated response as a speech-synthesis message (`SYNTH_START`) to standard output (the message stream)

```python
#### example/sample-dialog.py
import re

# Set input and output strings to UTF-8
import sys
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

# Return a response
def generate_response(str):
    if str == "Hello":
        return "Nice to meet you!"
    return "I don't understand."

# Main function
def main():
    while True:
        instr = input().strip()
        if not instr:
            break
        # Check if the input is RECOG_EVENT_STOP
        utterance = re.findall('^RECOG_EVENT_STOP\|(.*)$', instr)
        if utterance:
            # Extract the speech content from the message and generate a response sentence
            outstr = generate_response(utterance[0])
            # Output the generated response sentence as a SYNTH_START message
            print(f"SYNTH_START|0|slt_voice_normal|{outstr}")

if __name__ == "__main__":
    main()
```

As with test.py, configure this program as a submodule. In the .mdf, write the following (overwrite the previous test command).

{{< mdf>}}
Plugin_AnyScript_Command=python -u sample-dialog.py
{{< / mdf >}}

After configuring, start MMDAgent-EX and try saying "Hello".

```shell
./Release/MMDAgent-EX.exe ./example/main.mdf
```

## Extending

All output text is sent to MMDAgent-EX as messages, so your script can also send control messages -- for example, sending a `MOTION_ADD` message will play a motion.