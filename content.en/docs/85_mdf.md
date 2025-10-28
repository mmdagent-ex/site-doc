---
title: List of .mdf Configuration Options
slug: mdf
---
# List of parameters configurable in .mdf

## How it works

- MMDAgent-EX launches content by specifying a .mdf file
  - The .mdf file is located in the top directory of the content.
- The .mdf file is a text file.
  - It specifies runtime parameters for MMDAgent-EX.
- `MMDAgent-EX.mdf` in the same directory as the MMDAgent-EX executable is the system configuration
  - It is read first on every startup
  - If settings overlap with the content’s .mdf, the content-side settings take precedence
- You can import arbitrary environment variable values by writing them like `%ENV{NAME}`.

## Notes

- In the list below, values are generally the default values.
- For 3D space coordinates, you can roughly assume 1.0 ≈ 8 cm (MMD scale).

# Configuration items

## Input/Output

Specify a file path to record all logs to the specified file. Default is empty (on Linux/Mac logs go to stdout; on Windows nothing is output).

{{<mdf>}}
log_file=
{{</mdf>}}

Set whether to exchange messages via standard input/output. Default is `false`. If set to `true`, messages are output to stdout and inputs from stdin are accepted as messages. When this is `true`, logs are no longer written to stdout, so specify a file in `log_file` if you want to keep a log.

{{<mdf>}}
use_stdinout=false
{{</mdf>}}

## Plugins

Enable or disable plugins.

{{<mdf>}}
disablePlugin=ALL
enablePlugin=Audio,VIManager
{{</mdf>}}

The right-hand value can be the following strings:

- **`ALL`** : matches all plugins
- **`NONE`** : matches none
- **Plugin name**: Specify the name portion `xxxx` of `Plugin_xxxx.dll` or `Plugin_xxxx.so` under the `Plugins` directory. In the example above, only Plugin_Audio.dll (or .so) and Plugin_VIManager.dll (or .so) are enabled. Use commas to separate multiple names.

Evaluation is done in the order `enablePlugin` → `disablePlugin`. The order of lines in the .mdf file does not matter.

Example 1: Enable only plugins `A`, `B`, `C` and disable the rest:

{{<mdf>}}
enablePlugin=A,B,C
disablePlugin=ALL
{{</mdf>}}

Example 2: Disable plugins `D`, `E` and enable the rest:

{{<mdf>}}
disablePlugin=D,E
{{</mdf>}}

Note: The old format below (specifying disabled plugins one by one) is also supported:

{{<mdf>}}
exclude_Plugin_Audio=yes
{{</mdf>}}

## Network

Note: Effective when using Plugin_Remote.

Note: In this section the values are sample values, not defaults.

### Using a WebSocket server

Specify the WebSocket host, port, and path.

{{<mdf>}}
Plugin_Remote_Websocket_Host=localhost
Plugin_Remote_Websocket_Port=9000
Plugin_Remote_Websocket_Directory=/chat
{{</mdf>}}

### TCP/IP Server

As a TCP/IP client connecting to a server:

{{<mdf>}}
Plugin_Remote_EnableClient=true
Plugin_Remote_Hostname=localhost
Plugin_Remote_Port=50001
{{</mdf>}}

As a TCP/IP server:

{{<mdf>}}
Plugin_Remote_EnableServer=true
Plugin_Remote_ListenPort=50001
{{</mdf>}}

### Common settings

Specify the number of automatic retry attempts on connection failure (default is 0).

{{<mdf>}}
Plugin_Remote_RetryCount=60
{{</mdf>}}

## Audio playback (SPEAK_START) (v1.0.4)

Use pre-v1.0.4 synchronous guaranteed 16 kHz conversion playback for SPEAK_START. If unspecified or `false`, the higher-quality playback introduced in v1.0.4+ is used.

{{<mdf>}}
Plugin_Remote_Speak_16k=true
{{</mdf>}}

## Display

Initial window size (width,height)

{{<mdf>}}
window_size=600,600
{{</mdf>}}

Start in fullscreen (can be toggled after startup with the `F` key)

{{<mdf>}}
full_screen=false
{{</mdf>}}

Show operation status in the top-left on startup (toggle with `S` after startup)

{{<mdf>}}
show_fps=true
{{</mdf>}}

(Windows) Enable or disable a transparent window. When `true`, the window is transparent. Clicks on transparent areas pass through to underlying applications.

By default color-based transparency is used. During rendering a special "transparent color" is set as the background canvas color, and pixels that match that color become transparent. The default transparent color is green (0.0,1.0,0.0), which can be changed with `transparent_color`.

If you set `transparent_pixmap` to `true`, a slower but higher-quality pixmap-based transparency method is used. The alpha channel of the rendered pixmap is used directly as the window transparency. This always produces more natural transparency than the color-based method, but is slower and can significantly reduce frame rates, especially on large screens.

Note that the stage background image is not drawn while transparency is enabled.

{{<mdf>}}
transparent_window=false
{{</mdf>}}

(Windows) Specify/change the transparent color used for color-based transparency. Default is green (0.0,1.0,0.0).

{{<mdf>}}
transparent_color=0.0,1.0,0.0
{{</mdf>}}

(Windows) Enable pixmap-based transparency instead of color-based. When `transparent_pixmap` is `true`, a slower but more accurate pixmap-based transparency is used. The alpha channel of the rendered pixmap is used directly for window transparency. This produces better visual quality than color-based transparency but is slower and can reduce frame rate on large screens.

{{<mdf>}}
transparent_pixmap=false
{{</mdf>}}

## 3-D Models

Maximum number of models displayed at once. Minimum 1, maximum 1024.

{{<mdf>}}
max_num_model=10
{{</mdf>}}

Toon edge width (changeable after startup with `K`, `Shift+K`)

![bold edge](/images/edge1.png)
![thin edge](/images/edge2.png)

{{<mdf>}}
cartoon_edge_width=0.35
{{</mdf>}}

Turn off the feature that adjusts toon edges to the light direction (v1.0.5+), to revert to MMD compatibility.

{{<mdf>}}
light_edge=false
{{</mdf>}}

Number of parallel threads used for skinning. Default 1 is fine in most cases, but for very large models with many vertices you can set `2` or `4`. This can also be changed later via messages.

{{<mdf>}}
parallel_skinning_numthreads=1
{{</mdf>}}


## Camera

Initial camera parameters. From top: position, rotation (degrees), camera distance, field of view (degrees).

{{<mdf>}}
camera_transition=0.0,13.0,0.0
camera_rotation=0.0,0.0,0.0
camera_distance=100.0
camera_fovy=16.0
{{</mdf>}}

## CG Rendering

Antialiasing (MSAA) level. Higher values smooth lines but increase load. Set 0 to disable. Maximum supported value is 32.

{{<mdf>}}
max_multi_sampling=4
{{</mdf>}}

Size of the background and floor images in 3D space. Parameters (x,y,z) mean x = half-width, y = floor depth, z = background height.

![stage image](/images/stage.png)

{{<mdf>}}
stage_size=25.0,25.0,40.0
{{</mdf>}}

Canvas color (space background color) (R,G,B)

{{<mdf>}}
campus_color=0.0,0.0,0.2
{{</mdf>}}

Light direction (x,y,z,w), intensity (0.0–1.0), color (R,G,B). Direction and color can be changed via messages at runtime.

{{<mdf>}}
light_direction=0.5,1.0,0.5,0.0
light_intensity=0.6
light_color=1.0,1.0,1.0
{{</mdf>}}

Diffusion postfilter: enable with `diffusion_postfilter=true`

Note: Windows and Linux only — not available on macOS

{{<mdf>}}
diffusion_postfilter=false
diffusion_postfilter_intensity=0.6
diffusion_postfilter_scale=1.0
{{</mdf>}}

## Shadows

Initial shadow display setting at startup (toggle with `Shift+S` after startup)

{{<mdf>}}
use_shadow=true
{{</mdf>}}

Enable shadow mapping at startup (toggle with `X` after startup)

{{<mdf>}}
use_shadow_mapping=false
{{</mdf>}}

Doppel Shadow effect on/off (default OFF) and parameters

![doppel_shadow](/images/doppel_shadow.png)

{{<mdf>}}

# turn on doppel shadow
doppel_shadow=true

# color of double shadow
doppel_shadow_color=r,g,b

# offset of double shadow
doppel_shadow_offset=x,y,z

# density of the shadow (default is 0.5)
shadow_density=0.5
{{</mdf>}}

## Physics

Simulation resolution (fps) for physics. Allowed values: 30, 60, 120. Lower values reduce processing load but may cause rigid bodies to pass through each other more easily.

{{<mdf>}}
bullet_fps=120
{{</mdf>}}

## External control

Switch lipsync during external control from remote audio to microphone input (specify `yes` to enable)

{{<mdf>}}
Plugin_Remote_EnableLocalLipsync=no
{{</mdf>}}

If the above is `yes`, setting the following to `yes` will pass microphone input through to audio output

{{<mdf>}}
Plugin_Remote_EnableLocalPassthrough=no
{{</mdf>}}

Record lipsync audio per utterance into the specified directory. You can set a recording time limit in minutes (default: 120 minutes)

{{<mdf>}}
Plugin_Remote_Record_Wave_Dir=directory
Plugin_Remote_Record_Wave_Limit=120
{{</mdf>}}

Maximum duration (minutes) when saving motion via the MOTIONCAPTURE_START message

{{<mdf>}}
motion_capture_max_minutes=10
{{</mdf>}}

## Speech Recognition

Plugin_Julius_conf, Plugin_Julius_lang

Names for the speech recognition engine configuration and language.

There is no default. Prepare models and specify a valid combination in the .mdf to enable Plugin_Julius.

Combinations supported by the default models:

- dnn, ja
- dnn, en
- gmm, ja

{{<mdf>}}
Plugin_Julius_conf=dnn
Plugin_Julius_lang=en
{{</mdf>}}

Plugin_Julius_wordspacing

Specify whether to separate words in recognition output.

- `no`: Do not insert anything between words (default for `ja`)
- `yes`: Insert spaces between words (default for languages other than `ja`)
- `comma`: Insert commas between words (compatible with older MMDAgent)

{{<mdf>}}
Plugin_Julius_wordspacing=yes
{{</mdf>}}

Plugin_Julius_logfile

Output the Julius engine internal log to a file.

{{<mdf>}}
Plugin_Julius_logfile=log.txt
{{</mdf>}}

show_caption

Show captions. The left side of the screen displays speech recognition results, and the right side displays synthesized speech content (text provided with **SYNTH_START**).

{{<mdf>}}
show_caption=true
{{</mdf>}}

## Other adjustments

### HTTP Server

Disable the HTTP server feature (default: enabled)

{{<mdf>}}
http_server=false
{{</mdf>}}

Change the port number (default: 50000)

{{<mdf>}}
http_server_port=50000
{{</mdf>}}

### Rendering

Use cartoon rendering

{{<mdf>}}
use_cartoon_rendering=true
{{</mdf>}}

Use MMD-compatible coloring

{{<mdf>}}
use_mmd_like_cartoon=true
{{</mdf>}}

Edge color for the selected model (R,G,B,A — values 0.0–1.0)

{{<mdf>}}
cartoon_edge_selected_color=1.0,0.0,0.0,1.0
{{</mdf>}}

Whether to insert a floor plane at y = 0 for physics.

{{<mdf>}}
bullet_floor=true
{{</mdf>}}

Gravity factor

{{<mdf>}}test
gravity_factor=10.0
{{</mdf>}}

Duration (seconds) to display the model’s internal comment at load. Set 0 to disable.

{{<mdf>}}
display_comment_time=0
{{</mdf>}}

Shadow mapping texture size (per side)

{{<mdf>}}
shadow_mapping_texture_size=1024
{{</mdf>}}

Shadow density cast onto models during shadow mapping

{{<mdf>}}
shadow_mapping_self_density=1.0
{{</mdf>}}

Shadow density cast onto the floor during shadow mapping

{{<mdf>}}
shadow_mapping_floor_density=0.5
{{</mdf>}}

Shadow mapping rendering order: true for light→dark, false for dark→light

{{<mdf>}}
shadow_mapping_light_first=true
{{</mdf>}}

### Display

Show defined buttons on screen at startup (toggle with `Q` after startup)

{{<mdf>}}
show_button=true
{{</mdf>}}

Simple log display settings (size, position, scale)

{{<mdf>}}
log_size=80,30
log_position=-17.5,3.0,-20.0
log_scale=1.0
{{</mdf>}}

Fine-tune motion playback timing (seconds, max 10.0)

{{<mdf>}}
motion_adjust_time=0.0
{{</mdf>}}

Playback priority for lip motion generated by automatic lipsync

{{<mdf>}}
lipsync_priority=100.0
{{</mdf>}}

### User interface

Adjust sensitivity for key/mouse operations: camera rotation, camera translation, distance, field of view

{{<mdf>}}
rotate_step=4.5
translate_step=0.5
distance_step=4.0
fovy_step=1.0
{{</mdf>}}

Step multiplier when changing edge width with the `K` / `Shift+K` keys

{{<mdf>}}
cartoon_edge_step=1.2
{{</mdf>}}