---
title: Message List
slug: messages
---
# Message List

## Overview

MMDAgent's internal modules are connected in a spoke-and-hub manner.

- Messages output by one module are broadcast to all modules.
- All messages are delivered to all modules.
- Each module may react to any message and may output any message.

Below is a list of messages used by the MMDAgent core and plugin modules.

All text encoding is UTF-8.

## Legend

- "()" explains parameters.
- "x,y,z" are coordinates. MMDAgent uses OpenGL so a right-handed coordinate system. Default is 0,0,0.

  ![right handed coordinate system](/images/right-handed.png)

- "rx,ry,rz" are rotation values (degrees). Default is 0,0,0.
- "r,g,b" or "r,g,b,a" specify colors. Values range 0.0–1.0.
- "(A or B ...)" indicates a choice. Default is the first element of the list.

---

# 3D Models

## Adding / Removing Models

**MODEL_ADD**

Add a 3D model to the scene. If no parent model is specified the model is shown in world coordinates. If a parent model is specified the model can be mounted on that model's bone. On completion **MODEL_EVENT_ADD** is issued.

- 1st arg: model alias (new)
- 2nd arg: model filename .pmd
- 3rd arg (optional): initial position, default 0,0,0
- 4th arg (optional): initial rotation, default 0,0,0
- 5th arg (optional): toon rendering ON/OFF, default ON
- 6th arg (optional): parent model alias
- 7th arg (optional): parent model bone name

{{<message>}}
MODEL_ADD|(model alias)|(model file name)
MODEL_ADD|(model alias)|(model file name)|x,y,z
MODEL_ADD|(model alias)|(model file name)|x,y,z|rx,ry,rz
MODEL_ADD|(model alias)|(model file name)|x,y,z|rx,ry,rz|(ON or OFF for cartoon)
MODEL_ADD|(model alias)|(model file name)|x,y,z|rx,ry,rz|(ON or OFF for cartoon)|(parent model alias)
MODEL_ADD|(model alias)|(model file name)|x,y,z|rx,ry,rz|(ON or OFF for cartoon)|(parent model alias)|(parent bone name)
MODEL_EVENT_ADD|(model alias)
{{</message>}}

**MODEL_CHANGE, MODEL_CHANGE_ASYNC**

Replace a displayed model. MODEL_CHANGE blocks until model loading finishes. MODEL_CHANGE_ASYNC is the asynchronous version: loading happens in a separate thread without blocking the main thread. When the model swap finishes **MODEL_EVENT_CHANGE** is issued.

{{<message>}}
MODEL_CHANGE|(model alias)|(model file name)
MODEL_CHANGE_ASYNC|(model alias)|(model file name)
MODEL_EVENT_CHANGE|(model alias)
{{</message>}}

**MODEL_DELETE**

Delete a displayed model. On completion **MODEL_EVENT_DELETE** is issued.

{{<message>}}
MODEL_DELETE|(model alias)
MODEL_EVENT_DELETE|(model alias)
{{</message>}}

**MODEL_EVENT_SELECT**

Issued when a model is selected by double-click.

{{<message>}}
MODEL_EVENT_SELECT|(model alias)
{{</message>}}

## Motion Playback

A predefined sequence of movement is called a motion. Multiple motions can play simultaneously on a single model.

**MOTION_ADD**

Add and start playing a motion on a model. Give each motion an alias. On completion **MOTION_EVENT_ADD** is issued. If the model does not exist the system logs a warning and does nothing. If a motion with the specified alias is already playing, it is overwritten by the new motion.

- 1st arg: target model alias
- 2nd arg: motion alias (new)
- 3rd arg: motion filename .vmd
- 4th arg (optional): FULL (full) or PART (partial), default FULL
- 5th arg (optional): ONCE or LOOP, default ONCE
- 6th arg (optional): smoothing ON/OFF, default ON
- 7th arg (optional): force model reposition OFF/ON at start, default OFF
- 8th arg (optional): motion stacking priority, default 0

Note: If PART (partial) is specified, bones that have no explicit motion (i.e., only have frame 0 keyframes) are excluded from control.

Note: When smoothing is ON the motion will be smoothed at start and end. Specify OFF to disable this.

Note: If the 7th arg (reposition) is ON, at the start of playback the model's "center" bone coordinates will be forcibly converted to the model's root coordinates. Usually OFF is fine.

{{<message>}}
MOTION_ADD|(model alias)|(motion alias)|(motion file name)
MOTION_ADD|(model alias)|(motion alias)|(motion file name)|(FULL or PART)
MOTION_ADD|(model alias)|(motion alias)|(motion file name)|(FULL or PART)|(ONCE or LOOP)
MOTION_ADD|(model alias)|(motion alias)|(motion file name)|(FULL or PART)|(ONCE or LOOP)|(ON or OFF for smooth)
MOTION_ADD|(model alias)|(motion alias)|(motion file name)|(FULL or PART)|(ONCE or LOOP)|(ON or OFF for smooth)|(OFF or ON for reposition)
MOTION_ADD|(model alias)|(motion alias)|(motion file name)|(FULL or PART)|(ONCE or LOOP)|(ON or OFF for smooth)|(OFF or ON for reposition)|priority
MOTION_EVENT_ADD|(model alias)|(motion alias)
{{</message>}}

**MOTION_CHANGE**

Replace a currently playing motion with another. On completion **MOTION_EVENT_CHANGE** is issued.

{{<message>}}
MOTION_CHANGE|(model alias)|(motion alias)|(motion file name)
MOTION_EVENT_CHANGE|(model alias)|(model alias)
{{</message>}}

**MOTION_RESET**

Restart a playing motion from its first frame.

{{<message>}}
MOTION_RESET|(model alias)|(motion alias)
{{</message>}}

**MOTION_DELETE**

Stop and delete a motion. On completion **MOTION_EVENT_DELETE** is issued.

{{<message>}}
MOTION_DELETE|(model alias)|(model alias)
MOTION_EVENT_DELETE|(model alias)|(motion alias)
{{</message>}}

**MOTION_ACCELERATE**

Gradually change a motion's playback speed toward a target frame. On completion **MOTION_EVENT_ACCELERATE** is issued.

- speed: target playback speed, relative to normal 1.0. 0.0 stops playback.
- duration: time in seconds to reach the target speed
- target: target frame on the motion (seconds)

{{<message>}}
MOTION_ACCELERATE|(model alias)|(motion alias)|(speed)|(duration)|(target)
MOTION_EVENT_ACCELERATE|(model alias)|(motion alias)
{{</message>}}

## Motion Blending Configuration

Settings for blending multiple motions. When blending, motions are computed in order from low to high priority and applied to bones and morphs; these settings control how they apply. Default is replace, but you can set add or none. Settings can be applied per motion and further refined per bone.

**MOTION_CONFIGURE**

Configure blend behavior for an existing motion.

- 1st arg: model alias
- 2nd arg: motion alias
- 3rd arg: configuration label (see below)
- 4th+ args: parameters (depend on label)

Available labels. Let rs be the current value and rd be the value specified by this motion. You can also set a blend rate to scale rd.

- **MODE_REPLACE**: replace (rd)
- **MODE_ADD**: add (rs + rd)
- **MODE_MUL**: morphs are multiplied (rs * rd), bones are replaced
- **BLEND_RATE**: set blend rate only (rd' = rd * rate)

{{<message>}}
MOTION_CONFIGURE|(model)|(motion)|MODE_REPLACE
MOTION_CONFIGURE|(model)|(motion)|MODE_REPLACE|(rate)
MOTION_CONFIGURE|(model)|(motion)|MODE_ADD
MOTION_CONFIGURE|(model)|(motion)|MODE_ADD|(rate)
MOTION_CONFIGURE|(model)|(motion)|MODE_MUL
MOTION_CONFIGURE|(model)|(motion)|MODE_MUL|(rate)
MOTION_CONFIGURE|(model)|(motion)|BLEND_RATE|(rate)
{{</message>}}

To set behavior per bone:

- **MODE_BONE_REPLACE**: set specified bones to replace
- **MODE_BONE_ADD**: set specified bones to add
- **MODE_BONE_NONE**: skip specified bones
- **MODE_FACE_REPLACE**: set specified morphs to replace
- **MODE_FACE_ADD**: set specified morphs to add
- **MODE_FACE_MUL**: set specified morphs to multiply
- **MODE_FACE_NONE**: skip specified morphs

{{<message>}}
MOTION_CONFIGURE|(model alias)|(motion alias)|MODE_BONE_REPLACE|bonename[,bonename,..]
MOTION_CONFIGURE|(model alias)|(motion alias)|MODE_BONE_ADD|bonename[,bonename,..]
MOTION_CONFIGURE|(model alias)|(motion alias)|MODE_BONE_NONE|bonename[,bonename,..]
MOTION_CONFIGURE|(model alias)|(motion alias)|MODE_FACE_REPLACE|morphname[,morphname,..]
MOTION_CONFIGURE|(model alias)|(motion alias)|MODE_FACE_ADD|morphname[,morphname,..]
MOTION_CONFIGURE|(model alias)|(motion alias)|MODE_FACE_MUL|morphname[,morphname,..]
MOTION_CONFIGURE|(model alias)|(motion alias)|MODE_FACE_NONE|bonename[,bonename,..]
{{</message>}}

On completion **MOTION_EVENT_CONFIGURE** is issued.

{{<message>}}
MOTION_EVENT_CONFIGURE|(model alias)|(motion alias)
{{</message>}}

## Per-Bone / Per-Morph Control

Ways to externally control a model's bones and morphs outside of motions.

**MODEL_BINDBONE**

Set values for a bone. Two methods: fixed values or binding to a KeyValue. If the bone is controlled by a motion, the motion takes precedence. On completion **MODEL_EVENT_BINDBONE** is issued. Values apply immediately.

- Fixed values: specify translation and rotation numerically.

{{<message>}}
MODEL_BINDBONE|(model alias)|(bone name)|x,y,z|rx,ry,rz
{{</message>}}

- KeyValue binding: after setting, the bone will follow the specified KeyValue key in real time.

{{<message>}}
MODEL_BINDBONE|(key name)|(min)|(max)|(model alias)|(bone name)|x1,y1,z1|rx1,ry1,rz1|x2,y2,z2|rx2,ry2,rz2
{{</message>}}

The target parameters are determined between the two specified parameter sets according to the KeyValue value change.

![BindBone](/images/bindbone.png)

**MODEL_BINDFACE**

Set morph values. Like bones, you can use fixed values or KeyValue binding. If the morph is influenced by a motion, the motion takes precedence. On completion **MODEL_EVENT_BINDFACE** is issued.

- Fixed value: specify a numeric value. Value applies immediately. If `transition_duration` is specified the value will change gradually over that time.

{{<message>}}
MODEL_BINDFACE|(model alias)|(morph name)|(value)`
MODEL_BINDFACE|(model alias)|(morph name)|(value)|(transition_duration)`
{{</message>}}


- KeyValue binding: after setting, the morph will follow the specified KeyValue key in real time. After setting **MODEL_EVENT_BINDBONE** is issued.

{{<message>}}
MODEL_BINDFACE|(key name)|(min)|(max)|(model alias)|(morph name)|rate1|rate2
{{</message>}}

**MODEL_UNBINDBONE**

Unbind the specified bone. On completion **MODEL_EVENT_UNBINDBONE** is issued.

{{<message>}}
MODEL_UNBINDBONE|(model alias)|(bone name)
MODEL_EVENT_UNBINDBONE|(model alias)|(bone name)
{{</message>}}

**MODEL_UNBINDFACE**

Unbind the specified morph. On completion **MODEL_EVENT_UNBINDFACE** is issued.

{{<message>}}
MODEL_UNBINDFACE|(model alias)|(morph name)
MODEL_EVENT_UNBINDFACE|(model alias)|(morph name)
{{</message>}}

## Moving Model Display Position

In the coordinates below `GLOBAL` means world coordinates and `LOCAL` means model-relative coordinates.

**MOVE_START, MOVE_STOP**

Smoothly move a model to a specified position. Movement can be interrupted with MOVE_STOP. On start **MOVE_EVENT_START** is issued; on completion or interruption **MOVE_EVENT_STOP** is issued.

If move speed is specified the model moves to the target at that speed (distance/sec).

{{<message>}}
MOVE_START|(model alias)|x,y,z
MOVE_START|(model alias)|x,y,z|(GLOBAL or LOCAL position)
MOVE_START|(model alias)|x,y,z|(GLOBAL or LOCAL position)|(move speed)
MOVE_STOP|(model alias)
MOVE_EVENT_START|(model alias)
MOVE_EVENT_STOP|(model alias)
{{</message>}}

**TURN_START, TURN_STOP**

Rotate a model so the specified position becomes its front. TURN_STOP can interrupt rotation. On start **TURN_EVENT_START** is issued; on completion or interruption **TURN_EVENT_STOP** is issued.

If rotation speed is specified the model rotates at that speed (degrees/sec).

{{<message>}}
TURN_START|(model alias)|x,y,z
TURN_START|(model alias)|x,y,z|(GLOBAL or LOCAL position)
TURN_START|(model alias)|x,y,z|(GLOBAL or LOCAL position)|(rotation speed)
TURN_STOP|(model alias)
TURN_EVENT_START|(model alias)
TURN_EVENT_STOP|(model alias)
{{</message>}}

**ROTATE_START, ROTATE_STOP**

Rotate a model by the specified rotation amount. ROTATE_STOP can interrupt rotation. On start **ROTATE_EVENT_START** is issued; on completion or interruption **ROTATE_EVENT_STOP** is issued.

If rotation speed is specified the model rotates at that speed (degrees/sec).

{{<message>}}
ROTATE_START|(model alias)|rx,ry,rz
ROTATE_START|(model alias)|rx,ry,rz|(GLOBAL or LOCAL rotation)
ROTATE_START|(model alias)|rx,ry,rz|(GLOBAL or LOCAL rotation)|(rotation speed)
ROTATE_STOP|(model alias)
ROTATE_EVENT_START|(model alias)
ROTATE_EVENT_STOP|(model alias)
{{</message>}}

## Texture Animation

**TEXTURE_SETANIMATIONRATE**

Change the animation speed for an APNG texture per texture.

- `textureFileName` should match the texture identifier used in the model.
- `rate` is 1.0 for normal speed, 0.5 half speed, 2.0 double speed. 0.0 stops.

{{<message>}}
TEXTURE_SETANIMATIONRATE|model alias|textureFileName|rate
{{</message>}}

## Parallel Skinning Configuration

**CONFIG_PARALLELSKINNING_THREADS**

Change the number of threads used for parallel skinning. Valid range is 1–4. Default is the value set in .mdf.

Note: Changing the number of parallel threads while running may destabilize the system. If it behaves poorly, specify `parallel_skinning_numthreads=2` in the .mdf at startup instead.

{{<message>}}
CONFIG_PARALLELSKINNING_THREADS|2
{{</message>}}

## Capture Motion to File

**MOTIONCAPTURE_START, MOTIONCAPTURE_STOP**

Capture model motion to a motion file (.vmd).

{{<message>}}
MOTIONCAPTURE_START|model alias|filename.vmd
MOTIONCAPTURE_STOP|model alias
{{</message>}}

# Screen Composition

## Camera (Viewpoint)

**CAMERA**

Change the camera viewpoint. There are three specification methods.

Numeric specification: set parameters with `x,y,z|rx,ry,rz|(distance)|(fovy)`. These values match those shown at the bottom-left when you press D for a simple log. Transition time period specifies how the viewpoint changes to the target. Default (-1) smoothly transitions, 0 jumps immediately, a positive value moves at a constant rate over that many seconds.

{{<message>}}
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)|(transition time period)
{{</message>}}

Mount to a model: make the camera follow a model's movement in real time. If no bone is specified the camera follows the "center" bone.

{{<message>}}
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)|(transition time period)|(model alias)
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)|(transition time period)|(model alias)|(bone name)
{{</message>}}

Specify via motion: start camera motion defined by a camera motion file (.vmd)

{{<message>}}
CAMERA|(camera motion file name)
{{</message>}}

## Background / Stage

**STAGE**

Specify or change the background, floor images, or a 3D stage model. Background/floor display size is set by `stage_size` in the .mdf. Images are stretched to fit the specified size.

{{<message>}}
STAGE|(floor image file),(back image file)
STAGE|(stage file .xpmd or .pmd)
{{</message>}}

## Image Overlays (Foreground / Frame)

**WINDOWFRAME**

Overlay a frame image (.png) on top of the screen. The image is stretched to match the screen aspect ratio. Single-image method.

![frame](/images/frame.png)

{{<message>}}
WINDOWFRAME|filename.png
{{</message>}}

To remove the image specified by WINDOWFRAME issue it with NONE.

{{<message>}}
WINDOWFRAME|NONE
{{</message>}}

**WINDOWFRAME_ADD**

Add a new frame image. Give an alias name as the argument. On success **WINDOWFRAME_EVENT_ADD** is emitted. If you call WINDOWFRAME_ADD again with the same name the image is replaced.

{{<message>}}
WINDOWFRAME_ADD|frame1|filename.png
WINDOWFRAME_EVENT_ADD|frame1
{{</message>}}

**WINDOWFRAME_DELETE**

Delete the frame image with the specified alias. On success **WINDOWFRAME_EVENT_DELETE** is emitted.

{{<message>}}
WINDOWFRAME_DELETE|frame1
WINDOWFRAME_EVENT_DELETE|frame1
{{</message>}}

**WINDOWFRAME_DELETEALL**

Delete all currently displayed frame images.

{{<message>}}
WINDOWFRAME_DELETEALL
{{</message>}}

**WINDOWOVERLAY_ADD**

Add image as on-screen overlay.  The aspect ratio of the image will be always kept regardless of the window ratio.  the args are:

- alias name
- image file path
- relative width [0..1]: maximum width relative to window, 0 = full width
- relative height [0..1]: maximum height relative to window, 0 = full height
- anchor: specify one of the following literal
  - `CENTER`
  - `TOP_LEFT`
  - `TOP_RIGHT`
  - `BOTTOM_LEFT`
  - `BOTTOM_RIGHT`
- Padding [0..1] space from the anchor (ignored on `CENTER`)

On success, **WINDOWOVERLAY_EVENT_ADD** will be issued.  Issuing this command
for an existing alias will replace the image.

{{<message>}}
WINDOWOVERLAY_ADD|alias1|filename.png|0|0|CENTER|0
WINDOWOVERLAY_EVENT_ADD|alias1
{{</message>}}

**WINDOWOVERLAY_DELETE**

Delete the specified overlay image.  **WINDOWOVERLAY_EVENT_DELETE** will be issued on success.

{{<message>}}
WINDOWOVERLAY_DELETE|alias1
WINDOWOVERLAY_EVENT_DELETE|alias1
{{</message>}}

**WINDOWOVERLAY_DELETEALL**

Forcely clear all existing overlay images.

{{<message>}}
WINDOWOVERLAY_DELETEALL
{{</message>}}

## Transparent Window (Win)

**TRANSPARENT_START**

(Windows only) Make the main window transparent. If no color is specified the default is used (the default comes from .mdf's `transparent_color=`; if unspecified the default is green `0.0,1.0,0.0`).

{{<message>}}
TRANSPARENT_START
TRANSPARENT_START|r,g,b
{{</message>}}

**TRANSPARENT_STOP**

(Windows only) Revert a transparent window to opaque.

{{<message>}}
TRANSPARENT_STOP
{{</message>}}

## Lighting

**LIGHTCOLOR**

Change light direction and color.

{{<message>}}
LIGHTDIRECTION|x,y,z
LIGHTCOLOR|r,g,b
{{</message>}}

# Displaying Text and Images

## Display Text, Images, or Live Camera Feed

Display arbitrary text, images, or live camera feed in 3D space.

Procedure: first define a display area with **TEXTAREA_ADD**, then specify content with **TEXTAREA_SET**. Calling **TEXTAREA_SET** repeatedly lets you change the content in the same area.

**TEXTAREA_ADD**

Add a new area. Specify size, colors, coordinates, and orientation. Coordinates are the area's center. You may parent the area to a model.

On completion **TEXTAREA_EVENT_ADD** is issued.

- 1st arg: alias name (new)
- 2nd arg: width and height
  - Positive: fixed size (content is scaled down to fit if overflow)
  - 0: flexible size: auto-adjusts to content. For images aspect ratio is preserved.
- 3rd arg: text size, margin, line spacing. Each 1.0 is the default.
- 4th arg: background color r,g,b,a (a = 0 means no background)
- 5th arg: text color r,g,b,a
- 6th arg: center coordinates
- 7th arg (optional): orientation (rotation)
- 8th arg (optional): parent model alias
- 9th arg (optional): parent bone name (defaults to "center" if omitted)

{{<message>}}
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z|rx,ry,rz
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z|rx,ry,rz|(parent model alias)
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z|rx,ry,rz|(parent model alias)|(parent bone name)
TEXTAREA_EVENT_ADD|alias
{{</message>}}

**TEXTAREA_SET**

Display text or an image in the area. On start **TEXTAREA_EVENT_SET** is issued. If something is already displayed it is replaced.

For the 2nd arg:

- If you provide a string it is displayed. If it contains spaces enclose it in "". Use "\n" for line breaks.
- If you provide an image file path the image is displayed.

{{<message>}}
TEXTAREA_SET|(textarea alias)|(string or image path)
TEXTAREA_EVENT_SET|alias
{{</message>}}

**TEXTAREA_DELETE**

Delete the area and remove the display. On completion **TEXTAREA_EVENT_DELETE** is issued.

{{<message>}}
TEXTAREA_DELETE|(textarea alias)
TEXTAREA_EVENT_DELETE|alias
{{</message>}}

## Text Captions

Display text captions. Differences from TextArea:

- On-screen display (not in 3D space), fixed to the screen
- You can specify custom fonts
- Up to two outline (edge) styles can be specified
- Can auto-disappear after a specified duration
- (v1.0.2) .lrc files can be used to play a sequence of captions

![caption](/images/caption.png)

**CAPTION_SETSTYLE**

Define a style. After defining **CAPTION_EVENT_SETSTYLE** is issued.

- 1st arg: style alias (new)
- 2nd arg: font file path; "default" uses system font
- 3rd arg: text color r,g,b,a
- 4th arg (optional): first edge color and thickness r,g,b,a,thickness. To disable, set a or thickness to 0.
- 5th arg (optional): second edge color and thickness (same format)
- 6th arg (optional): base/background color r,g,b,a — set a to 0 if not needed

(v1.0.2) Args after the 4th can be collectively omitted. If omitted default edge styles are applied.

{{<message>}}
CAPTION_SETSTYLE|style_alias|fontpath|r,g,b,a
CAPTION_SETSTYLE|style_alias|fontpath|r,g,b,a|edge1|edge2|basecolor
CAPTION_EVENT_SETSTYLE|style_alias
{{</message>}}

**CAPTION_START**

Start showing text with the specified style. If already present only the text is updated. The caption disappears on CAPTION_STOP or after the `duration` specified.

(v1.0.2) Instead of text you may specify a .lrc file path to play captions according to the .lrc file.

- 1st arg: alias (new)
- 2nd arg: style name defined via CAPTION_SETSTYLE, or "_default" (v1.0.2)
- 3rd arg: display text. If it contains spaces enclose in "". Use "\n" for line breaks. (v1.0.2) Or .lrc file path.
- 4th arg: text size
- 5th arg: horizontal alignment: CENTER, LEFT, or RIGHT
- 6th arg: vertical position as a relative value where bottom=0.0 and top=1.0
- 7th arg: display duration in frames (30 = 1 second)

{{<message>}}
CAPTION_START|alias|style|text|size|align|height|duration
(v1.0.2) CAPTION_START|alias|style|file.lrc|size|align|height|duration
CAPTION_EVENT_START|alias
CAPTION_EVENT_STOP|alias
{{</message>}}

Example:

{{<message>}}
10 10:
    KEY|1 CAPTION_SETSTYLE|terop|rounded-mplus-1c-heavy.ttf|1,0.5,0,1|1,1,1,1,4|0,0,0,0.6,6|0,0,0,0
    CAPTION_EVENT_SETSTYLE|terop CAPTION_START|test|terop|test|3.0|CENTER|0.5|300
{{</message>}}

**CAPTION_STOP**

Forcefully remove a displayed caption. On success **CAPTION_EVENT_STOP** is issued.

{{<message>}}
CAPTION_STOP|alias
CAPTION_EVENT_STOP|alias
{{</message>}}

## Notification

**NOTIFY_SHOW**

Show a system message on the screen. It disappears after 2.0 seconds.

{{<message>}}
 NOTIFY_SHOW|(text)
{{</message>}}

You can change the display duration.

{{<message>}}
 NOTIFY_SHOW|(text)|(seconds)
{{</message>}}

## Show a Text Prompt and Get User Response

**PROMPT_SHOW**

Display a message dialog for user selection. If the text contains spaces enclose it in "". Maximum choices: 15.

{{<message>}}
PROMPT_SHOW|(main text)|(item text 0)|(item text 1)|...
{{</message>}}

Example:

{{<message>}}
PROMPT_SHOW|"main text"|item1|item2|item3
{{</message>}}

![prompt](/images/prompt.png)

When the user selects an item **PROMPT_EVENT_SELECTED** is emitted with the selected index (0–). If the user cancels (click outside the dialog or press ESC) -1 is returned.

{{<message>}}
PROMPT_EVENT_SELECTED|(selected number or -1 for cancel)
{{</message>}}

## Show Document Fullscreen and Get User Response

**INFOTEXT_FILE**

Display the contents of a text file fullscreen. On start **INFOTEXT_EVENT_SHOW** is issued.

- 1st arg: text file path
- 2nd arg: title label
- 3rd arg: button labels, comma-separated e.g. "Yes,No,Cancel"
- 4th arg (optional): text scale (default 1.0)
- 5th arg (optional): background color as hex "RRGGBBAA", e.g. white = FFFFFFFF
- 6th arg (optional): text color same format

The displayed document can be scrolled by dragging (swipe).

Buttons specified by the 3rd arg appear at the bottom. When the user selects a button the display closes and **INFOTEXT_EVENT_CLOSE** is issued with the index of the pressed button.

Example: show README.txt

{{<message>}}
INFOTEXT_FILE|README.md|"This is readme"|OK,Cancel
{{</message>}}

![infotext](/images/infotext.png)

{{<message>}}
INFOTEXT_FILE|(filepath)|(titleLabel)|(buttonLabels)
INFOTEXT_FILE|(filepath)|(titleLabel)|(buttonLabels)|(scale)
INFOTEXT_FILE|(filepath)|(titleLabel)|(buttonLabels)|(scale)|(BACKGROUNDCOLOR)|(TEXTCOLOR)
INFOTEXT_EVENT_SHOW
INFOTEXT_EVENT_CLOSE|(selecteDButtonLabel)
{{</message>}}


**INFOTEXT_STRING**

Display a string fullscreen.

- 1st arg: text content (string)
- 2nd arg: title label
- 3rd arg: button labels, e.g. "Yes,No,Cancel"
- 4th arg (optional): text scale (default 1.0)
- 5th arg (optional): background color hex "RRGGBBAA"
- 6th arg (optional): text color

Button labels appear at the bottom. When a button is pressed the display closes.

On show **INFORTEXT_EVENT_SHOW** is issued; on close **INFORTEXT_EVENT_CLOSE** is issued with the index of the selected button.

{{<message>}}
INFOTEXT_STRING|textbody|(titleLabel)|(buttonLabels)
INFOTEXT_STRING|textbody|(titleLabel)|(buttonLabels)|(scale)
INFOTEXT_STRING|textbody|(titleLabel)|(buttonLabels)|(scale)|(BACKGROUNDCOLOR)|(TEXTCOLOR)
INFOTEXT_EVENT_SHOW
INFOTEXT_EVENT_CLOSE|(selecteDButtonLabel)
{{</message>}}

# Audio

## Sound Playback

**SOUND_START**

Start playback of a sound file. mp3 and wav are supported. On start **SOUND_EVENT_START** is emitted, and on stop **SOUND_EVENT_STOP** is emitted.

{{<message>}}
SOUND_START|(sound alias)|(sound file name)
SOUND_EVENT_START|(sound alias)
SOUND_EVENT_STOP|(sound alias)
{{</message>}}

**SOUND_STOP**

Force-stop a playing sound. On stop **SOUND_EVENT_STOP** is emitted.

{{<message>}}
SOUND_STOP|(sound alias)
SOUND_EVENT_STOP|(sound alias)
{{</message>}}

## Speech Playback with LIPSYNC

**SPEAK_START**

Make a specified model speak using an audio file. LIPSYNC is performed in sync with playback. On start **SPEAK_EVENT_START** is emitted and on end **SPEAK_EVENT_STOP** is emitted. A .shapemap configuration is required.

{{<message>}}
SPEAK_START|(model alias)|(audio file)
SPEAK_EVENT_START|(model alias)
SPEAK_EVENT_STOP|(model alias)
{{</message>}}

**SPEAK_STOP**

Stop audio started by SPEAK_START. When audio stops (or is already stopped) **SPEAK_EVENT_STOP** is emitted.

{{<message>}}
SPEAK_STOP|(model alias)
SPEAK_EVENT_STOP|(model alias)
{{</message>}}

## Speech Recognition

Message contents vary depending on the module or plugin used.

### Common

**RECOG_EVENT_START**

Emitted when speech input starts.

{{<message>}}
RECOG_EVENT_START
{{</message>}}

**RECOG_EVENT_STOP**

Emitted when a speech recognition result is obtained.

{{<message>}}
RECOG_EVENT_STOP|(recognized result string)
{{</message>}}

### Plugin_Julius

**RECOG_EVENT_OVERFLOW**

Emitted when input audio level is too high and overflows.

{{<message>}}
RECOG_EVENT_OVERFLOW
{{</message>}}

**RECOG_EVENT_MODIFY**

Emitted when a RECOG_MODIFY message has been processed.

{{<message>}}
RECOG_EVENT_MODIFY|GAIN
RECOG_EVENT_MODIFY|USERDICT_SET
RECOG_EVENT_MODIFY|USERDICT_UNSET
RECOG_EVENT_MODIFY|CHANGE_CONF|(jconf_file_prefix)
{{</message>}}

**RECOG_EVENT_AWAY**

Emitted when speech recognition is temporarily suspended (ON) or resumed (OFF) due to menu actions or external control.

{{<message>}}
RECOG_EVENT_AWAY|ON
RECOG_EVENT_AWAY|OFF
{{</message>}}

**RECOG_EVENT_GMM**

Output tag from Julius environmental sound classification.

{{<message>}}
RECOG_EVENT_GMM|noise
{{</message>}}

**RECOG_MODIFY**

Engine configuration change commands. Dynamically modify a running engine.

- GAIN: input amplitude scaling factor (default 1.0)
- USERDICT_SET: load a user dictionary (replace if already loaded)
- USERDICT_UNSET: remove the user dictionary
- CHANGE_CONF: restart engine with specified jconf files

{{<message>}}
RECOG_EVENT_MODIFY|GAIN|(scale)
RECOG_EVENT_MODIFY|USERDICT_SET|(dict_file_path)
RECOG_EVENT_MODIFY|USERDICT_UNSET
RECOG_EVENT_MODIFY|CHANGE_CONF|(jconf_file_prefix)
{{</message>}}

**RECOG_RECORD_START**

Start automatic recording of input audio. Extracted audio segments are saved sequentially as individual .wav files in the specified directory.

{{<message>}}
RECOG_RECORD_START|(directory)
{{</message>}}

**RECOG_RECORD_STOP**

Stop automatic recording of input audio.

{{<message>}}
RECOG_RECORD_STOP
{{</message>}}

## Speech Synthesis

Message contents vary by module/plugin.

### Common

**SYNTH_START**

Start speech synthesis. The specified model will lipsync to the synthesized output. When output starts **SYNTH_EVENT_START** is emitted; when it finishes **SYNTH_EVENT_STOP** is emitted.

{{<message>}}
SYNTH_START|(model alias)|(voice alias)|(synthesized text)
SYNTH_EVENT_START|(model alias)
SYNTH_EVENT_STOP|(model alias)
{{</message>}}

**SYNTH_STOP**

Force-stop ongoing speech synthesis. When stopped **SYNTH_EVENT_STOP** is emitted.

{{<message>}}
SYNTH_STOP|(model alias)
SYNTH_EVENT_STOP|(model alias)
{{</message>}}

### Plugin_Open_JTalk

Japanese speech synthesis engine.

{{<message>}}
LIPSYNC_START|(model alias)|(phoneme and millisecond pair sequence)
LIPSYNC_STOP|(model alias)
LIPSYNC_EVENT_START|(model alias)
LIPSYNC_EVENT_STOP|(model alias)
{{</message>}}

# External Control (Plugin_Remote)

## Control / Operation

**AVATAR|START, AVATAR|STOP**

Issued when the external control API receives the external-control start command `__AV_START` or end command `__AV_END`.

{{<message>}}
AVATAR|START
AVATAR|END
{{</message>}}

**AVATAR_CONTROL**

Temporarily suspend or resume model control from external API commands. After processing **AVATAR_EVENT_CONTROL** is issued.

- DISABLE: temporarily disable
- ENABLE: end disable and resume

{{<message>}}
AVATAR_CONTROL|DISABLE
AVATAR_EVENT_CONTROL|DISABLED
AVATAR_CONTROL|ENABLE
AVATAR_EVENT_CONTROL|ENABLED
{{</message>}}

**REMOTEKEY_CHAR, REMOTEKEY_DOWN, REMOTEKEY_UP**

Send keyboard input from external sources.

{{<message>}}
REMOTEKEY_CHAR|(character)
REMOTEKEY_DOWN|(key code string)
REMOTEKEY_UP|(key code string)
{{</message>}}

## Operation Log Recording

**AVATAR_LOGSAVE_START, AVATAR_LOGSAVE_STOP**

Record all external control commands to a file. Start with AVATAR_LOGSAVE_START and stop with AVATAR_LOGSAVE_STOP.

{{<message>}}
AVATAR_LOGSAVE_START|filename
AVATAR_LOGSAVE_STOP
{{</message>}}

# Event Notifications

## Current Time

**CURRENT_TIME**

Message representing the current time. Issued by the system every 30 seconds.

{{<message>}}
CURRENT_TIME|hh|mm
{{</message>}}

## Key Input / Mouse Clicks

**DRAGANDDROP**

Emitted when the user drags and drops a file.

{{<message>}}
DRAGANDDROP|(file name)
{{</message>}}

**KEY**

Emitted when the user presses a key.

{{<message>}}
KEY|(key name)
{{</message>}}

**TAPPED**

Emitted when the user clicks or taps.

{{<message>}}
TAPPED|x|y
{{</message>}}

**SCREEN_EVENT_LONGPRESSED, SCREEN_EVENT_LONGRELEASED**

Emitted when the user long-presses the screen. `xxxxx_yyyyy_wwwww_hhhhh` represents the long-press coordinates. `(x,y)` is the pressed coordinate on the screen, `(w,h)` are the screen width and height in pixels.

{{<message>}}
SCREEN_EVENT_LONGPRESSED|xxxxx_yyyyy_wwwww_hhhhh
SCREEN_EVENT_LONGRELEASED|xxxxx_yyyyy_wwwww_hhhhh
{{</message>}}

# Variables

## Variables

**VALUE_SET**

Set a variable value. You can also set a random value within a range. On completion **VALUE_EVENT_SET** is issued.

{{<message>}}
VALUE_SET|(variable alias)|(value)
VALUE_SET|(variable alias)|(minimum value for random)|(maximum value for random)
VALUE_EVENT_SET|(variable alias)
{{</message>}}

**VALUE_GET**

Request a variable's value; it will be issued in a **VALUE_EVENT_GET** message.

{{<message>}}
VALUE_GET|(variable alias)
VALUE_EVENT_GET|(variable alias)|(value)
{{</message>}}

**VALUE_UNSET**

Delete a variable. On completion **VALUE_EVENT_UNSET** is issued.

{{<message>}}
VALUE_UNSET|(variable alias)
VALUE_EVENT_UNSET|(variable alias)
{{</message>}}

**VALUE_EVAL**

Evaluate a variable numerically. Result is issued in **VALUE_EVENT_EVAL**.

{{<message>}}
VALUE_EVAL|(variable alias)|(EQ or NE or LE or LT or GE or GT for evaluation)|(value)
VALUE_EVENT_EVAL|(variable alias)|(EQ or NE or LE or LT or GE or GT for evaluation)|(value)|(TRUE or FALSE)
{{</message>}}

## Countdown Timer

**TIMER_START**

Start a timer variable. Value is in seconds; minimum resolution is 0.1 sec.

- When a timer starts **TIMER_EVENT_START** is issued.
- When the specified time elapses **TIMER_EVENT_STOP** is issued and the timer variable is deleted.
- If a timer with the same name already exists:
  - **TIMER_EVENT_CANCELLED** is issued
  - The value is overwritten
  - **TIMER_EVENT_START** is issued

{{<message>}}
TIMER_START|(count down alias)|(value)
TIMER_EVENT_START|(count down alias)
TIMER_EVENT_STOP|(count down alias)
TIMER_EVENT_CANCELLED|(count down alias)
{{</message>}}

**TIMER_STOP**

Stop a running timer variable.

- If the timer exists **TIMER_EVENT_STOP** is issued.
- If the timer does not exist nothing happens (only a warning is logged).

{{<message>}}
TIMER_STOP|(count down alias)
TIMER_EVENT_STOP|(count down alias)
{{</message>}}

**TIMER_CANCEL**

Forcefully interrupt and delete a timer variable.

- If the specified timer exists it is deleted and **TIMER_EVENT_CANCEL** is issued.
- If it does not exist **TIMER_EVENT_CANCEL** is still issued.

{{<message>}}
TIMER_CANCEL|(count down alias)
TIMER_EVENT_CANCELLED|(count down alias)
{{</message>}}

## Setting KeyValue Values

**KEYVALUE_SET**

Set a KeyValue value by issuing this message.

{{<message>}}
KEYVALUE_SET|(key name)|(value)
{{</message>}}

# Integration

## Open Other Content

**OPEN_CONTENT**

Close the current content and open the specified .mdf.

{{<message>}}
OPEN_CONTENT|relative_mdf_path
{{</message>}}

**FST_LOAD**

Discard the currently running FST and load/start the specified FST.

{{<message>}}
FST_LOAD|(.fst file path)
FST_LOAD|(.fst file path)|(initial state label)
{{</message>}}

**SUBFST_START**, **SUBFST_START_IF**

Start the specified .fst as a sub-FST. SUBFST_START_IF only runs if the file exists (no error if missing).

- When started **SUBFST_EVENT_START** is issued.
- When stopped **SUBFST_EVENT_STOP** is issued.

{{<message>}}
SUBFST_START|(alias)|(.fst file path)
SUBFST_START_IF|(alias)|(.fst file path)
SUBFST_EVENT_START|(alias)
SUBFST_EVENT_STOP|(alias)
{{</message>}}

**SUBFST_STOP**

Force-stop the specified sub-FST.

- On stop **SUBFST_EVENT_STOP** is issued.

{{<message>}}
SUBFST_STOP|(alias)
SUBFST_EVENT_STOP|(alias)
{{</message>}}

## Force-Set Home

**HOME_SET**

Set the current content as home.

{{<message>}}
HOME_SET
{{</message>}}

**HOME_CLEAR**

Clear the home setting.

{{<message>}}
HOME_CLEAR
{{</message>}}

## App Integration

**EXECUTE**

Execute the specified file (Windows only).

{{<message>}}
EXECUTE|(file name)
{{</message>}}

**KEY_POST**

Send a key event to the specified application window (Windows only).

{{<message>}}
KEY_POST|(window class name)|(key name)|(ON or OFF for shift-key)|(ON or OFF for ctrl-key)|(On or OFF for alt-key)
{{</message>}}

## File Download

**NETWORK_GET**

Download a file. On completion **NETWORK_EVENT_GET** is issued.

{{<message>}}
NETWORK_GET|(net alias)|(URI)|(save file name)
NETWORK_EVENT_GET|(net alias)
{{</message>}}

# User Interface

## Button Display

**BUTTON_ADD**

Add a button on the screen. After display completes **BUTTON_EVENT_ADD** is issued.

- 1st arg: alias name (new)
- 2nd arg: display scale
- 3rd arg: display position x,y. Positive = distance from left (bottom); negative = distance from right (top)
- 4th arg: image file
- 5th arg: action ("play", "open", "message", "keyvalueset", ...)
- 6th arg: post-click behavior (ON = auto-close, OFF = keep displayed)

{{<message>}}
BUTTON_ADD|alias|scale|x,y|image path|action|(ON or OFF for autoclose)
BUTTON_EVENT_ADD|alias
{{</message>}}

**BUTTON_DELETE**

Delete a button. After deletion **BUTTON_EVENT_DELETE** is issued.

{{<message>}}
BUTTON_DELETE|alias
BUTTON_EVENT_DELETE|alias
{{</message>}}

**BUTTON_EVENT_EXEC**

Emitted when a button is clicked (tapped).

{{<message>}}
BUTTON_EVENT_EXEC|alias
{{</message>}}

## Add Menu Pages

**MENU|ADD**

Add a new page to the menu. Up to 20 pages including the default. On completion **MENU_EVENT|ADD** is issued.

{{<message>}}
MENU|ADD|(alias)
MENU|ADD|(alias)|backgroundImagePath
MENU_EVENT|ADD|(alias)
{{</message>}}

**MENU|SETITEM**

Register an item at a specified position on a menu page. `id` starts at 0. Up to 30 items per page. On completion **MENU_EVENT|SETITEM** is issued.

{{<message>}}
MENU|SETITEM|(alias)|(id)|(label)|(type)|(arg1)|(arg2)|...
MENU_EVENT|SETITEM|(alias)|(id)
{{</message>}}

**MENU|DELETEITEM**

Delete the item at the specified position on a menu page. On completion **MENU_EVENT|DELETEITEM** is issued.

{{<message>}}
MENU|DELETEITEM|(alias)|(id)
MENU_EVENT|DELETEITEM|(alias)|(id)
{{</message>}}

**MENU|DELETE**

Delete the specified menu page entirely. On completion **MENU_EVENT|DELETE** is issued.

{{<message>}}
MENU|DELETE|(alias)
MENU_EVENT|DELETE|(alias)
{{</message>}}
