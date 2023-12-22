---
title: Logs
slug: log
---

# Logs

The status of the system in operation, flowing messages, warnings, etc., are all output in real time to the logs. By viewing the logs, you can see in detail what is happening inside MMDAgent-EX.

## Several ways of outputting logs

Logs can be output in the following four ways:

- output to terminal
- save to file
- show on screen
- render in 3D scene

## Output to terminal

On macOS and Linux, logs are output to the standard output.

On Windows, you can open a log terminal in a separate window by pressing the `Shift+d` key.

## Save to file

You can save logs to a file. Please specify the output file with `log_file=` in the .mdf file.

{{< mdf>}}
log_file=log.txt
{{< / mdf >}}

## Show on screen

You can display detailed logs on the screen by pressing the `Shift+f` key. You can erase it by pressing `Shift+f` again.

![Log 2](/images/log2.png)

- **System Log**: System log (same as above)
  - Timeline of FST transition information
  - Network status
  - Other system logs
- **Message Log**: Message log (same as above)
  - Sent: Message was issued
  - Captured: Received and processed the message
- **FST Status**: Status display for each dialogue script
  - For each FST, displays transition history, current status, messages waiting
  - Displays for each FST when using sub-FST function

## Render in 3D scene

You can display simple logs within the 3D scene by pressing the `d` key. You can erase it by pressing the `d` key again.

![Log 1](/images/log1.png):

- **Message Log**: Message log
  - Sent: Message was issued
  - Captured: Received and processed the message
- **System Log**: System log
  - FST transition information
  - Network status
  - Other system logs