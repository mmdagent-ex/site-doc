---
title: Key and Mouse Operation
slug: keybind-basic
---
# Key and Mouse Operations

MMDAgent-EX can be operated using keys and mouse. Try various actions such as displaying logs, changing the view, and full screen.

## Basic Operations

|Function|Key|Description|
|:--|:--|:--|
|**Exit App** |`ESC`|Close the window and exit the app|
|**Reload** |`Shift+r` |Restart the content|
|**Full Screen** | `f` |Toggle full screen|
|**Show/Hide Status Indicator** | `s` | Toggle the [Status Indicator](../screen/#1-status) at the top left of the screen|
|**View/Hide 3D Log**| `d` | Toggle the [log in 3D scene](../log/#render-in-3d-scene)|
|**View/Hide on-screen log**| `Shift+f` |Toggle the [on-screen log](../log/#show-on-screen)|
|**View Log Terminal**| `Shift+d` | Start log terminal (Windows)|
|**Scroll Log**|`PageUP`, `PageDown` |Scroll through the log|

## Camera

Use the `Arrow keys` to change the camera direction, and hold `Shift` for movement.

Use `+` key to zoom in and `-` key to zoom out.

Camera movement by mouse is disabled by default.  Press `c` key to start moving camera with mouse.  Rotate by dragging around the center of the window, move by sliding from a double tap, and zoom in and out with a two-finger pinch. Lock it again with the `c` key.

After changed camera, press `Shift + c` to reset camera to the its original position.

※ The changes above will be ignored while playing camera motion.

## Menu

Press `/` or the tab bar `menu` to bring up the menu.

Turn the pages with the left and right keys or left and right flicks. If there are many items, scroll with vertical flicks.

Select an item by using the up and down keys and pressing Enter, or by tapping.

## History

Press `Shift + h` or the tab bar's `history` to display the history of the most recently played content.

Selecting this will play the content.

## External App Collaboration

Press `e` to open the running dialogue script file in a text editor.

Press `Shift + e` to open the content's folder in the explorer.

※ These function works only on Windows.

## Drag & Drop

By dragging and dropping model files (.pmd) or motion files (.vmd) onto the window, you can play them.

※ This feature only works on Windows.


|What File | Where | While Pressing | Result | Note |
|:--|:--|:--|:--|:--|
|.pmd|On the model|-|Replace existing model with specified file||
|.pmd|Anywhere|Ctrl|Display a new model||
|.vmd|On the model|-|Play motion| Loop playback ("base", FULL, LOOP)|
|.vmd|Anywhere|Ctrl|Play on all models| Apply to all models as above|
|.vmd|On the model|Shift|Add motion|Play overlaid motions once (PART, ONCE)|
|.vmd|Anywhere|Ctrl+Shift|Add and play on all models| Apply to all models as above|
|Image file|Anywhere|-|Replace background image|png, jpg, bmp, tga|
|Image file|Anywhere|Ctrl|Replace floor image|png, jpg, bmp, tga|
|.xpmd|Anywhere|-|Replace stage||