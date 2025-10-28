---
title: Buttons
slug: buttons
---
# Buttons

You can define buttons for each piece of content. When the content is played, the buttons appear on the screen after a long tap or by pressing the `q` key. You can assign various content-dependent actions to them.

## How to define a button

Place a button definition file in the top folder of the content package. The first file must be named `BUTTON0.txt`; additional buttons use `BUTTON1.txt`, etc. You can define up to 10 buttons, up to `BUTTON9.txt`.

```text
BUTTON0.txt
BUTTON1.txt
...
BUTTON9.txt
```

You can also define "sub-buttons" by adding files like `BUTTON0-0.txt`, `BUTTON0-1.txt` and so on. Sub-buttons are not shown by default; they appear when their parent button (e.g. `BUTTON0.txt`) is pressed.

```text
BUTTON0.txt
BUTTON0-0.txt
BUTTON0-1.txt
BUTTON0-2.txt
BUTTON1.txt
BUTTON1-1.txt
...
```

## Button definition file

Below is a simple example of a button definition file. A line that starts with "`#`" is a comment.

```text
#### BUTTON0.txt

image=btn_rocket.png
x=0.2
y=-1.0
scale=1.0
label=Testing
labelX=0.0
labelY=0.0
labelScale=1.0
labelColor=#FF0000
from=left
exec=open,http://www.google.com/
#exec=play,mmdagent://somewhere/some/dir
#exec=message,MODEL_DELETE|mei
#exec=setkeyvalue,__BUTTON1=true
```

### Button image

Image file to be displayed as the button. A transparent PNG is recommended.

```text
image=imgfile.png
```

### Button position

Center coordinates of the button.

```text
x=1.0
y=-1.0
```

- Positive values measure distance from the left and bottom edges of the screen
- Negative values measure distance from the right and top edges of the screen

### Button scale

Scale factor of the image.

```text
scale=2.0
```

### Button text

A text label can be overlaid on the button image. Fixed text can be specified with `label`.

```text
label=some string
```

When specifying a KeyValue name by prefixing it with "`@`", the corresponding value will be displayed dynamically.

```text
label=@KeyName
```

### Button text adjustment

The scale and position of the text label can be adjusted with `labelX`, `labelY` and `labelScale`. The origin of the text is the left-middle edge of the button.

```text
# move text label to upper-right of original and magnify by 1.5
labelX=1.0
labelY=0.5
labelScale=1.5
```

Text color can be specified with `labelColor`. Color should be like `#RRGGBB` or `#RRGGBBAA`. Default is `#FFFFFFFF`.

```text
labelColor=#FF0000
```

### Button animation direction

Specify from which edge of the screen the button appears. Valid values are `left`, `right`, `top`, `bottom` and `parent`. `parent` means that the button will appear from the parent button's position and is valid only for sub-buttons. Default value is `left`.

```text
from=left
```

### Button actions

An action for a button is defined using the `exec` option. Several action types are supported.

#### 1. Open URL on external browser

To open a web page, specify action as `open` and the target URL.

```text
exec=open,http://www.google.com/
```

#### 2. Play contents

To start playing content, specify `play` and the target. The target can be a URL (web content) or a file path to a .mdf file (local content).

```text
# web contents
exec=play,http://www.google.com/
# local contents
exec=play,xxx/yyy/foo.mdf
```

#### 3. Issue message

Specify `message` and a message string in `exec` to issue the message when the button is pressed.

```text
exec=message,MODEL_DELETE|model
```

#### 4. Set KeyValue

You can also configure a button to set a KeyValue. Use `setkeyvalue` followed by the key-name pair to set on tap.

```text
exec=setkeyvalue,KeyName=Value
```

### Change button appearance by KeyValue

A button's appearance and actions can be changed at run time. You can specify a key-value pair as a trigger condition, and properties to be changed when the condition is met. Below is an example.

```text
#### BUTTON0.txt with variants

## normal button definition
image=...
label=...
exec=...

## variant 1
# condition (required)
1-ifKeyName=KeyName
1-ifKeyValue=Value
# image should be always specified at a variant
1-image=...
# others are optional
1-exec=...
1-scale=...
1-x=...
1-y=...
1-from=...
1-label=...
1-labelX=...
1-labelY=...
1-labelScale=...
1-labelColor=...

## variant 2
2-ifKeyName=KeyName
2-ifKeyValue=AnotherValue
2-image=...
```

The prefix "`1-`" can be replaced with "`2-`", "`3-`" and so on to define multiple conditioned variants. Up to 9 variants are supported. When a condition matches, the properties with the same prefix are applied; properties not defined with the prefix are left unchanged.