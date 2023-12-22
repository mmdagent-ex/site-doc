

---
title: Environment Variables
slug: envval
---

# Environment Variables

This is a guide on how to reference environment variables in MMDAgent-EX files, as well as the environment variables that affect the operation of MMDAgent-EX.

## Referencing Environment Variables in .mdf Files

Environment variables can be referenced with `%ENV{name}`. If the specified name of the environment variable is not defined, it will be blank.

## Playback Command play for `AUDIO_START`

In Ubuntu and macOS, the "play" command from sox is used for sound file playback with the `AUDIO_START` message. Playback is initiated from within MMDAgent-EX using the `-q` option as follows:

```shell
play -q file.mp3
```

First, the `play` command is searched for in the PATH. If there is an error because `play` is not found in the path, it searches in the order of `/opt/homebrew/bin/play`, `/usr/local/bin/play`, `/usr/bin/play`, and the first one found is used.

If you want to specify a different sound playback command, specify it with the `MMDAGENT_AUDIO_PLAY_COMMAND` environment variable.

### Content Folder

The content folder is a workspace that stores downloaded content and history information. By default, it is "MMDAgent-Contents" directly under the desktop. However, you can specify a different location using the `MMDAgentContentDir` environment variable.