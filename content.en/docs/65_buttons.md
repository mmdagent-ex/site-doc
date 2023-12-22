

---
title: Buttons
slug: buttons
---

# Buttons

You can define buttons for each piece of content. When the content is being viewed, these buttons will appear on the screen either by long pressing or pressing the `q` key. You can assign various actions to these buttons that are specific to the content.

## How to define a button

To define a button, place a button definition file in the top folder of the content package. The name of the file should be `BUTTON0.txt`, and additional buttons can be defined as `BUTTON1.txt`, and so forth. You can define up to 10 buttons, from `BUTTON0.txt` to `BUTTON9.txt`.

```text
BUTTON0.txt
BUTTON1.txt
...
BUTTON9.txt
```

Moreover, you can define "sub-buttons" by creating button definition files named `BUTTON0-0.txt`, `BUTTON0-1.txt`, and so on. By default, these sub-buttons will not appear on the screen, but they will show up when their parent button (such as `BUTTON0.txt`) is pressed.

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

Here is a simple example of a button definition file. Lines that start with "`#`" are comments.

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

The image file that will be displayed as the button. It is recommended to use a transparent PNG.

```text
image=imgfile.png
```

### Button position

This is the center coordinate of the button.

```text
x=1.0
y=-1.0
```

- A positive value represents a distance from the left and bottom edges of the screen.
- A negative value represents a distance from the right and top edges of the screen.

### Button scale

This is the scale factor of the image.

```text
scale=2.0
```

### Button text

You can display a text label on top of the button image. The fixed text can be specified by `label`.

```text
label=some string
```

If you specify a key name of KeyValue preceded by "`@`", the value of the key will be displayed as dynamic text.

```text
label=@KeyName
```

### Button text adjustment

You can adjust the scale and position of the text label with `labelX`, `labelY`, and `labelScale`. The origin of the text is the left-middle edge of the button.

```text
# move text label to upper-right of original and magnify by 1.5
labelX=1.0
labelY=0.5
labelScale=1.5
```

The text color can be specified with `labelColor`. The color should be in the format `#RRGGBB` or `#RRGGBBAA`. The default is `#FFFFFFFF`.

```text
labelColor=#FF0000
```

### Button animation direction

You can specify from which edge of the screen the button will appear. Valid values are `left`, `right`, `top`, `bottom`, and `parent`. `Parent` indicates that the button will appear from the same location as the parent button and is only valid for sub-buttons. The default value is `left`.

```text
from=left
```

### Button actions

You can assign an action to a button with the `exec` option. There are several types of actions available.

#### 1. Open URL in external browser

To open a webpage, specify the action as `open` and provide the target URL.

```text
exec=open,http://www.google.com/
```

#### 2. Play content

To start playing content, specify `play` and the target content. The target content can be a URL (web content) or the file path of the .mdf file (local content).

```text
# web contents
exec=play,http://www.google.com/
# local contents
exec=play,xxx/yyy/foo.mdf
```

#### 3. Send message

By specifying `message` and the message string in `exec`, a message will be sent when the button is pressed.

```text
exec=message,MODEL_DELETE|model
```

#### 4. Set KeyValue

You also have the option to define a button to set a KeyValue. By using `setkeyvalue` along with the key-name pair, the value will be set upon tapping.

```text
exec=setkeyvalue,KeyName=Value
```

### Modify button appearance using KeyValue

The look and behavior of a button can be adjusted on the fly. You can establish a key-value pair as a trigger condition, and the properties to be altered when the key-value condition is met. The example below illustrates this.

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
# image should always be specified in a variant
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

The prefix "`1-`" can be replaced with "`2-`", "`3-`" and so on to define multiple conditional buttons. A maximum of 9 variants can be defined. When the condition is satisfied, the properties defined with the same prefix will be applied. Properties not defined with the prefix will remain unchanged.