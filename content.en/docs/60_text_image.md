---
title: Displaying Images and Text
slug: image-and-text
---
{{< hint info >}}
**TEXTAREA_ADD**, **TEXTAREA_SET** functions are provided by the Plugin_TextArea. Make sure this plugin is enabled when using them.
{{< /hint >}}

# Displaying Images and Text

Using text and images together with audio allows you to create richer and more effective interactions. MMDAgent-EX provides multiple ways to display images and text on screen, and by combining these with dialogue scripts you can build multimodal interactions.

- Display text and images within a scene
- Show on-screen captions
- Present prompts with choices for the user to select
- Provide a text-file viewer to let the user read README files

Below are instructions for each feature.

## Displaying images and text in 3D space (TEXTAREA)

You can display arbitrary text or images in the 3D scene. The procedure is divided into two steps:

1. Define the display area (the area to show content) (**TEXTAREA_ADD**)
2. Specify the content to display (**TEXTAREA_SET**)

### Defining a display area

Use the **TEXTAREA_ADD** message to define a display area. The display area is a "panel" in scene space; you can set its width, height, position, color, font settings, and other properties.

- 1st arg: alias name (new)
- 2nd arg: width and height
- 3rd arg: font size, margin, line spacing. Each default is 1.0.
- 4th arg: background color r,g,b,a — a = 0 means no background
- 5th arg: text color r,g,b,a
- 6th arg: center coordinate position

{{<message>}}
TEXTAREA_ADD|(textarea alias)|(width,height)|(size,margin,exlinespace)|r,g,b,a|r,g,b,a|x,y,z
{{</message>}}

When displaying text, if you set either `width` or `height` to unspecified (0), that direction is unconstrained and the panel will automatically resize to fit the text specified later. If you set a non-zero value, that direction is fixed to the specified size; if the text would overflow, the font will automatically scale down to fit.

For images, if you set either `width` or `height` to unspecified (0), the unspecified dimension will be adjusted automatically to preserve the image aspect ratio. You must specify a non-zero value for either `width` or `height`.

The above is the basic usage, but you can also specify panel rotation, model mount, bone mount, and more. For details, see the [Message list](../messages/) page.

When the addition is complete, **TEXTAREA_EVENT_ADD** is dispatched.

{{<message>}}
TEXTAREA_EVENT_ADD|alias
{{</message>}}

### Specifying content to display

Use **TEXTAREA_SET** on a display area to show a string or an image. If the area already has content, it will be replaced by the newly specified content.

When displaying a string, specify the string. Wrap it in "" to include spaces; use "\n" for line breaks.

{{<message>}}
TEXTAREA_SET|(textarea alias)|"You can specify a sentence like this.\nHello"
{{</message>}}

When displaying an image, specify the image file path. Supported image formats are png and jpg. Animated PNG is also supported.

{{<message>}}
TEXTAREA_SET|(textarea alias)|somewhere/image.png
{{</message>}}

When the specified display starts, **TEXTAREA_EVENT_SET** is dispatched.

{{<message>}}
TEXTAREA_EVENT_SET|alias
{{</message>}}

### Deleting a display area

Use **TEXTAREA_DELETE** to remove an area and clear its display. When deletion is complete, **TEXTAREA_EVENT_DELETE** is dispatched.

{{<message>}}
TEXTAREA_DELETE|(textarea alias)
TEXTAREA_EVENT_DELETE|alias
{{</message>}}

## Text caption display

You can display text as captions on-screen as shown in the image below. Differences from the TextArea above:

- Shown on-screen (fixed position relative to the view, not in 3D space)
- Automatically disappears after a specified time
- You can specify a custom font (ttf)
- Up to two text outlines (edges) can be specified

Since v1.0.2, the following changes apply:

- Support for timeline display via .lrc files (v1.0.2)
- Default style `_default` (v1.0.2)
- Arguments from the 4th onward of **CAPTION_SETSTYLE** are now optional (v1.0.2)

![caption](/images/caption.png)

Start a caption by specifying text or an .lrc file with **CAPTION_START**. You can use the default style by specifying `_default` as the second argument, or define a custom style using **CAPTION_SETSTYLE** and then reference that style name in **CAPTION_START**.

### Defining caption styles

Define styles with **CAPTION_SETSTYLE**. If you do not define a style, `_default` will be used. The first three arguments (alias, font path, color) are required; arguments from the fourth onward are optional for more detailed style settings.

- 1st arg: style alias name (new)
- 2nd arg: font file path. Use "default" to use the system font.
- 3rd arg: text color r,g,b,a
- 4th arg: (optional) first outline color and thickness r,g,b,a,thickness. If no outline is needed, set a or thickness to 0.
- 5th arg: (optional) second outline color and thickness, same format as above.
- 6th arg: (optional) background box color r,g,b,a. Set a to 0 if not required.

{{<message>}}
CAPTION_SETSTYLE|style_alias|fontpath|r,g,b,a|edge1|edge2|basecolor
{{</message>}}

After defining a style, **CAPTION_EVENT_SETSTYLE** is dispatched.

{{<message>}}
CAPTION_EVENT_SETSTYLE|style_alias
{{</message>}}

### Starting caption display

Use **CAPTION_START** to begin displaying a caption. Specify either text directly or an lrc file.

- 1st arg: alias name (new)
- 2nd arg: alias of a defined style to use
- 3rd arg: text to display or an lrc file. Wrap text with "" if it contains spaces. Use "\n" for line breaks.
- 4th arg: font size
- 5th arg: horizontal alignment — specify one of CENTER, LEFT, RIGHT
- 6th arg: vertical position as a relative value where bottom = 0.0 and top = 1.0
- 7th arg: display duration in frames (30 = 1 second)

If a caption with the specified alias already exists, it will be removed and replaced by the new one.

{{<message>}}
CAPTION_START|alias|style_alias|text|size|align|height|duration
{{</message>}}

Example:

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

When a caption display starts, **CAPTION_EVENT_START** is dispatched.

{{<message>}}
CAPTION_EVENT_START|alias
{{</message>}}

### Stopping caption display

A caption will disappear after the specified duration, but you can also remove it immediately by sending **CAPTION_STOP**.

{{<message>}}
CAPTION_STOP|alias
{{</message>}}

When a caption stops, **CAPTION_EVENT_STOP** is dispatched.

{{<message>}}
CAPTION_EVENT_STOP|alias
{{</message>}}