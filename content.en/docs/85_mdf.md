

---
title: List of mdf Configuration Items
slug: mdf
---

# List of Parameters that can be Set with .mdf

## Mechanism

- MMDAgent-EX launches content by specifying a .mdf file
  - The .mdf file is located in the top directory of the content.
- The content of the .mdf file is a text file.
  - It can specify the operational parameters of MMDAgent-EX
- `MMDAgent-EX.mdf` in the same directory as the MMDAgent-EX executable is for system settings
  - It is read first at every startup
  - If the settings of the content's .mdf overlap, the content side is prioritized
- You can incorporate the value of any environment variable by describing it as `%ENV{name}`.

## Precautions

- In the following list, the values are basically the default values
- The coordinates of 3D space can be considered as approximately 1.0 ≒ 8cm (MMD scale)

# List of Configuration Items

## Input/Output

Output logs to a file. The default is blank (i.e., no output).

{{<mdf>}}
log_file=
{{</mdf>}}

## Plugin

Specify whether to enable or disable plugins.

{{<mdf>}}
disablePlugin=ALL
enablePlugin=Audio,VIManager
{{</mdf>}}

The value on the right side can specify the following strings

- **`ALL`**: Matches all plugins
- **`NONE`**: Matches nothing
- **Plugin Name**: Specify the name part `xxxx` of `Plugin_xxxx.dll` or `Plugin_xxxx.so` under the `Plugins` directory. In the above example, only Plugin_Audio.dll (or .so) and Plugin_VIManger.dll (or .so) are enabled. If there are multiple, separate them with commas.

Evaluation is done in the order of `enablePlugin` → `disablePlugin`. The order of description in .mdf does not matter.

Example 1: To enable only plugins `A`, `B`, `C` and disable the rest:

{{<mdf>}}
enablePlugin=A,B,C
disablePlugin=ALL
{{</mdf>}}

Example 2: To disable plugins `D`, `E` and enable the rest:

{{<mdf>}}
disablePlugin=D,E
{{</mdf>}}

※ The old version of writing (specifying one plugin to disable at a time) can also be used

{{<mdf>}}
exclude_Plugin_Audio=yes
{{</mdf>}}

## Network

※ Effective when using Plugin_Remote

※ The values in this section are not default values, but sample values

### When using a WebSocket server

Specify the hostname, port number, and path of the WebSocket connection

{{<mdf>}}
Plugin_Remote_Websocket_Host=localhost
Plugin_Remote_Websocket_Port=9000
Plugin_Remote_Websocket_Directory=/chat
{{</mdf>}}

### TCP/IP Server

When connecting to a server as a TCP/IP client

{{<mdf>}}
Plugin_Remote_EnableClient=true
Plugin_Remote_Hostname=localhost
Plugin_Remote_Port=50001
{{</mdf>}}

When becoming a TCP/IP server

{{<mdf>}}
Plugin_Remote_EnableServer=true
Plugin_Remote_ListenPort=50001
{{</mdf>}}

### Common Settings

Specify the number of automatic retries on connection failure (default is 0)

{{<mdf>}}
Plugin_Remote_RetryCount=60
{{</mdf>}}

## Voice playing (SPEAK_START) (v1.0.4)

Switch **SPEAK_START** to use old 16kHz playing scheme for forced sync.  (If not set or set to false, use high-quality playing scheme)

{{<mdf>}}
Plugin_Remote_Speak_16k=true
{{</mdf>}}

## Display

Initial window size (width, height)

{{<mdf>}}
window_size=600,600
{{</mdf>}}

Start in full screen (can be switched after starting with the `F` key)

{{<mdf>}}
full_screen=false
{{</mdf>}}

Show the operating status on the top left at startup (can be switched after starting with the `S` key)

{{<mdf>}}
show_fps=true
{{</mdf>}}

(Windows) Enable / disable transparent window.  When set to `true`, window will become transparent.  The transparent part of the window is click-through.  

By default, it performs **color based** transparency.  A special transparent color is temporary painted for campus background, and pixels with the color will be made transparent.  The default transparent color is green (0.0,1.0,0.0), but can be changed by `transparent_color`.

When `transparent_pixmap` is set to true, it performs slow-but-better **pixmap based** transparency.  The alpha channel in the rendered picture will be directly used as window tranparent value.  This method results always results in better transparent quality, but it is slow (extremely for large screen) and may degrades smoothness.

While transparent, the stage background image will not be rendered.

{{<mdf>}}
transparent_window=false
{{</mdf>}}

(Windows) Change the transparent color used in the color based transparency.  Default is `0.0,1.0,0.0` (green).

{{<mdf>}}
transparent_color=0.0,1.0,0.0
{{</mdf>}}

(Windows) Use pixmap-based transparent mode instead of color based. 

When set to true, it performs slow-but-better **pixmap based** transparency.  The alpha channel in the rendered picture will be directly used as window tranparent value.  This method results always results in better transparent quality, but it is slow and may degrades smoothness.

{{<mdf>}}
transparent_pixmap=false
{{</mdf>}}

## 3-D Models

Maximum number of models to display at once. Minimum is 1, maximum is 1024.

{{<mdf>}}
max_num_model=10
{{</mdf>}}

Toon edge thickness (can be changed after startup with `K`, `Shift+K`)

![bold edge](/images/edge1.png)
![thin edge](/images/edge2.png)

{{<mdf>}}
cartoon_edge_width=0.35
{{</mdf>}}

Disable light-direction-based edge deformation (v1.0.5 and later) and revert to MMD-compliant edge.

{{<mdf>}}
light_edge=false
{{</mdf>}}

Number of parallel threads to use for skinning. Normally, the default of 1 is no problem, but if rendering becomes slow with a huge model with many vertices, specify `2` or `4`. Can be changed later with a message.

{{<mdf>}}
parallel_skinning_numthreads=1
{{</mdf>}}

## Viewpoint (Camera)

Initial camera parameters. In order from the top, position, amount of rotation (degrees), camera distance, field of view (degrees).

{{<mdf>}}
camera_transition=0.0,13.0,0.0
camera_rotation=0.0,0.0,0.0
camera_distance=100.0
camera_fovy=16.0
{{</mdf>}}

## CG Rendering

Anti-aliasing (MSAA) intensity. The higher the value, the smoother the lines will be displayed, but it will also become heavier. You can turn off this function by setting it to 0. The maximum setting value is 32.

{{<mdf>}}
max_multi_sampling=4
{{</mdf>}}

The size of the background image and floor image in the 3D space. The parameters (x, y, z) are x=half of the width, y=depth of the floor, z=height of the background.

![stage image](/images/stage.png)

{{<mdf>}}
stage_size=25.0,25.0,40.0
{{</mdf>}}

Canvas color (space background color) (R,G,B)

{{<mdf>}}
campus_color=0.0,0.0,0.2
{{</mdf>}}

The direction of the light source (x,y,z,w), intensity (0.0-1.0), and color (R,G,B). The direction of arrival and color can also be changed by a message after startup.

{{<mdf>}}
light_direction=0.5,1.0,0.5,0.0
light_intensity=0.6
light_color=1.0,1.0,1.0
{{</mdf>}}

Diffusion filter: Enable with `diffusion_postfilter=true`

*Only available on Windows and Linux, not available on macOS

{{<mdf>}}
diffusion_postfilter=false
diffusion_postfilter_intensity=0.6
diffusion_postfilter_scale=1.0
{{</mdf>}}

## Shadows

Initial shadow display settings at startup (can be switched with `Shift+S` after startup)

{{<mdf>}}
use_shadow=true
{{</mdf>}}

Turn on shadow mapping at startup (can be switched with `X` after startup)

{{<mdf>}}
use_shadow_mapping=false
{{</mdf>}}

Doppel Shadow effect ON/OFF (default is OFF) and parameters

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

## Physics Simulation

Simulation resolution (fps) of physics simulation. You can specify 30, 60, 120. Setting a lower value will lighten the processing, but it will make it easier for rigid bodies to escape.

{{<mdf>}}
bullet_fps=120
{{</mdf>}}

## External Operations

Switch lip sync during external operations from remote voice to microphone input (`yes` when specified)

{{<mdf>}}
Plugin_Remote_EnableLocalLipsync=no
{{</mdf>}}

When the above is `yes`, specifying `yes` for the following will pass through the microphone input to voice output

{{<mdf>}}
Plugin_Remote_EnableLocalPassthrough=no
{{</mdf>}}

Record lip sync voice in specified directory by speech unit. It is possible to specify the maximum recording time in minutes (default: 120 minutes)

{{<mdf>}}
Plugin_Remote_Record_Wave_Dir=directory
Plugin_Remote_Record_Wave_Limit=120
{{</mdf>}}

Maximum duration when saving motion with **MOTIONCAPTURE_START** message (unit: minutes)

{{<mdf>}}
motion_capture_max_minutes=10
{{</mdf>}}

## Voice Recognition

**Plugin_Julius_conf**, **Plugin_Julius_lang**

The configuration name and language name of the voice recognition engine.

No default specified. Prepare the model and enable Plugin_Julius by specifying these valid combinations in .mdf.

Supported combinations by default model:

- dnn, ja
- dnn, en
- gmm, ja

{{<mdf>}}
Plugin_Julius_conf=dnn
Plugin_Julius_lang=en
{{</mdf>}}

**Plugin_Julius_wordspacing**

Specifies whether to separate words in the output of recognition results.

- `no`: Pack without putting anything between words (default for `ja`)
- `yes`: Insert a space between words (default for languages other than `ja`)
- `comma`: Insert a comma between words (compatible with old MMDAgent)

{{<mdf>}}
Plugin_Julius_wordspacing=yes
{{</mdf>}}

**Plugin_Julius_logfile**

Output the internal log of the Julius engine to a file.

{{<mdf>}}
Plugin_Julius_logfile=log.txt
{{</mdf>}}

**show_caption**

Display subtitles. The voice recognition results are displayed on the left side of the screen and the voice synthesis content (the sentence given with **SYNTH_START**) is displayed on the right side.

{{<mdf>}}
show_caption=true
{{</mdf>}}

## Other Adjustment Items

### HTTP Server

Disable the HTTP server function (default: enabled)

{{<mdf>}}
http_server=false
{{</mdf>}}

Change the port number (default: 50000)

{{<mdf>}}
http_server_port=50000
{{</mdf>}}

### Rendering Related

Use cartoon rendering

{{<mdf>}}
use_cartoon_rendering=true
{{</mdf>}}

Use MMD compatible coloring

{{<mdf>}}
use_mmd_like_cartoon=true
{{</mdf>}}

Edge color of the selected model (R,G,B,A, values between 0.0 and 1.0)

{{<mdf>}}
cartoon_edge_selected_color=1.0,0.0,0.0,1.0
{{</mdf>}}

Whether to place a floor plane at y = 0 during physics simulation

{{<mdf>}}
bullet_floor=true
{{</mdf>}}

Gravity factor

{{<mdf>}}test
gravity_factor=10.0
{{</mdf>}}

Duration (in seconds) to display the internal comments of the model during loading. 0 to not display.

{{<mdf>}}
display_comment_time=0
{{</mdf>}}

Size of one side of the texture for shadow mapping

{{<mdf>}}
shadow_mapping_texture_size=1024
{{</mdf>}}

Density of the shadow cast on the model during shadow mapping

{{<mdf>}}
shadow_mapping_self_density=1.0
{{</mdf>}}

Density of the shadow cast on the floor during shadow mapping

{{<mdf>}}
shadow_mapping_floor_density=0.5
{{</mdf>}}

Shadow mapping rendering order: true for light to dark, false for dark to light

{{<mdf>}}
shadow_mapping_light_first=true
{{</mdf>}}

### Display Related

Display the button at startup during button definition (can be toggled after startup with `Q` key)

{{<mdf>}}
show_button=true
{{</mdf>}}

Position of the simplified log display (size, position, scale)

{{<mdf>}}
log_size=80,30
log_position=-17.5,3.0,-20.0
log_scale=1.0
{{</mdf>}}

Fine-tuning the motion playback timing (unit: seconds, maximum value 10.0)

{{<mdf>}}
motion_adjust_time=0.0
{{</mdf>}}

Priority of the lip motion created by automatic lip-sync during playback

{{<mdf>}}
lipsync_priority=100.0
{{</mdf>}}

### User Interface Related

Adjustment of sensitivity during key and mouse operations: camera rotation, camera movement, distance, field of view

{{<mdf>}}
rotate_step=4.5
translate_step=0.5
distance_step=4.0
fovy_step=1.0
{{</mdf>}}

Step multiplier when changing the thickness of the edge with `K`, `Shift+K` keys

{{<mdf>}}
cartoon_edge_step=1.2
{{</mdf>}}

{{< hint ms >}}
### Face tracking parameters [MS]

{{<mdf>}}
# Coef. of BODY rotation from head rotation
Plugin_Remote_RotationRateBody=0.5
# Coef. of NECK rotation from head rotation
Plugin_Remote_RotationRateNeck=0.5
# Coef. of HEAD rotation from head rotation
Plugin_Remote_RotationRateHead=0.6
# Coef. of CENTER up/down movement from head rotation
Plugin_Remote_MoveRateUpDown=3.0
# Coef. of CENTER left/right movement from head rotation
Plugin_Remote_MoveRateSlide=0.7
# enable mirrored movement
Plugin_Remote_EnableMirrorMode=false
{{</mdf>}}

{{< /hint >}}
