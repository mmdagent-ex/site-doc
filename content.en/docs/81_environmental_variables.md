---
title: Environment Variables
slug: envval
---
# Environment Variables

How to reference environment variables in MMDAgent-EX files, and environment variables that affect MMDAgent-EX behavior.

## Referencing environment variables in .mdf files

You can reference environment variables with `%ENV{name}`. If the specified environment variable is not defined, it will be replaced with an empty string.

## Playback command "play" for `AUDIO_START`

On Ubuntu and macOS, MMDAgent-EX uses the sox command "play" to play sound files for `AUDIO_START` messages. Playback is launched from within MMDAgent-EX with the `-q` option as follows:

```shell
play -q file.mp3
```

The `play` command is first searched for on the PATH. If not found on the PATH (or if it fails for other reasons), MMDAgent-EX will look for `/opt/homebrew/bin/play`, `/usr/local/bin/play`, and `/usr/bin/play` in that order and use the first one found.

If you want to specify a sound playback command other than `play`, set the environment variable `MMDAGENT_AUDIO_PLAY_COMMAND`.

### Content folder

The content folder is a workspace for downloaded content and history data. By default it is "MMDAgent-Contents" on the desktop, but you can change its location with the `MMDAgentContentDir` environment variable.