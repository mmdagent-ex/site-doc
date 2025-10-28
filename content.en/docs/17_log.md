---
title: Log
slug: log
---
# Log

The system's runtime state, streaming messages, warnings, and other events are all output to the log in real time. Viewing the log lets you inspect in detail what is happening inside MMDAgent-EX.

## Log output methods

Logs can be output in the following four ways:

- Output to the terminal
- Output to a file
- On-screen output
- Output inside the 3D scene

## Output to the terminal

On macOS and Linux, logs are written to standard output.

On Windows, press `Shift+d` to open a separate log terminal window.

## Output to a file

Logs can be saved to a file. In an .mdf file, specify the output file with `log_file=`.

{{< mdf>}}
log_file=log.txt
{{< / mdf >}}

## On-screen detailed output

Press `Shift+f` to display a detailed log on-screen. Press `Shift+f` again to hide it.

![Log 2](/images/log2.png)

- **System Log**: System log (same as above)
  - Time-ordered FST transition information
  - Network status
  - Other system logs
- **Message Log**: Message log (same as above)
  - Sent: A message was issued
  - Captured: A message was received and processed
- **FST Status**: State display for each interaction script
  - For each FST, shows transition history, current state, and waiting messages
  - When sub-FSTs are used, each FST is displayed separately

## 3D scene output

Press `d` to display the log in the 3D scene. Press `d` again to hide it.

![Log 1](/images/log1.png)

- **Message Log**: Message log
  - Sent: A message was issued
  - Captured: A message was received and processed
- **System Log**: System log
  - FST transition information
  - Network status
  - Other system logs