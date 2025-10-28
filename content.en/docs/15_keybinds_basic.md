---
title: Controls
slug: keybind-basic
---
# Controls

MMDAgent-EX supports basic operations with keyboard and mouse. Try features such as log display, camera movement, and fullscreen.

## Basic controls

|Function|Key|Description|
|:--|:--|:--|
|**Exit application** |`ESC`|Close the window and exit the application|
|**Reload** |`Shift+r` |Restart content|
|**Fullscreen** | `f` |Toggle fullscreen (press again to return)|
|**Status display** | `s` | Toggle the [Status display](../screen/) at the top-left|
|**Simple log**| `d` | Toggle the [Simple log](../log/#3d-scene-output)|
|**Detailed log**| `Shift+f` |Toggle the [Detailed log](../log/#on-screen-detailed-output)|
|**Log terminal**| `Shift+d` | Show log terminal (Windows only)|
|**Log scroll**|`PageUP`, `PageDown` |Scroll the log display|

## Camera controls

`Arrow keys` change the camera direction; hold `Shift` to move.

Press `+` to zoom in and `-` to zoom out.

The mouse is locked by default -- press `c` to unlock. Drag near the window center to rotate, double-tap then drag to pan, and use a two-finger pinch to zoom. Press `c` again to re-lock.

After changing camera settings, press `Shift + c` to reset to the default used before movement started.

Note: Cannot be changed while a camera motion is running.

## Menu

Press `/` or the tab bar `menu` to open the menu.

Flip pages with the left/right keys or a horizontal flick. If there are many items, scroll with a vertical flick.

Select items with the up/down keys and press Enter, or tap to select.

## History

Press `Shift + h` or the tab bar `history` to open the recent playback history.

Select an item to play that content.

## External app integration

Press `e` to open the currently running interaction script file in a text editor.

Press `Shift + e` to open the content's folder in Explorer.

Note: Windows only.

## Drag & Drop

You can play model files (.pmd) and motion files (.vmd) by dragging and dropping them onto the window.

Note: This feature works on Windows only.


|File|Where|Modifier keys|Result|Notes|
|:--|:--|:--|:--|:--|
|.pmd|On a model|-|Replace the existing model with the specified file||
|.pmd|Anywhere|Ctrl|Load as a new model||
|.vmd|On a model|-|Play motion|Loop playback ("base", FULL, LOOP)|
|.vmd|Anywhere|Ctrl|Play on all models|Apply the above to all models|
|.vmd|On a model|Shift|Add motion|Overlay the motion and play once (PART, ONCE)|
|.vmd|Anywhere|Ctrl+Shift|Add and play on all models|Apply the above to all models|
|image file|Anywhere|-|Replace background image|png, jpg, bmp, tga|
|image file|Anywhere|Ctrl|Replace floor image|png, jpg, bmp, tga|
|.xpmd|Anywhere|-|Replace the stage||