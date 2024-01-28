

---
title: Displaying Images and Text
slug: image-and-text
---
{{< hint info >}}
The functionalities of **TEXTAREA_ADD**, and **TEXTAREA_SET** are provided by the Plugin_TextArea. Make sure this plugin is enabled when you use it.
{{< /hint >}}

# Displaying Images and Text

By using text and images alongside audio, you can create complex and effective interactions. MMDAgent-EX offers multiple ways to display text and images on the screen, which can be combined with dialogue scripts to create multimodal dialogues.

- Displaying sentences or images within a scene
- Displaying subtitles on the screen
- Presenting user with choices through prompt presentation
- Letting user read README files through text file browsing

Below, we introduce how to use each of these features.

## Displaying Images and Text in 3D Space (TEXTAREA)

You can display arbitrary text or images in a 3D space. The procedure is divided into the following two steps:

1. Define the area where it should be displayed (the display area) (**TEXTAREA_ADD**)
2. Specify what to display (**TEXTAREA_SET**)

### Display Area Definition

The display area is defined using the **TEXTAREA_ADD** message. The display area is a "board" in the scene space, and you specify properties such as its width, height, position, color, and text.

- First argument: Alias name (new)
- Second argument: Width and height
- Third argument: Text size, margin, line spacing. Each is based on 1.0.
- Fourth argument: Background color r,g,b,a; a = 0 means no background
- Fifth argument: Text color r,g,b,a
- Sixth argument: Center coordinate position

{{<message>}}
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z
{{</message>}}

When displaying text, if you set `width` or `height` to undefined (0), there will be no constraints in that direction, and the size of the board will stretch or shrink automatically to fit the text to be specified later. If you specify a number other than 0, that direction will be fixed to the specified value, and if the text overflows, it will automatically reduce to fit within the defined dimension.

For images, if you set either `width` or `height` to undefined (0), the undefined dimension will be adjusted automatically to match the aspect ratio of the image. Please specify a size for either `width` or `height`.

While this is the default usage, you can also specify the rotation of the board, model mount, bone mount, etc. For more details, please visit the [message list](http://localhost:1313/ja/docs/messages/#%e3%83%86%e3%82%ad%e3%82%b9%e3%83%88%e7%94%bb%e5%83%8f%e3%82%ab%e3%83%a1%e3%83%a9%e6%98%a0%e5%83%8f%e3%82%92%e8%a1%a8%e7%a4%ba) page.

The **TEXTAREA_EVENT_ADD** is issued when the addition is completed.

{{<message>}}
TEXTAREA_EVENT_ADD|alias
{{</message>}}

### Specifying Display Content

You can display a string or an image in the display area using the **TEXTAREA_SET** command. If there is already something displayed in the area, it will be replaced with the new specified item.

**To display a string**, specify the string. The string can include spaces if it is enclosed in "", and you can create a new line with "\n".

{{<message>}}
TEXTAREA_SET|(textarea alias)|"You can specify a sentence like this.\nHello"
{{</message>}}

**To display an image**, specify the path to the image file. You can use png, jpg formats. Animated pngs can also be used.

{{<message>}}
TEXTAREA_SET|(textarea alias)|somewhere/image.png
{{</message>}}

{{<hint ms>}}
By specifying __camera0 instead of a text or image path, you can open a webcam and display its video in the designated display area in real-time.

{{<message>}}
TEXTAREA_SET|(textarea alias)|__camera0
{{</message>}}

![textarea with camera](/images/textarea_camera.png)

`0` の部分数字はカメラ番号（0=デフォルト）で、`__camera1`, `__camera2` のようにすることで複数のWebカメラがあるときにカメラを個別に指定できます。

The number in the part is the camera index (0=default).  By specifying `__camera1` ,`__camera2`, etc., you can specify which camera to open.

Note: When using a high-resolution webcam, it may take tens of seconds or more to start, due to OpenCV's specifications. In such cases, you can bipass some initialization step and may be able to make the start up delay much smaller by setting the environment variable `OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS` to `0`.

{{</hint>}}

When the specified display starts, the **TEXTAREA_EVENT_SET** is issued.

{{<message>}}
TEXTAREA_EVENT_SET|alias
{{</message>}}

### Deleting Display Area

The area is deleted and the display is cleared with **TEXTAREA_DELETE**. Upon completion of deletion, **TEXTAREA_EVENT_DELETE** is issued.

{{<message>}}
TEXTAREA_DELETE|(textarea alias)
TEXTAREA_EVENT_DELETE|alias
{{</message>}}

## Displaying Text Captions

As shown in the image below, text can be displayed as captions. The differences from the above TextArea:

- Displayed on-screen, not in 3D space (displayed at a fixed position regardless of viewpoint)
- Automatically disappears after a specified time
- Able to specify any font (ttf)
- Up to two kinds of text outlines can be specified
- Supports .lrc file (v1.0.2)

![caption](/images/caption.png)

To use it, first define the style of the caption (**CAPTION_SETSTYLE**), then display the text referencing that style (**CAPTION_START**).

### Defining Caption Style

The style is defined with **CAPTION_SETSTYLE**.

- Argument 1: Alias name of the style (new)
- Argument 2: Font file path. Use system font with "default".
- Argument 3: Text color r,g,b,a
- Argument 4: Color and size of the first outline r,g,b,a,thickness. If no outline is needed, set a or thickness to 0.
- Argument 5: Color and size of the second outline. The specification is the same as above.
- Argument 6: Frame background color r,g,b,a. If not needed, set a to 0.

{{<message>}}
CAPTION_SETSTYLE|style_alias|fontpath|r,g,b,a|edge1|edge2|basecolor
{{</message>}}

After the definition is completed, a **CAPTION_EVENT_SETSTYLE** message is issued.

{{<message>}}
CAPTION_EVENT_SETSTYLE|style_alias
{{</message>}}

### Starting Caption Display

Start a new caption display with **CAPTION_START**.

- Argument 1: Alias name (new)
- Argument 2: Alias name of the predefined style to use
- Argument 3: Text of the display content, or .lrc file name. On text, if it contains spaces, enclose it in "". You can also use "\n" for line breaks.
- Argument 4: Text size
- Argument 5: Specify the left-right position of the display with one of the strings CENTER, LEFT, RIGHT
- Argument 6: The up-down position of the display. A relative value with the bottom of the screen being 0.0 and the top being 1.0
- Argument 7: Display duration in number of frames (30=1 second)

If a text display with the specified alias name already exists, that display is erased and overwritten with the new specification.

{{<message>}}
CAPTION_START|alias|style_alias|text|size|align|height|duration
{{</message>}}

Usage example:

{{<fst>}}

# Test display the caption with the "1" key

# Use the font file rounded-mplus-1c-heavy.ttf.

# Text color: Orange

# Edge 1: White, thickness 4

# Edge 2: Semi-transparent Black, Thickness 6

# Frame Background: No Drawing
10 10:
    KEY|1 CAPTION_SETSTYLE|terop|rounded-mplus-1c-heavy.ttf|1,0.5,0,1|1,1,1,1,4|0,0,0,0.6,6|0,0,0,0
    CAPTION_EVENT_SETSTYLE|terop CAPTION_START|test|terop|Test|3.0|CENTER|0.5|300
{{</fst>}}

When the display starts, a **CAPTION_EVENT_START** message is output.

{{<message>}}
CAPTION_EVENT_START|alias
{{</message>}}

### Caption Display End

The text being displayed will disappear after a specified time, but you can also immediately remove it by issuing a **CAPTION_STOP** message.

{{<message>}}
CAPTION_STOP|alias
{{</message>}}

When the display ends, a **CAPTION_EVENT_STOP** message is output.

{{<message>}}
CAPTION_EVENT_STOP|alias
{{</message>}}