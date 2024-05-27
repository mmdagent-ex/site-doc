

---
title: Background, Floor, and Frame
slug: scene
---

# Background, Floor, and Frame

While the main focus in voice interactions is obviously the CG character itself, we cannot afford to neglect ancillary information such as the background and frame displayed on the screen. Just as people's impressions can change based on the clothes they wear, what is displayed in the background and around the character can influence the overall impression.

In this section, we will discuss the scene settings in MMDAgent-EX that are related to things other than the CG character.

- Color of space
- Background and floor images
- 3D stage
- Screen frame

{{< details "Drag & Drop" close >}}
**Windows only**: You can also change the image by dragging and dropping an image file from the explorer into the background area.

- Background: Drop the image
- Floor: Drop the image while pressing `CTRL`
{{< /details >}}

## Color of Space

You can specify the default color of the space (i.e., the color of empty space) in the .mdf file using `campus_color`. `r,g,b` specifies the intensity of R, G, B from 0.0 to 1.0. The default is dark blue (`0,0,0.2`).

{{<mdf>}}
campus_color=r,g,b
{{</mdf>}}

## Background and Floor

You can set and change the images for the floor and background by issuing a **STAGE** message. Specify two images in the order of "floor image, background image". You can use .png, .jpg files.

{{<message>}}
STAGE|(floor image file),(back image file)
{{</message>}}

The floor and background are displayed as boards in the scene. You can change the size of these boards in the .mdf file as follows:

{{<mdf>}}
stage_size=x,y,z
{{</mdf>}}

`x,y,z` specify the length of each part. Note that `x` is half the width.

![stage image](/images/stage.png)

## Stage Model

You can specify a 3D model for the stage to represent the entire scene with a 3D model. Only .pmd format (including those transformed from .pmx format) can be used. You specify the model file with a **STAGE** message.

{{<message>}}
<eps> STAGE|stage/tatami_room/tatami_room.pmd
{{</message>}}

※ When using a stage model, the floor and background are not drawn.

The following is an example of specifying the samples in the `stage` folder under Example with **STAGE**.

![stage example](/images/stage_example.png)

## Screen Frame

You can paste any PNG image over the entire front of the screen with the **WINDOWFRAME** message. It supports transparent PNGs, so you can use a transparent image to create a frame-like effect on the screen. Here are some examples of how to use it.

![window frame example 1](/images/windowframe_example.png)

![window frame example 2](/images/windowframe_example2.png)

When you issue **WINDOWFRAME|other_image.png** while another frame is displaying, it will be swapped to the new one.  You can totally delete the frame by issuing **WINDOWFRAME|NONE"

You can further handle multiple frames by using **WINDOWFRAME_ADD** and **WINDOWFRAME_DELETE**.  Issuing **WINDOWFRAME_ADD|name|foobar.png** will add a new frame to the screen.  You should specify a unique name to use multiple frames.  If you specify a **name** that exists, the image formally specified by the **name** will be swapped to the new one.

{{<message>}}
<eps> WINDOWFRAME_ADD|frame1|images/frame_trad.png
{{</message>}}

You can delete each frame by issuing **WINDOWFRAME_DELETE|name**.  When issued, frame of the specified name will be deleted.

{{<message>}}
<eps> WINDOWFRAME_DELETE|frame1
{{</message>}}

Also you can delete all the frames at once by issuing **WINDOWFRAME_DELETEALL**.

{{<message>}}
<eps> WINDOWFRAME_DELETEALL
{{</message>}}
