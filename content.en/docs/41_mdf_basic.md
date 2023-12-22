

---
title: Parameter Settings
slug: mdf-basic
---

# Parameter Settings

You can specify various settings in the .mdf file.

The .mdf file serves as the starting point for content playback. The settings described in the .mdf file of the content are read when the content is executed.

Additionally, the system configuration file `MMDAgent-EX.mdf`, located in the same folder as the MMDAgent-EX executable file, is loaded as the default setting at startup. If there are overlapping specifications, the content side takes precedence, overriding the default values if the settings are described in the .mdf file of the content.

In the file, you can refer to environment elements in the form of `%ENV{environment variable name}`. At the time of content startup, this part is replaced with the value of the corresponding environment variable and interpreted.

## Sample

Here is a sample of an .mdf file. There are a wide range of values that can be set. For more details, please refer to the [mdf Parameter List](../mdf).

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