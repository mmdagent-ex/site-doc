

---
title: List of Messages
slug: messages
---

# List of Messages

## Overview

The internal modules of MMDAgent are connected in a Spoke and Hub manner

- Messages output from a module are broadcast to all modules
- All messages are delivered to all modules
- Each module can respond to any message and output any message

The following is a list of messages handled by the MMDAgent main body and plugin modules.

All character codes should be in UTF-8.

## Legend

- "()" explains the parameters
- "x,y,z" represents coordinates. As MMDAgent is OpenGL-based, it uses a right-hand coordinate system. The default is 0,0,0.

  ![right handed coordinate system](/images/right-handed.png)

- "rx,ry,rz" are amounts of rotation (unit: degree). The default is 0,0,0.
- "r,g,b" or "r,g,b,a" specifies colors. The values range from 0.0 to 1.0.
- "(A or B ...)" signifies a choice. The default is the first element in the list.

---

# 3D Models

## Adding & Deleting Models

**MODEL_ADD**

Adds a 3D model to the scene. If no parent model is specified, it will be displayed in world coordinates. If a parent model is specified, it can be mounted to that model's bone. Upon completion, it issues a **MODEL_EVENT_ADD**.

- Argument 1: Model alias (new)
- Argument 2: Model file name .pmd
- Argument 3 (optional): Initial coordinates, default 0,0,0
- Argument 4 (optional): Initial rotation, default 0,0,0
- Argument 5 (optional): Whether to use toon rendering, default ON
- Argument 6 (optional): Parent model's model alias
- Argument 7 (optional): Name of the bone to mount on the parent model

{{< message >}}
MODEL_ADD|(model alias)|(model file name)
MODEL_ADD|(model alias)|(model file name)|x,y,z
MODEL_ADD|(model alias)|(model file name)|x,y,z|rx,ry,rz
MODEL_ADD|(model alias)|(model file name)|x,y,z|rx,ry,rz|(ON or OFF for cartoon)
MODEL_ADD|(model alias)|(model file name)|x,y,z|rx,ry,rz|(ON or OFF for cartoon)|(parent model alias)
MODEL_ADD|(model alias)|(model file name)|x,y,z|rx,ry,rz|(ON or OFF for cartoon)|(parent model alias)|(parent bone name)
MODEL_EVENT_ADD|(model alias)
{{< /message >}}

**MODEL_CHANGE, MODEL_CHANGE_ASYNC**

Replaces the currently displayed model. MODEL_CHANGE blocks the process until the model load is finished. MODEL_CHANGE_ASYNC is the asynchronous version, which loads on a separate thread without blocking the main thread. Upon completion of the model swap, it issues a **MODEL_EVENT_CHANGE**.

{{< message >}}
MODEL_CHANGE|(model alias)|(model file name)
MODEL_CHANGE_ASYNC|(model alias)|(model file name)
MODEL_EVENT_CHANGE|(model alias)
{{< /message >}}

**MODEL_DELETE**

Deletes the currently displayed model. Upon deletion completion, it issues a **MODEL_EVENT_DELETE**.

{{< message >}}
MODEL_DELETE|(model alias)
MODEL_EVENT_DELETE|(model alias)
{{< /message >}}

**MODEL_EVENT_SELECT**

Issued when a model is selected by double-clicking.

{{< message >}}
MODEL_EVENT_SELECT|(model alias)
{{< /message >}}

## Motion Playback

A sequence of predefined actions is referred to as a motion. Multiple motions can be played simultaneously on a single model.

**MOTION_ADD**

This adds a motion to the model and starts playback. Each motion is assigned an alias. Upon completion, **MOTION_EVENT_ADD** is generated.

If the specified model does not exist, the system will output a Warning and does nothing.  If a motion of the name is already running, overwrite it.

- Argument 1: Model alias
- Argument 2: Motion alias (new)
- Argument 3: Motion file name .vmd
- Argument 4 (optional): Specifies whether it is normal playback (FULL) or partial playback (PART), default is FULL.
- Argument 5 (optional): Specifies whether it is a single play (ONCE) or loop playback (LOOP), default is ONCE.
- Argument 6 (optional): Smoothing ON / OFF, default is ON
- Argument 7 (optional): Force model coordinates to change at startup OFF / ON, default is OFF
- Argument 8 (optional): Priority when overlapping motions, default is 0

※ If partial playback (PART) is specified, bones that are not actually specified to move in the motion (=only the first frame (frame 0) exists) are excluded from control.

※ Smoothing is applied at the beginning and end when smoothing is ON, making the motion start and end smoothly. Specify OFF if you want to cut it.

※ If you set the forced change of model coordinates in the 7th argument to ON, the coordinate position of the "center" bone of the model is forcibly converted to the root coordinates of the model at the start of playback. Normally, OFF is fine.

{{< message >}}
MOTION_ADD|(model alias)|(motion alias)|(motion file name)
MOTION_ADD|(model alias)|(motion alias)|(motion file name)|(FULL or PART)
MOTION_ADD|(model alias)|(motion alias)|(motion file name)|(FULL or PART)|(ONCE or LOOP)
MOTION_ADD|(model alias)|(motion alias)|(motion file name)|(FULL or PART)|(ONCE or LOOP)|(ON or OFF for smooth)
MOTION_ADD|(model alias)|(motion alias)|(motion file name)|(FULL or PART)|(ONCE or LOOP)|(ON or OFF for smooth)|(OFF or ON for reposition)
MOTION_ADD|(model alias)|(motion alias)|(motion file name)|(FULL or PART)|(ONCE or LOOP)|(ON or OFF for smooth)|(OFF or ON for reposition)|priority
MOTION_EVENT_ADD|(model alias)|(motion alias)
{{< /message >}}

**MOTION_CHANGE**

Replaces the motion being played with another motion. Upon replacement completion, **MOTION_EVENT_CHANGE** is generated.

{{< message >}}
MOTION_CHANGE|(model alias)|(motion alias)|(motion file name)
MOTION_EVENT_CHANGE|(model alias)|(motion alias)
{{< /message >}}

**MOTION_RESET**

Restarts the playback of the motion from the initial frame.

{{< message >}}
MOTION_RESET|(model alias)|(motion alias)
{{< /message >}}

**MOTION_DELETE**

Interrupts and deletes the motion playback. Upon completion, **MOTION_EVENT_DELETE** is generated.
No output (just warning on log) when the specified motion does not being played.

{{< message >}}
MOTION_DELETE|(model alias)|(motion alias)
MOTION_EVENT_DELETE|(model alias)|(motion alias)
{{< /message >}}

**MOTION_ACCELERATE**

Gradually changes the playback speed of the motion towards a specified frame. Upon change completion, **MOTION_EVENT_ACCELERATE** is generated.

- speed: The target playback speed. Relative speed with the standard being 1.0. Stops at 0.0.
- duration: The time it takes to change speed towards the target (in seconds)
- target: The frame on the motion that is the target (in seconds)

{{< message >}}
MOTION_ACCELERATE|(model alias)|(motion alias)|(speed)|(duration)|(target)
MOTION_EVENT_ACCELERATE|(model alias)|(motion alias)
{{< /message >}}

## Motion Layering Adjustment

Setting for layering multiple motions. When layering, the motions are calculated in order from lowest to highest priority, and values are set for the bones and morphs targeted by each motion. You can set the behavior at this time. The default is "overwrite (replace)", but this can be changed to addition (add) or none (ignore). While you can specify this on a per-motion basis, it's also possible to set it more granularly on a per-bone basis.

**MOTION_CONFIGURE**

Sets the behavior during layering for existing motions.

- Argument 1: Model alias
- Argument 2: Motion alias
- Argument 3: Setting label (see below)
- Argument 4 onward: Parameters (dependent on the setting label)

The possible setting labels are as follows. Let's call the current value rs and the value specified by this motion rd. If you set the rate, you can also set the blend rate at the same time.

- **MODE_REPLACE**: Overwrite (rd)
- **MODE_ADD**: Addition (rs + rd)
- **MODE_MUL**: Morphs are multiplied (rs * rd), bones are overwritten
- **BLEND_RATE**: Only sets the blend rate (rd' = rd * blend rate)

{{< message >}}
MOTION_CONFIGURE|(model)|(motion)|MODE_REPLACE
MOTION_CONFIGURE|(model)|(motion)|MODE_REPLACE|(rate)
MOTION_CONFIGURE|(model)|(motion)|MODE_ADD
MOTION_CONFIGURE|(model)|(motion)|MODE_ADD|(rate)
MOTION_CONFIGURE|(model)|(motion)|MODE_MUL
MOTION_CONFIGURE|(model)|(motion)|MODE_MUL|(rate)
MOTION_CONFIGURE|(model)|(motion)|BLEND_RATE|(rate)
{{< /message >}}

To specify individually for each bone:

- **MODE_BONE_REPLACE**: Set specified bone to overwrite
- **MODE_BONE_ADD**: Set specified bone to add
- **MODE_BONE_NONE**: Set specified bone to no effect (skip)
- **MODE_FACE_REPLACE**: Set specified morph to overwrite
- **MODE_FACE_ADD**: Set specified morph to add
- **MODE_FACE_MUL**: Set specified morph to multiply
- **MODE_FACE_NONE**: Set specified morph to no effect (skip)

{{< message >}}
MOTION_CONFIGURE|(model alias)|(motion alias)|MODE_BONE_REPLACE|bonename[,bonename,..]
MOTION_CONFIGURE|(model alias)|(motion alias)|MODE_BONE_ADD|bonename[,bonename,..]
MOTION_CONFIGURE|(model alias)|(motion alias)|MODE_BONE_NONE|bonename[,bonename,..]
MOTION_CONFIGURE|(model alias)|(motion alias)|MODE_FACE_REPLACE|morphname[,morphname,..]
MOTION_CONFIGURE|(model alias)|(motion alias)|MODE_FACE_ADD|morphname[,morphname,..]
MOTION_CONFIGURE|(model alias)|(motion alias)|MODE_FACE_MUL|morphname[,morphname,..]
MOTION_CONFIGURE|(model alias)|(motion alias)|MODE_FACE_NONE|bonename[,bonename,..]
{{< /message >}}

Upon completing the settings, issue **MOTION_EVENT_CONFIGURE**.

{{< message >}}
MOTION_EVENT_CONFIGURE|(model alias)|(motion alias)
{{< /message >}}

## Individual Bone & Morph Control

Methods for controlling a model's bones and morphs externally, aside from motion.

**MODEL_BINDBONE**

Set values to the bone. There are two methods to specify: fixed values and binding to KeyValue values. If the bone is under motion control, the motion side will take precedence. After execution, it will issue **MODEL_EVENT_BINDBONE**. The values are applied immediately.

- **Fixed Values**: Specify the amount of movement and rotation numerically.

{{< message >}}
MODEL_BINDBONE|(model alias)|(bone name)|x,y,z|rx,ry,rz
{{< /message >}}

- **KeyValue Value Binding**: After the setting, it will start to respond in real-time to the key values of the specified KeyValue.

{{< message >}}
MODEL_BINDBONE|(key name)|(min)|(max)|(model alias)|(bone name)|x1,y1,z1|rx1,ry1,rz1|x2,y2,z2|rx2,ry2,rz2
{{< /message >}}

The parameter values of the specified part will be determined as follows, between the two given parameters, according to the changes in the KeyValue values.

![BindBone](/images/bindbone.png)

**MODEL_BINDFACE**

Set the values of the morph. Similar to the bone, there are two methods to specify: fixed values and binding to KeyValue values. If the morph is under motion control, the motion side will take precedence. It will issue **MODEL_EVENT_BINDFACE** at the end.

- **Fixed Values**: Specify the amount of change numerically. The values are immediately applied. When `transition_duration` is specified, it will change slowly over the specified time.

{{< message >}}
MODEL_BINDFACE|(model alias)|(morph name)|(value)
MODEL_BINDFACE|(model alias)|(morph name)|(value)|(transition_duration)
{{< /message >}}


- **KeyValue Value Binding**: After the setting, it will start to respond in real-time to the key values of the specified KeyValue. After the setting execution, it will issue **MODEL_EVENT_BINDBONE**.

{{< message >}}
MODEL_BINDFACE|(key name)|(min)|(max)|(model alias)|(morph name)|rate1|rate2
{{< /message >}}

**MODEL_UNBINDBONE**

Unbind the specified bone. It will issue **MODEL_EVENT_UNBINDBONE** at the end.

{{< message >}}
MODEL_UNBINDBONE|(model alias)|(bone name)
MODEL_EVENT_UNBINDBONE|(model alias)|(bone name)
{{< /message >}}

**MODEL_UNBINDFACE**

Unbind the specified morph. It will issue **MODEL_EVENT_UNBINDFACE** at the end.

{{< message >}}
MODEL_UNBINDFACE|(model alias)|(morph name)
MODEL_EVENT_UNBINDFACE|(model alias)|(morph name)
{{< /message >}}

## Moving the Model's Display Position

In the following, `GLOBAL` refers to the world coordinate system, and `LOCAL` refers to the model coordinate system when specifying coordinates.

**MOVE_START, MOVE_STOP**

Smoothly move the model to the specified coordinates. The movement can be interrupted with MOVE_STOP. At the start of the movement, a **MOVE_EVENT_START** is issued, and at the end or when interrupted, a **MOVE_EVENT_STOP** is issued.

If a move speed is specified, the model will move at a constant speed (distance/second) to the specified coordinates.

{{< message >}}
MOVE_START|(model alias)|x,y,z
MOVE_START|(model alias)|x,y,z|(GLOBAL or LOCAL position)
MOVE_START|(model alias)|x,y,z|(GLOBAL or LOCAL position)|(move speed)
MOVE_STOP|(model alias)
MOVE_EVENT_START|(model alias)
MOVE_EVENT_STOP|(model alias)
{{< /message >}}

**TURN_START, TURN_STOP**

Rotates the model so that the specified coordinates are at the front. The rotation can be interrupted with TURN_STOP. A **TURN_EVENT_START** is issued at the start of the rotation, and a **TURN_EVENT_STOP** is issued when it ends or is interrupted.

If a rotation speed is specified, the model will rotate at a constant speed (degrees/second).

{{< message >}}
TURN_START|(model alias)|x,y,z
TURN_START|(model alias)|x,y,z|(GLOBAL or LOCAL position)
TURN_START|(model alias)|x,y,z|(GLOBAL or LOCAL position)|(rotation speed)
TURN_STOP|(model alias)
TURN_EVENT_START|(model alias)
TURN_EVENT_STOP|(model alias)
{{< /message >}}

**ROTATE_START, ROTATE_STOP**

Rotates the model by the specified rotation amount. The rotation can be interrupted with ROTATE_STOP. A **ROTATE_EVENT_START** is issued at the start of the rotation, and a **ROTATE_EVENT_STOP** is issued when it ends or is interrupted.

If a rotation speed is specified, the model will rotate at a constant speed (degrees/second).

{{< message >}}
ROTATE_START|(model alias)|rx,ry,rz
ROTATE_START|(model alias)|rx,ry,rz|(GLOBAL or LOCAL rotation)
ROTATE_START|(model alias)|rx,ry,rz|(GLOBAL or LOCAL rotation)|(rotation speed)
ROTATE_STOP|(model alias)
ROTATE_EVENT_START|(model alias)
ROTATE_EVENT_STOP|(model alias)
{{< /message >}}

## Executing Texture Animation

**TEXTURE_SETANIMATIONRATE**

Change the animation speed of Animation PNG (APNG) textures individually.

- `textureFileName` should match the texture specification string within the model.
- `rate` is standard at 1.0, half at 0.5, double at 2.0, and stopped at 0.0.

{{< message >}}
TEXTURE_SETANIMATIONRATE|model alias|textureFileName|rate
{{< /message >}}

## Parallel Skinning Configuration

**CONFIG_PARALLELSKINNING_THREADS**

Change the number of threads used for parallel skinning. You can specify a number from 1 to 4, with the default being the value set in the .mdf file.

※ Changing the number of parallel threads while the system is running may cause instability. If it doesn't work well, it is recommended to specify the number of threads at startup with `parallel_skinning_numthreads=2` in the .mdf file.

{{< message >}}
CONFIG_PARALLELSKINNING_THREADS|2
{{< /message >}}

## Capture Motion to File

**MOTIONCAPTURE_START, MOTIONCAPTURE_STOP**

Capture and record the model's movements as a motion file (.vmd).

{{< message >}}
MOTIONCAPTURE_START|model alias|filename.vmd
MOTIONCAPTURE_STOP|model alias
{{< /message >}}

# Screen Layout

## Viewpoint (Camera)

**CAMERA**

Change the viewpoint. There are three ways to specify it.

**Specify by Numbers**: Specify parameters with `x,y,z|rx,ry,rz|(distance)|(fovy)`. These values can be set based on the values that appear at the bottom left when the simple log is displayed using the `D` key. The transition time period specifies how the viewpoint changes to the specified point. The default (-1) smoothly transitions the viewpoint, 0 jumps immediately, and a value greater than 0 transitions to the specified coordinates over that number of seconds.

{{< message >}}
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)|(transition time period)
{{< /message >}}

**Mount to Model**: Make the camera follow the model's movements in real time. If no bone name is specified, it will follow the "center" bone.

{{< message >}}
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)|(transition time period)|(model alias)
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)|(transition time period)|(model alias)|(bone name)
{{< /message >}}

**Specify with Motion**: Start the camera's movements by specifying a predefined camera motion file (.vmd).

{{< message >}}
CAMERA|(camera motion file name)
{{< /message >}}

## Background & Floor

**STAGE**

Specify and change the images for the background and floor, or the 3D model for the stage. The display size of the background and floor is specified by `stage_size` in .mdf. The images will be stretched to fit the specified size.

{{< message >}}
STAGE|(floor image file),(back image file)
STAGE|(stage file .xpmd or .pmd)
{{< /message >}}

## Foreground image overlay (Frame)

**WINDOWFRAME**

Overlay a frame image (.png) on top of the screen. The image will be stretched to fit the screen's aspect ratio.

![frame](/images/frame.png)

{{< message >}}
WINDOWFRAME|filename.png
{{< /message >}}

Deleting the frame that was specified by **WINDOWFRAME** above:

{{< message >}}
WINDOWFRAME|NONE
{{< /message >}}

**WINDOWFRAME_ADD**

Add a frame image (.png).  Specify an alias name.  When success, **WINDOWFRAME_EVENT_ADD** will be issued.  Use the same existing name to swap the current image to the new one.

{{< message >}}
WINDOWFRAME_ADD|frame1|filename.png
WINDOWFRAME_EVENT_ADD|frame1
{{< /message >}}

**WINDOWFRAME_DELETE**

Delete the specified frame image.  When success, **WINDOWFRAME_EVENT_DELETE** will be issued.

{{< message >}}
WINDOWFRAME_DELETE|frame1
WINDOWFRAME_EVENT_DELETE|frame1
{{< /message >}}

**WINDOWFRAME_DELETEALL**

Totally delete all frame images.

{{< message >}}
WINDOWFRAME_DELETEALL
{{< /message >}}


## Transparent Window (Win)

**TRANSPARENT_START**

(Windows only) Make app window transparent.  The transparent color can be specified.  If the color is not specified, the default value will be used.  (default value is the color specified by `transparent_color=` in .mdf, or `0.0,1.0,0.0`)

{{< message >}}
TRANSPARENT_START
TRANSPARENT_START|r,g,b
{{< /message >}}

**TRANSPARENT_STOP**

(Windows only) Reset transparency and revert to normal window.

{{< message >}}
TRANSPARENT_STOP
{{< /message >}}

## Light Source

**LIGHTCOLOR**

Change the direction and color of the light source.

{{< message >}}
LIGHTDIRECTION|x,y,z
LIGHTCOLOR|r,g,b
{{< /message >}}

# Displaying Text & Images

## Displaying Text, Images, and Camera Footage

It is possible to display any text, images, or live camera footage within a 3D space.

The steps involve defining a display area with **TEXTAREA_ADD**, and then specifying the content to display in that area with **TEXTAREA_SET**. By repeatedly using **TEXTAREA_SET**, you can change the content in the same location.

**TEXTAREA_ADD**

This command adds a new area. You can specify its size, color, coordinates, and orientation. The coordinates designate the center of the area. You can also 'place' it on a parent model.

When the addition is complete, **TEXTAREA_EVENT_ADD** is triggered.

- Argument 1: Alias name (new)
- Argument 2: Width and height
  - Positive values: Fixed size (If the content overflows, it will be reduced to fit)
  - 0: Variable size: Automatically adjusted according to the content. For images, the aspect ratio is maintained.
- Argument 3: Text size, margin, line spacing. The base value for each is 1.0.
- Argument 4: Background color r,g,b,a. With a = 0, there is no background.
- Argument 5: Text color r,g,b,a
- Argument 6: Center coordinates
- Argument 7 (optional): Orientation (amount of rotation)
- Argument 8 (optional): Parent model's alias
- Argument 9 (optional): Name of the bone to mount on the parent model (If omitted, 'center' is used)

{{< message >}}
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z|rx,ry,rz
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z|rx,ry,rz|(parent model alias)
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z|rx,ry,rz|(parent model alias)|(parent bone name)
TEXTAREA_EVENT_ADD|alias
{{< /message >}}


**TEXTAREA_SET**

This command displays text or an image in the area. **TEXTAREA_EVENT_SET** is issued at the start of the display. If something is already displayed, it will be replaced.

The content to display is specified in the second argument:

- If you **write a string**, that string will be displayed. If the string includes spaces, enclose it in "". You can also break lines with "\n".
- If you **write the path of an image file**, that image will be displayed.

{{< message >}}
TEXTAREA_SET|(textarea alias)|(string or image path)
TEXTAREA_EVENT_SET|alias
{{< /message >}}

{{<hint ms>}}

- specify `__camera0` to open webcam (number = camera id)

You can also change camera resolution by setting `Plugin_TextArea_Camera_Size` in .mdf.

{{<mdf>}}
Plugin_TextArea_Camera_Size=1280x720
{{</mdf>}}

Note: When using a high-resolution webcam, it may take tens of seconds or more to start, due to OpenCV's specifications. In such cases, you can bipass some initialization step and may be able to make the start up delay much smaller by setting the environment variable `OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS` to `0`.

{{</hint>}}

**TEXTAREA_DELETE**

This command deletes the area and removes the display. When the deletion is complete, **TEXTAREA_EVENT_DELETE** is issued.

{{< message >}}
TEXTAREA_DELETE|(textarea alias)
TEXTAREA_EVENT_DELETE|alias
{{< /message >}}

{{< hint ms >}}

**TEXTAREA_HIDE**

Hide the text area from scene.  A hided TextArea exists but will not be rendered.

{{< message >}}
TEXTAREA_HIDE|(textarea alias)
TEXTAREA_EVENT_HIDE|alias
{{< /message >}}

**TEXTAREA_SHOW**

Re-start showing a hided text area from scene.

{{< message >}}
TEXTAREA_SHOW|(textarea alias)
TEXTAREA_EVENT_SHOW|alias
{{< /message >}}

{{< /hint >}}

## Text Caption

Display text caption. Differences from the above TextArea:

- On-screen display, not in 3D space (displayed at a fixed position regardless of viewpoint)
- Any font can be specified
- Up to two types of text outlining can be specified
- Can be set to automatically disappear after a specified time
- (v1.0.2) support lyric file (.lrc) play

![caption](/images/caption.png)

**CAPTION_SETSTYLE**

Defines the style. After defining, issue **CAPTION_EVENT_SETSTYLE**.

- First argument: New alias name for the style
- Second argument: The path to the font file. The system font can be used by specifying "default"
- Third argument: Text color r,g,b,a
- Fourth argument (optional): Color and size of the first outline r,g,b,a,thickness. If no outline is needed, set a or thickness to 0
- Fifth argument (optional): Color and size of the second outline, specified in the same way
- Sixth argument (optional): Frame background color r,g,b,a. If not needed, set a to 0

(v1.0.2) The fourth and subsequent arguments can be omitted altogether. If omitted, MMDAgent-EX will apply default style for the edges.

{{< message >}}
CAPTION_SETSTYLE|style_alias|fontpath|r,g,b,a
CAPTION_SETSTYLE|style_alias|fontpath|r,g,b,a|edge1|edge2|basecolor
CAPTION_EVENT_SETSTYLE|style_alias
{{< /message >}}

**CAPTION_START**

Starts text display with a style. If already displayed, swap its text. It will disappear when **CAPTION_STOP** is issued or after the time specified with `duration`.

(v1.0.2) Specify "file.lrc" instead of text to start playing .lrc file as captions.

- First argument: New alias name
- Second argument: Style name.  Either one defined in **CAPTION_SETSTYLE**, or "_default" (v1.0.2)
- Third argument: The text to display. If it includes a space, surround it with "". You can also use "\n" to break lines. (v1.0.2) or LRC file path (file.lrc)
- Fourth argument: Text size
- Fifth argument: Left/right position of the display. Specify either CENTER, LEFT, RIGHT
- Sixth argument: Up/down position of the display. Use relative values where the bottom of the screen is 0.0 and the top is 1.0
- Seventh argument: Display duration in number of frames (30=1 second)

{{< message >}}
CAPTION_START|alias|style_alias|text|size|align|height|duration
(v1.0.2) CAPTION_START|alias|style|file.lrc|size|align|height|duration
CAPTION_EVENT_START|alias
CAPTION_EVENT_STOP|alias
{{< /message >}}

Example of use:

{{< message >}}
10 10:
    KEY|1 CAPTION_SETSTYLE|terop|rounded-mplus-1c-heavy.ttf|1,0.5,0,1|1,1,1,1,4|0,0,0,0.6,6|0,0,0,0
    CAPTION_EVENT_SETSTYLE|terop CAPTION_START|test|terop|てすと|3.0|CENTER|0.5|300
{{< /message >}}

**CAPTION_STOP**

Force delete the displayed text. On success, issues **CAPTION_EVENT_STOP**.

{{< message >}}
CAPTION_STOP|alias
CAPTION_EVENT_STOP|alias
{{< /message >}}

## Notification

**NOTIFY_SHOW**

Displays a system message on the screen. Disappears after 2.0 seconds.

{{< message >}}
 NOTIFY_SHOW|(text)
{{< /message >}}

It's also possible to change the duration.

{{< message >}}
 NOTIFY_SHOW|(text)|(seconds)
{{< /message >}}

## Prompting a Text Prompt and Obtaining User's Response

**PROMPT_SHOW**

Displays a message dialog and lets the user make a selection. If the specified text contains blank spaces, enclose it with "". The maximum number of options is 15.

{{< message >}}
PROMPT_SHOW|(main text)|(item text 0)|(item text 1)|...
{{< /message >}}

Example:

{{< message >}}
PROMPT_SHOW|"main text"|item1|item2|item3
{{< /message >}}

![prompt](/images/prompt.png)

When the user selects any of the items, **PROMPT_EVENT_SELECTED** is issued together with the number of the selected item (0～) and this dialog disappears. If the selection is cancelled (clicking outside the dialog or ESC key), -1 is returned.

{{< message >}}
PROMPT_EVENT_SELECTED|(selected number or -1 for cancel)
{{< /message >}}

## Displaying Documents in Full Screen to Gather User Reactions

**INFOTEXT_FILE**

This displays the contents of a text file in full screen. When the display starts, **INFORTEXT_EVENT_SHOW** is issued.

- Argument 1: Path of the text file
- Argument 2: Title label
- Argument 3: Selection button labels, separated by commas. Example: "Yes,No,Cancel"
- Argument 4 (optional): Text scale (default: 1.0)
- Argument 5 (optional): Background color in hexadecimal "RRGGBBAA". Example: white=FFFFFFFF
- Argument 6 (optional): Text color, same as above.

The displayed document can be scrolled by dragging (swiping).

The labels specified in the third argument are displayed at the bottom. When a user makes a selection, the display ends, and **INFOTEXT_EVENT_CLOSE** is issued along with the index of the selected button.

Example: Display README.txt

{{< message >}}
INFOTEXT_FILE|README.md|"This is readme"|OK,Cancel
{{< /message >}}

![infotext](/images/infotext.png)

{{< message >}}
INFOTEXT_FILE|(filepath)|(titleLabel)|(buttonLabels)
INFOTEXT_FILE|(filepath)|(titleLabel)|(buttonLabels)|(scale)
INFOTEXT_FILE|(filepath)|(titleLabel)|(buttonLabels)|(scale)|(BACKGROUNDCOLOR)|(TEXTCOLOR)
INFOTEXT_EVENT_SHOW
INFOTEXT_EVENT_CLOSE|(selectedButtonLabel)
{{< /message >}}


**INFOTEXT_STRING**

This directly specifies a string and displays it on the screen in full screen.

- Argument 1: Text content (string)
- Argument 2: Title label
- Argument 3: Selection button labels. Example: "Yes,No,Cancel"
- Argument 4 (optional): Text scale (default: 1.0)
- Argument 5 (optional): Background color in hexadecimal "RRGGBBAA". Example: white=FFFFFFFF
- Argument 6 (optional): Text color, same as above.

The selection button labels appear as buttons at the bottom of the screen, and multiple can be specified by separating them with commas. The display ends when one is pressed.

When the display is complete, **INFORTEXT_EVENT_SHOW** is issued, and when a button is selected and the display ends, **INFORTEXT_EVENT_CLOSE** is issued along with the index of the selected button.

{{< message >}}
INFOTEXT_STRING|textbody|(titleLabel)|(buttonLabels)
INFOTEXT_STRING|textbody|(titleLabel)|(buttonLabels)|(scale)
INFOTEXT_STRING|textbody|(titleLabel)|(buttonLabels)|(scale)|(BACKGROUNDCOLOR)|(TEXTCOLOR)
INFOTEXT_EVENT_SHOW
INFOTEXT_EVENT_CLOSE|(selectedButtonLabel)
{{< /message >}}

# Audio

## Sound Playback

**SOUND_START**

This initiates the playback of a sound file. mp3 and wav formats are supported. When playback starts, **SOUND_EVENT_START** is issued, and when it ends, **SOUND_EVENT_STOP** is issued.

{{< message >}}
SOUND_START|(sound alias)|(sound file name)
SOUND_EVENT_START|(sound alias)
SOUND_EVENT_STOP|(sound alias)
{{< /message >}}

**SOUND_STOP**

This forcibly interrupts the sound that is currently playing. At the time of interruption, **SOUND_EVENT_STOP** is issued.

{{< message >}}
SOUND_STOP|(sound alias)
SOUND_EVENT_STOP|(sound alias)
{{< /message >}}

## Voice Playback with Lip Sync

**SPEAK_START**

This makes the specified model speak the audio file. Lip sync is performed simultaneously with playback. When playback starts, **SPEAK_EVENT_START** is issued, and when it ends, **SPEAK_EVENT_STOP** is issued. .shapemap configuration is required.

{{< message >}}
SPEAK_START|(model alias)|(audio file)
SPEAK_EVENT_START|(model alias)
SPEAK_EVENT_STOP|(model alias)
{{< /message >}}


**SPEAK_STOP**

Stops the playing speech formaly started by **SPEAK_START** immediately.  **SPEAK_EVENT_STOP** will be issued whenever it has been processed successfully (i.e. stopped the playing audio or no audio was played at that time) 

{{< message >}}
SPEAK_STOP|(model alias)
SPEAK_EVENT_STOP|(model alias)
{{< /message >}}


## Voice Recognition

The content of the message changes depending on the module or plugin used.

### Common

**RECOG_EVENT_START**

This message is issued at the start of voice input.

{{< message >}}
RECOG_EVENT_START
{{< /message >}}

**RECOG_EVENT_STOP**

This message is issued when voice recognition results are obtained.

{{< message >}}
RECOG_EVENT_STOP|String of recognition results
{{< /message >}}

### Plugin_Julius

**RECOG_EVENT_OVERFLOW**

Emitted when the level of the input sound is too large and causes an overflow.

{{< message >}}
RECOG_EVENT_OVERFLOW
{{< /message >}}

**RECOG_EVENT_MODIFY**

Emitted when the processing of the RECOG_MODIFY message is complete.

{{< message >}}
RECOG_EVENT_MODIFY|GAIN
RECOG_EVENT_MODIFY|USERDICT_SET
RECOG_EVENT_MODIFY|USERDICT_UNSET
RECOG_EVENT_MODIFY|CHANGE_CONF|(jconf_file_prefix)
{{< /message >}}

**RECOG_EVENT_AWAY**

Emitted when speech recognition is paused (ON) or resumed (OFF) due to menu operations or external control.

{{< message >}}
RECOG_EVENT_AWAY|ON
RECOG_EVENT_AWAY|OFF
{{< /message >}}

**RECOG_EVENT_GMM**

Output of the identification result tag when using Julius's environmental sound identification function.

{{< message >}}
RECOG_EVENT_GMM|noise
{{< /message >}}

**RECOG_MODIFY**

Engine configuration change command. Dynamically changes the running engine.

- `GAIN`: Amplitude scaling factor of input sound (default 1.0)
- `USERDICT_SET`: Loads user dictionary (if already loaded, replaces)
- `USERDICT_UNSET`: Deletes user dictionary
- `CHANGE_CONF`: Restarts the engine with the specified jconf configuration file

{{< message >}}
RECOG_EVENT_MODIFY|GAIN|(scale)
RECOG_EVENT_MODIFY|USERDICT_SET|(dict_file_path)
RECOG_EVENT_MODIFY|USERDICT_UNSET
RECOG_EVENT_MODIFY|CHANGE_CONF|(jconf_file_prefix)
{{< /message >}}

**RECOG_RECORD_START**

Starts automatic recording of input sound. The cut-out sound fragments are sequentially saved as individual .wav files in the specified directory.

{{< message >}}
RECOG_RECORD_START|(directory)
{{< /message >}}

**RECOG_RECORD_STOP**

Stops automatic recording of input sound.

{{< message >}}
RECOG_RECORD_STOP
{{< /message >}}

## Speech Synthesis

The content of the message changes depending on the module or plugin used.

### Common

**SYNTH_START**

Starts speech synthesis. The specified model lip-syncs according to the pronunciation. **SYNTH_EVENT_START** is issued when the synthesized speech begins to output, and **SYNTH_EVENT_STOP** is issued when the output ends.

{{< message >}}
SYNTH_START|(model alias)|(voice alias)|(synthesized text)
SYNTH_EVENT_START|(model alias)
SYNTH_EVENT_STOP|(model alias)
{{< /message >}}

**SYNTH_STOP**

Forcibly interrupts the output of speech synthesis. **SYNTH_EVENT_STOP** is issued when it is interrupted.

{{< message >}}
SYNTH_STOP|(model alias)
SYNTH_EVENT_STOP|(model alias)
{{< /message >}}

### Plugin_Open_JTalk

Japanese speech synthesis engine.

{{< message >}}
LIPSYNC_START|(model alias)|(phoneme and millisecond pair sequence)
LIPSYNC_STOP|(model alias)
LIPSYNC_EVENT_START|(model alias)
LIPSYNC_EVENT_STOP|(model alias)
{{< /message >}}

# External Operation (Plugin_Remote)

## Control & Operation

**AVATAR|START, AVATAR|STOP**

Messages that are issued when the start command `__AV_START` or the end command `__AV_END` is received from the external control API to start or end external control of the model.

{{< message >}}
AVATAR|START
AVATAR|STOP
{{< /message >}}

**AVATAR_CONTROL**

Temporarily pause or resume controlling the model based on commands from the external control API. After processing, issue **AVATAR_EVENT_CONTROL**.

- **DISABLE**: Temporarily disable
- **ENABLE**: Terminate disabling and resume

{{< message >}}
AVATAR_CONTROL|DISABLE
AVATAR_EVENT_CONTROL|DISABLED
AVATAR_CONTROL|ENABLE
AVATAR_EVENT_CONTROL|ENABLED
{{< /message >}}

**REMOTEKEY_CHAR, REMOTEKEY_DOWN, REMOTEKEY_UP**

Messages that send keyboard inputs from the outside.

{{< message >}}
REMOTEKEY_CHAR|(character)
REMOTEKEY_DOWN|(key code string)
REMOTEKEY_UP|(key code string)
{{< /message >}}

{{< hint ms >}}
## Screen Transmission

**SCREENENCODE_START, SCREENENCODE_STOP**

Start sending screen captures and web camera captures.

{{< message >}}
SCREENENCODE_START|(ID of camera, -1 to disable)|bitrate|fps|base_width|base_height|camera_zoomrate
SCREENENCODE_STOP
SCREENENCODE_EVENT_START
SCREENENCODE_EVENT_STOP
{{< /message >}}

## File Transmission

**REMOTE_TRANSFILE**

Receive a file from remote end.

The procedure of file transmission as seen from the remote side is as follows:

- Send **REMOTE_TRANSFILE** message to MMDAgent-EX and wait for return message.
- When **REMOTE_TRANSFILE_PREPARED** has been sent from MMDAgent-EX, newly open the WebSocket channel of the name specified by the returned message, and send the file body with binary mode.
- When **REMOTE_TRANSFILE_FINISHED** has been received, close the transmission channel.

{{< message >}}
REMOTE_TRANSFILE|fileName
REMOTE_TRANSFILE_PREPARED|channelNameForTransmission|fileName
REMOTE_TRANSFILE_FINISHED|channelNameForTransmission|fileName
{{< /message >}}

{{< /hint >}}

## Operation Log Recording

**AVATAR_LOGSAVE_START, AVATAR_LOGSAVE_STOP**

Record all control commands from the outside to a file. Start with **AVATAR_LOGSAVE_START**, end with **AVATAR_LOGSAVE_STOP**.

{{< message >}}
AVATAR_LOGSAVE_START|filename
AVATAR_LOGSAVE_STOP
{{< /message >}}

# Event Notification

## Current Time

**CURRENT_TIME**

A message indicating the current time. It is issued by the system every 30 seconds.

{{< message >}}
CURRENT_TIME|hh|mm
{{< /message >}}

## Key Input & Mouse Click

**DRAGANDDROP**

A message issued when the user drags and drops a file.

{{< message >}}
DRAGANDDROP|(file name)
{{< /message >}}

**KEY**

A message issued when the user presses a key.

{{< message >}}
KEY|(key name)
{{< /message >}}

**TAPPED**

A message issued when the user clicks the mouse or taps.

{{< message >}}
TAPPED|x|y
{{< /message >}}

**SCREEN_EVENT_LONGPRESSED, SCREEN_EVENT_LONGRELEASED**

A message issued when the user long presses the screen. `xxxxx_yyyyy_wwwww_hhhhh` represents the coordinates of the long press. `(x,y)` are the coordinates of the long press on the screen, `(w,h)` are the width and height of the screen, in pixels.

{{< message >}}
SCREEN_EVENT_LONGPRESSED|xxxxx_yyyyy_wwwww_hhhhh
SCREEN_EVENT_LONGRELEASED|xxxxx_yyyyy_wwwww_hhhhh
{{< /message >}}

# Variables

## Variables

**VALUE_SET**

Set a value to a variable. You can also set a random value within a specified range.
Upon completion, it issues a **VALUE_EVENT_SET**.

{{< message >}}
VALUE_SET|(variable alias)|(value)
VALUE_SET|(variable alias)|(minimum value for random)|(maximum value for random)
VALUE_EVENT_SET|(variable alias)
{{< /message >}}

**VALUE_GET**

Get the value of a variable and issue **VALUE_EVENT_GET**.

{{<message>}}
VALUE_GET|(variable alias)
VALUE_EVENT_GET|(variable alias)|(value)
{{</message>}}

**VALUE_UNSET**

Delete a variable. Upon completion, it issues a **VALUE_EVENT_UNSET**.

{{< message >}}
VALUE_UNSET|(variable alias)
VALUE_EVENT_UNSET|(variable alias)
{{< /message >}}

**VALUE_EVAL**

Evaluate the variable as a number. The result is issued with **VALUE_EVENT_EVAL**.

{{< message >}}
VALUE_EVAL|(variable alias)|(EQ or NE or LE or LT or GE or GT for evaluation)|(value)
VALUE_EVENT_EVAL|(variable alias)|(EQ or NE or LE or LT or GE or GT for evaluation)|(value)|(TRUE or FALSE)
{{< /message >}}

## Countdown Timer

**TIMER_START**

Start a timer variable. The value is in seconds, with a minimum resolution of 0.1 seconds.

- When the timer starts, it issues a **TIMER_EVENT_START**
- When the specified time has passed, it issues a **TIMER_EVENT_STOP** and the timer variable is deleted.
- If a timer variable with the same name already exists,
  - It issues a **TIMER_EVENT_CANCELLED**
  - Overwrites the value
  - Issues a **TIMER_EVENT_START**

{{< message >}}
TIMER_START|(count down alias)|(value)
TIMER_EVENT_START|(count down alias)
TIMER_EVENT_STOP|(count down alias)
TIMER_EVENT_CANCELLED|(count down alias)
{{< /message >}}

**TIMER_STOP**

Stop a running timer variable.

- If a timer variable exists, it issues a **TIMER_EVENT_STOP**
- If a timer variable does not exist, it does nothing (only outputs a warning)

{{< message >}}
TIMER_STOP|(count down alias)
TIMER_EVENT_STOP|(count down alias)
{{< /message >}}

**TIMER_CANCEL**

Forcefully interrupt and delete a timer variable.

- If the specified timer variable exists, it deletes it and issues a **TIMER_EVENT_CANCEL**
- If the specified timer variable does not exist, it still issues a **TIMER_EVENT_CANCEL**

{{< message >}}
TIMER_CANCEL|(count down alias)
TIMER_EVENT_CANCELLED|(count down alias)
{{< /message >}}

{{< hint ms >}}

**TIMER_PAUSE**

Pause a timer variable.  Paused time does not proceed till **TIMER_RESUME**.

Doing multiple pauses does not count: can be resumed by a single **TIMER_RESUME**.

{{< message >}}
TIMER_PAUSE|(count down alias)
{{< /message >}}

**TIMER_RESUME**

Resume a paused timer variable.

{{< message >}}
TIMER_RESUME|(count down alias)
{{< /message >}}

{{< /hint >}}

## Setting KeyValue Values

**KEYVALUE_SET**

By issuing this message, you can set KeyValue values.

{{< message >}}
KEYVALUE_SET|(key name)|(value)
{{< /message >}}

# Collaboration

## Open Other Content

**OPEN_CONTENT**

End the current content and open the newly specified .mdf.

{{< message >}}
OPEN_CONTENT|relative_mdf_path
{{< /message >}}

**FST_LOAD**

Discard the currently running FST and load and start the specified FST.

{{< message >}}
FST_LOAD|(.fst file path)
FST_LOAD|(.fst file path)|(initial state label)
{{< /message >}}

**SUBFST_START**, **SUBFST_START_IF**

Start a sub-FST process of an FST file.  Use **SUBFST_START_IF** when start only if the file exists.

- Will issue **SUBFST_EVENT_START** on successful start.
- Will issue **SUBFST_EVENT_STOP** on termination.

{{<message>}}
SUBFST_START|(alias)|(.fst file path)
SUBFST_START_IF|(alias)|(.fst file path)
SUBFST_EVENT_START|(alias)
SUBFST_EVENT_STOP|(alias)
{{</message>}}

**SUBFST_STOP**

Force terminate the specified sub-FST.

- Will issue **SUBFST_EVENT_STOP** on termination.

{{<message>}}
SUBFST_STOP|(alias)
SUBFST_EVENT_STOP|(alias)
{{</message>}}

## Forced Home Setting

**HOME_SET**

Set the current content to home.

{{< message >}}
HOME_SET
{{< /message >}}

**HOME_CLEAR**

Clear the home setting.

{{< message >}}
HOME_CLEAR
{{< /message >}}

## App Integration

**EXECUTE**

Executes the specified file (Windows only)

{{< message >}}
EXECUTE|(file name)
{{< /message >}}

**KEY_POST**

Sends a key event to the specified application (Windows only)

{{< message >}}
KEY_POST|(window class name)|(key name)|(ON or OFF for shift-key)|(ON or OFF for ctrl-key)|(On or OFF for alt-key)
{{< /message >}}

## File Download

**NETWORK_GET**

Downloads a file. Upon completion, it triggers **NETWORK_EVENT_GET**.

{{< message >}}
NETWORK_GET|(net alias)|(URI)|(save file name)
NETWORK_EVENT_GET|(net alias)
{{< /message >}}

# User Interface

## Button Display

**BUTTON_ADD**

Adds a button to the screen. After the display is complete, it issues **BUTTON_EVENT_ADD**.

- Argument 1: Alias name (new)
- Argument 2: Display scale
- Argument 3: Display position x,y. Positive values are from the left (bottom), negative values are from the right (top)
- Argument 4: Image file
- Argument 5: Action ("play", "open", "message", "keyvalueset"...)
- Argument 6: Processing after pressing (ON=hide display, OFF=keep display)

{{< message >}}
BUTTON_ADD|alias|scale|x,y|image path|action|(ON or OFF for autoclose)
BUTTON_EVENT_ADD|alias
{{< /message >}}

**BUTTON_DELETE**

Deletes a button. After deletion is complete, it issues **BUTTON_EVENT_DELETE**.

{{< message >}}
BUTTON_DELETE|alias
BUTTON_EVENT_DELETE|alias
{{< /message >}}

**BUTTON_EVENT_EXEC**

Issued when a button is clicked (tapped).

{{< message >}}
BUTTON_EVENT_EXEC|alias
{{< /message >}}

## Menu Addition

**MENU|ADD**

Adds a new page to the menu. Up to 20 pages can be added including the default. After addition is complete, it issues **MENU_EVENT|ADD**.

{{< message >}}
MENU|ADD|(alias)
MENU|ADD|(alias)|backgroundImagePath
MENU_EVENT|ADD|(alias)
{{< /message >}}

**MENU|SETITEM**

Registers an item at a specified location on a specified page of the menu. `id` is the item number starting from 0. Up to 30 items can be registered per page. After registration is complete, it issues **MENU_EVENT|SETITEM**.

{{< message >}}
MENU|SETITEM|(alias)|(id)|(label)|(type)|(arg1)|(arg2)|...
MENU_EVENT|SETITEM|(alias)|(id)
{{< /message >}}

**MENU|DELETEITEM**

Deletes the item content at a specified location on a specified page of the menu. After deletion is complete, it issues **MENU_EVENT|DELETEITEM**.

{{< message >}}
MENU|DELETEITEM|(alias)|(id)
MENU_EVENT|DELETEITEM|(alias)|(id)
{{< /message >}}

**MENU|DELETE**

Deletes an entire specified page of the menu. After deletion is complete, it issues **MENU_EVENT|DELETE**.

{{< message >}}
MENU|DELETE|(alias)
MENU_EVENT|DELETE|(alias)
{{< /message >}}