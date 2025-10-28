---
title: Embedding Submodules
slug: submodule
---
{{< hint info >}}
The submodule embedding feature is provided by Plugin_AnyScript. Make sure this plugin is enabled when using it.
{{< /hint >}}

# Embedding Submodules

You can extend MMDAgent-EX by embedding any application (including Python scripts) as a submodule. The application is launched as a child process when MMDAgent-EX starts and exits when MMDAgent-EX does. The method used on the [Try voice interaction (Python)](../dialog-test-python) and [Example: Integrating ChatGPT](../dialog-test-chatgpt) pages uses this approach.

This page outlines how to embed submodules.

## Plugin_AnyScript

Embedding submodules is implemented by Plugin_AnyScript.
Plugin_AnyScript is a plugin that starts and connects applications as child processes. A child process started by Plugin_AnyScript has its standard I/O directly connected to MMDAgent-EX's message queue:

- The child process's standard output is issued to MMDAgent-EX as messages as-is.
- All messages issued by MMDAgent-EX are provided to the child process's standard input.

The usage shown on the [Try voice interaction (Python)](../dialog-test-python) page was about controlling dialogue, but you can also extend MMDAgent-EX in other ways, for example:

- Use a different speech synthesis engine: the process receives `SYNTH_START` messages on standard input, performs synthesis, and outputs audio (disable the default Plugin_Open_JTalk).
- Use a different speech recognition engine: the process performs recognition and writes the result to standard output in the form `RECOG_EVENT_STOP|Recognition result` (disable the default Plugin_Julius).
- Add a camera: send `MOTION_ADD` messages to standard output according to detection results to insert camera-reactive motions.

{{< hint warning >}}
### Programming notes

When embedding an application or script as a submodule, always disable **standard output buffering** for that process. If buffering is enabled, messages you output may not be delivered immediately to MMDAgent-EX, causing missed or delayed processing.

For Python scripts, start Python with the `-u` option to disable buffering. For other languages, ensure your program explicitly flushes output after each line.
{{< /hint >}}

## Registering submodules

Register submodules in .mdf files. Specify the command used to start the submodule. Everything from the `=` to the end of the line is used as the startup command. Spaces in the command are allowed.

Be careful when specifying paths:

- The executable can be specified as a full path or as a command. If given as a full path, that executable is run. If given as a command, on Windows the executable is located according to the CreateProcessA specifications, and on macOS/Linux it is searched for in the PATH environment variable according to execvp() behavior.
- The runtime current directory is the folder where the .mdf is located. Take care when passing filenames as arguments.

{{<mdf>}}
# example 1: full-path on Windows
Plugin_AnyScript_Command=C:\Program Files\Python310\python.exe -u test.py
# example 2: command on macOS/Linux
Plugin_AnyScript_Command=python3 -u test.py
{{</mdf>}}

To specify multiple modules, write them like the following. You can specify up to 10.

{{<mdf>}}
Plugin_AnyScript_Command1=...
Plugin_AnyScript_Command2=...
{{</mdf>}}

## Behavior at startup

Applications specified as submodules are started as MMDAgent-EX child processes when MMDAgent-EX launches, and they terminate when MMDAgent-EX exits.

## Selecting messages sent to stdin

All messages flowing within MMDAgent-EX are sent to the submodule's standard input. You cannot choose which message types are sent. Implement any filtering and processing required on the module side.

By default, standard input receives only "messages". If you also want to receive all operation logs, add the following to the .mdf:

{{<mdf>}}
Plugin_AnyScript_AllLog=true
{{</mdf>}}

## Example

Below is an example module that fetches a weather forecast and responds. The speech recognition result message `RECOG_EVENT_STOP` is sent not only to the MMDAgent-EX core but to all modules, so even if a .fst script cannot respond to the utterance "weather", a submodule like this can handle it.

```python
def query_weather():
    # Retrieve the weather forecast
    # Create a response based on the retrieved forecast
    return(response)

if __name__ == "__main__":
    while True:
        input_line = input().strip()
        if input_line.startswith("RECOG_EVENT_STOP|weather"):
            response = query_weather()
            print(f"SYNTH_START|0|mei_voice_normal|{response}")
```
