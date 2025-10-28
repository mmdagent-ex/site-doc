---
title: Parameter Settings
slug: mdf-basic
---
# Parameter Settings

You can specify various settings in a .mdf file.

.mdf files act as the entry point for content playback. Settings written in a content's .mdf file are read when that content is executed.

Also, the system settings file `MMDAgent-EX.mdf` located in the same folder as the MMDAgent-EX executable is loaded at startup as the default configuration. If the same setting is specified in both places, the content's setting takes precedence, so adding settings to a content's .mdf will override the defaults.

Note that within files you can reference environment elements in the form `%ENV{environment variable name}`. When the content starts, that part is replaced with the value of the environment variable and interpreted.

## Sample

Here is a sample .mdf file. Many values can be configured. For details, see [List of mdf parameters](../mdf).

{{< mdf>}}

# File name for saving logs
log_file=

# Disable all plugins except specified ones
disablePlugin=ALL
enablePlugin=Audio,VIManager

# Initial window size (width, height)
window_size=600,600

# Full screen at startup if true
full_screen=false

# Display status in top left
show_fps=true

# Anti-aliasing strength
max_multi_sampling=4

# Stage size
stage_size=25.0,25.0,40.0

# Voice Recognition (Julius)
Plugin_Julius_conf=dnn
Plugin_Julius_lang=ja
show_caption=true
{{< /mdf>}}