---
title: Key and Mouse Controls
slug: keybinding
---
# Key and Mouse Controls

A complete list of all controls.

## General

| |Mouse|Key|
|:--|:--|:--|
|**Quit app** | - |`ESC`|
|**Toggle fullscreen** | - | `F`|
|**Toggle VSync** | - | `Shift+V` |
|**Reload** | - |`Shift+R` |
|Screenshot *1  | - | `Shift+G` |
|Force refresh *2 |-  | `!` |

*1 Saves the screen to Desktop under `MMDAgent-Content` as `snapshot.png`.

*2 Only effective if auto-update is set up.

## Bookmarks, History & Files

|Function|Mouse|Key|
|:--|:--|:--|
|**Open bookmark** |bookmark icon||
|**Open history** |history icon|`Shift+H`|
|Open current .fst in editor *1  | - | `E`|
|Open current content folder in Explorer *1 | - | `Shift+E` |
|Built-in file browser|-|`Shift+O`|

*1 Windows only

## Menus and Buttons

|Function|Mouse|Key|
|:--|:--|:--|
|**Show/hide menu** |menu icon| `/` |
|Turn menu page|flick|Left / Right|
|Move cursor|-|Up / Down|
|Select item|click| `Enter` |
|Item options | long-press item|`Shift+Enter` |
|Hide/show buttons|long-press the screen | `Q` |

## View (Camera) Controls

By default view changes are locked. Press `C` to unlock and enable view changes. Press `C` again to re-lock.

To return to the initial view state after changing, press `Shift+C`.

|Function|Mouse|Key|
|:--|:--|:--|
|**Unlock / Re-lock** |-|`C`|
|**Reset camera** | - |`Shift+C`|
|**Rotate**|drag or slide|Arrow keys|
|**Pan**|Shift+drag or slide after double-tap | `Shift` + Arrow keys|
|**Zoom**|Ctrl+wheel or two-finger pinch|`+`, `-` |

## Display Toggles

|Function|Mouse|Key|
|:--|:--|:--|
|**Toggle motion state display** | - | `S` |
|Toggle shadow display   | - |`Shift+S`|
|Toggle physics simulation | - | `P` |
|Make gaze follow mouse pointer *1 | - | `L`|
|(debug) Show bones| - | `B` |
|(debug) Show physics rigid bodies | - | `Shift+W`|
|(debug) Show wireframe | - | `W` |
|Thicken toon edges | - |`K` |
|Thin toon edges | - |`Shift+K` |
|Toggle screen transparency *2| - | `T` |

*1 When Plugin_LookAt is enabled

*2 Windows only; requires setting in .mdf

## CG Effects

|Function|Mouse|Key|
|:--|:--|:--|
|Toggle shadow rendering mode (Projected / Shadow Map)| - |`X`|
|Change light position|Ctrl+Shift+drag | - |
|AutoLuminous: OFF→Low→High→OFF | - |`Shift+L` |
|Diffusion effect intensity: OFF→Low→High→OFF | - | `O` |
|Diffusion effect spread: OFF→Low→High→OFF | - | `I` |
|Toggle double-shadow effect | - | `Shift+J` |

## Log Display

|Function|Gesture|Mouse|Key|
|:--|:--|:--|:--|
|**Toggle simple log display**| - | - | `D` |
|**Toggle detailed log display**| - | - | `Shift+F` |
|Show logs in console window *1| - | - | `Shift+D` |
|Scroll logs| - | - | `PageUp`, `PageDown` |
|Search logs by keyword| - | - | `?` + type text, finish with `Del` |

*1 Windows only

## Scene Operations

|Function|Mouse|Key|
|:--|:--|:--|
|Move model on XZ plane |Ctrl+drag model | - |
|Move model on XY plane |Ctrl+Shift+drag model | - |
|Delete model | double-click the model and press `Del` | -|
|Reset rigid body positions | - |`Shift+P` |
|Fast-forward / rewind scene| - | `Ctrl` + Left/Right|
|Pause / unpause scene | - | `H` |

## File Drag & Drop

Windows only

|What file|Where|With key held|Result|Notes|
|:--|:--|:--|:--|:--|
|.pmd|on a model|-|Replace the existing model with the specified file||
|.pmd|anywhere|Ctrl|Add the model to the scene||
|.vmd|on a model|-|Play motion|Loop playback ("base", FULL, LOOP)|
|.vmd|anywhere|Ctrl|Play on all models|Applies the above to all models|
|.vmd|on a model|Shift|Add motion|Stack motion and play once (PART, ONCE)|
|.vmd|anywhere|Ctrl+Shift|Add and play on all models|Applies to all models|
|image file|anywhere|-|Replace background image|png, jpg, bmp, tga|
|image file|anywhere|Ctrl|Replace floor image|png, jpg, bmp, tga|
|.xpmd|anywhere|-|Replace stage||

## Speech Recognition (Plugin_Julius)

Only when Plugin_Julius is enabled

|Function|Mouse|Key|
|:--|:--|:--|
|Toggle voice input volume display|- |`a` |
|Adjust voice detection sensitivity | - | `<`, `>`|