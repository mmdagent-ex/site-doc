

---
title: Integrating Submodules
slug: submodule
---
{{< hint info >}}
The submodule integration feature is provided by Plugin_AnyScript. Please make sure this plugin is enabled when using it.
{{< /hint >}}

# Integrating Submodules

You can extend the capabilities of MMDAgent-EX by integrating any application, including Python scripts, as a submodule. The application is launched as a child process at the time of MMDAgent-EX startup and terminates simultaneously with it. This method was used in the [Voice Dialogue Test (Python)](../dialog-test-python) page, and the [ChatGPT Integration Example](../dialog-test-chatgpt).

This section provides an overview of how to integrate a submodule.

## Plugin_AnyScript

Submodule integration is achieved through Plugin_AnyScript. The Plugin_AnyScript plugin launches and connects applications as child processes. Child processes started by Plugin_AnyScript have their standard input/output directly connected to the MMDAgent-EX's message queue:

- The standard output of the child process is issued directly to MMDAgent-EX as a message
- All messages issued from MMDAgent-EX are given to the standard input of the child process

In the [Voice Dialogue Test (Python)](../dialog-test-python), we showed how to control dialogue, but you can also:

- **Use another speech synthesis engine**: The process receives a `SYNTH_START` message from the standard input, performs speech synthesis, and outputs audio (the default Plugin_Open_JTalk is disabled)
- **Use another voice recognition engine**: The process performs voice recognition and outputs the results in the form of `RECOG_EVENT_STOP|Recognition result` to the standard output (the default Plugin_Julius is disabled)
- Add a camera: By sending the `MOTION_ADD` message to the standard output according to the camera detection results, you can insert motions that react to the camera

These are some of the possible extensions.

{{< hint warning >}}

### Notes on Program Creation

When embedding applications or scripts as submodules, **always turn OFF the standard output buffering of their process**. If buffering is ON, the output messages will not be immediately emitted to MMDAgent-EX, which could lead to processing not being performed or being delayed.

In the case of Python scripts, you can turn off buffering by adding the `-u` option at startup. Otherwise, please create a program that explicitly flushes the output each time a line is output.
{{< /hint >}}

## Registering Submodules

Submodules are registered in .mdf files. Specify the command to start as a submodule. Everything from `=` to the end of the line is used as the start command. There's no problem if there are spaces in the command.

Please pay particular attention when specifying paths.

- You can specify the executable binary either as a full path or as a command. If specified as a full path, that executable binary will be executed. If specified as a command, the executable binary will be searched according to the specifications of the [`CreateProcessA` function on Windows](https://learn.microsoft.com/ja-jp/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa), and according to the `execvp()` specifications on macOS / Linux, with the executable binary being searched from the `PATH` environment variable.
- The current directory at runtime is the folder where the .mdf file is placed. Be careful when specifying file names and the like as arguments.

{{<mdf>}}

# example 1: full-path on Windows
Plugin_AnyScript_Command=C:\Program Files\Python310\python.exe -u test.py

# example 2: command on macOS/Linux
Plugin_AnyScript_Command=python3 -u test.py
{{</mdf>}}

If you want to specify multiple modules, write as follows. You can specify up to 10.

{{<mdf>}}
Plugin_AnyScript_Command1=...
Plugin_AnyScript_Command2=...
{{</mdf>}}

## Behavior at Startup

Applications specified as submodules will be launched as child processes of MMDAgent-EX at the time of MMDAgent-EX startup. They also terminate at the same time as MMDAgent-EX.

## Selecting Messages Sent to Standard Input

All messages flowing within MMDAgent-EX are sent to the standard input of the submodule. You cannot select the type of messages that are sent. Please write processes on the module side to select and process messages as necessary.

By default, only "messages" can be received via standard input. If you also want to receive all operation logs, please specify the following in the .mdf file.

{{<mdf>}}
Plugin_AnyScript_AllLog=true
{{</mdf>}}

## Sample Operation

Below is an example of creating a module that retrieves and responds to weather forecasts. Since the `RECOG_EVENT_STOP` message from the voice recognition result is sent to not only the main body of MMDAgent-EX but also all modules, even if the .fst script cannot answer the utterance "weather", you can create a submodule to respond like this.

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
