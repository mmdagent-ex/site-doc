---
title: Testing Voice Interaction (Python)
slug: dialog-test-python
---
# Work with Python

The default [FST based dialogue control](../dialog-test-fst) is a primitive way.  It is a low-level language and not always suitable for describing complex dialogue scenarios.

MMDAgent-EX has a facility to run any program as [sub module](../submodule) and connect its stdin / stdout with the MMDAgent-EX's message queue.  In this page, we show an example of connecting a python script as MMDAgent-EX submodule to run as a simple dialogue manager:

- Receive messages of voice recognition results from standard input
- Output corresponding response messages to standard output

{{< hint warning >}}
This page uses voice recognition and voice synthesis. If you haven't set these up yet, please complete the setup for [voice recognition](../asr-setup) and [voice synthesis](../tts-test) first.
{{< /hint >}}

## Preparation

Set up your Python environment. The following assumes version 3.7 and later.

If you have already tried "[Testing Voice Interaction (fst)](../dialog-test-fst)", the .fst may have been modified.  To make sure the following example runs correctly, please revert the .fst before edit.  If you are manually reverting it, keep the following section in `main.fst` and delete the rest.

{{<fst>}}
0 LOOP:
    <eps> STAGE|images/floor_green.png,images/back_white.png
    <eps> MODEL_ADD|0|gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0
{{</fst>}}

## Test Connectivity

First of all, try connection using a dummy program.

### Create test.py

The following is a tiny Python program that outputs the string "`TEST|aaa`" to standard output every second. Please create this under `example` folder, and save it as `test.py`.

```python
#### example/test.py
import time
while(1):
    print("TEST|aaa")
    time.sleep(1)
```

After saving, please check that it works in the terminal (or command prompt).  Output should look like this (Press `CTRL+C` to stop it):

```shell
% python example/test.py
TEST|aaa
TEST|aaa
...
```

### Set up to launch test.py as submodule

Open `example/main.mdf` in a text editor, and add the following line at the end.

{{< mdf>}}
Plugin_AnyScript_Command=python -u test.py
{{< / mdf >}}

The command to launch starts from the `=`. Write the same command as when launching from the shell. In Python, use the `-u` option.

Once you save the file, launch MMDAgent-EX specifying this .mdf file. After startup, the specified command is automatically launched as a subprocess, the message stream of MMDAgent-EX will be connected for the standard input and output of test.py. After startup, press the `d` key to display the log, and see if `TEST|aaa` is showing every second.

```shell
./Release/MMDAgent-EX.exe ./example/main.mdf
```

If it doesn't work, try the following solutions.

{{< details "Checkpoints if it's not working" close >}}

### Executable Path

In the launch command (in this case `python -u test.py`), the command is interpreted almost the same as in a regular command prompt (terminal).

- If the command is specified with a full path starting with `/`, the file at the specified path is executed.
- If the above does not apply, the execution command is searched and executed according to the set execution path.

If you cannot specify the command correctly, try specifying the executable file with a full path.

### Current Directory

The current directory at runtime is the folder where the .mdf file is located. Be careful with programs that provide file paths.

### Character Encoding

Text is exchanged in UTF-8. Please make sure that the standard input/output of the Python script is UTF-8.

### -u Option

If standard output buffering is enabled, messages may not be immediately output to MMDAgent-EX even if they are output. Disable standard output buffering as much as possible. In Python, this can be disabled with the `-u` option.

For other issues, if it doesn't work, please refer to the [detailed explanation](../submodule/).
{{< /details >}}

## Dumb Example of a Dialogue Program

Let's move on to the next example. We will try a Python sample program `example/sample-dialog.py` that responds with "Nice to meet you!" to the input "Hello". This program performs the following actions:

- Continuously reads text from the standard input (i.e., the MMDAgent-EX message stream)
- If there is a recognition result message (`RECOG_EVENT_STOP`), it extracts the recognition result part and passes it to the `generate_response()` function
- `generate_response()` returns a response to the recognized sentence. In this case, it responds to "Hello" with "Nice to meet you!" and to anything else with "I don't understand."
- Outputs the obtained response as a speech synthesis message (`SYNTH_START`) to the standard output (i.e., the message stream)

```python
#### example/sample-dialog.py
import re

# Set input and output strings to UTF-8
import sys
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

# Return a response
def generate_response(str):
    if str == "Hello.":
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

Just like the previous test.py, let's set this program as a submodule. Describe it in .mdf as follows (overwrite the previous test command).

{{< mdf>}}
Plugin_AnyScript_Command=python -u sample-dialog.py
{{< / mdf >}}

After setting, start MMDAgent-EX and try saying "Hello".

```shell
./Release/MMDAgent-EX.exe ./example/main.mdf
```

## Extension

Since all output texts are sent to MMDAgent-EX as messages, you can send various controls from the script, such as playing a motion by sending a `MOTION_ADD` message.