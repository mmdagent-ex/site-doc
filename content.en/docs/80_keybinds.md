

---
title: Key and Mouse Operations
slug: keybinding
---

# Key and Mouse Operations

A list of all operations.

## General

||Mouse|Key|
|:--|:--|:--|
|**Exit App** | - |`ESC`|
|**Switch Fullscreen** | - | `F`
|**Switch VSync** | - | `Shift+V` |
|**Reload** | - |`Shift+R` |
|Screenshot *1  | - | `Shift+G` |
|Force Update *2 |-  | `!` |

*1 Saves the screen under `MMDAgent-Content` on the desktop as `snapshot.png`

*2 Only valid when auto-update is set up

## Bookmark・History・File

|Function|Mouse|Key|
|:--|:--|:--|
|**Open Bookmark** |Bookmark icon||
|**Open History** |History icon|`Shift+H`|
|Open current .fst in editor *1  | - | `E`|
|Open current content folder in Explorer *1 | - | `Shift+E` |
|Built-in File Browser|-|`Shift+O`|

*1 Windows only

## Menu and Button

|Function|Mouse|Key|
|:--|:--|:--|
|**Show/Hide Menu** |Menu icon| `/` |
|Flip through Menu|Flick|Left/Right keys|
|Cursor movement|-|Up/Down keys|
|Select item|Click| `Enter` |
|Item options | Long press on item|`Shift+Enter` |
|Hide/Show button|Long press on screen | `Q` |

## Viewpoint (Camera) Change

By default, viewpoint change is locked and does not work. You can change it by unlocking it with the `C` key. Lock it again with the `C` key.

To return to the initial viewpoint state after operation, use the `Shift+C` key.

|Function|Mouse|Key|
|:--|:--|:--|
|**Unlock / Re-lock** |-|`C`
|**Camera Reset** |ー|`Shift+C`
|**Rotation**|Drag or Slide|Arrow keys |
|**Pan**|Shift+Drag or Slide from Double Tap | `Shift`+Arrow keys|
|**Zoom**|Ctrl+Wheel or Pinch with Two Fingers|`+`, `-` |

## Display Switch

|Function|Mouse|Key|
|:--|:--|:--|
|**Switch Operation Status Display ON/OFF** | - | `S` |
|Switch Shadow Display ON/OFF   | - |`Shift+S`|
|Switch Physics OFF/ON | - | `P` |
|Eye follows mouse pointer *1 | - | `L`|
|(debug) Show bones| - | `B` |
|(debug) Show physical rigid body | - | `Shift+W`|
|(debug) Show wireframe | - | `W` |
|Thicken toon edge | - |`K` |
|Thin toon edge | - |`Shift+K` |
|Transparent window ON/OFF *2| - | `T` |

*1 requires Plugin_LookAt

*2 Windows only, requires parameter settings in .mdf

*1 Effective when Plugin_LookAt is enabled

## CG Effects

|Function|Mouse|Key|
|:--|:--|:--|
|Toggle shadow display method (Projection/Shadow map)| - |`X`|
|Change light source position|Ctrl+Shift+Drag | - |
|AutoLuminous: OFF→Weak→Strong→OFF | - |`Shift+L` |
|Diffusion Effect intensity: OFF→Weak→Strong→OFF | - | `O` |
|Diffusion Effect spread: OFF→Weak→Strong→OFF | - | `I` |
|Double shadow effect ON/OFF | - | `Shift+J` |

## Log Display

|Function|Gesture|Mouse|Key|
|:--|:--|:--|:--|
|**Simplified log display ON/OFF**| - | - | `D` |
|**Detailed log display ON/OFF**| - | - | `Shift+F` |
|Display log in console window *1| - | - | `Shift+D` |
|Scroll log| - | - | `PageUP`, `PageDown` |
|Search keywords in log| - | - | `?` + Enter text, `Del` to finish |

*1 Windows only

## Scene Management

|Function|Mouse|Key|
|:--|:--|:--|
|Move model on XZ plane |Drag model with Ctrl | - |
|Move model on XY plane |Drag model with Ctrl+Shift | - |
|Delete model | Double click model and hit `Del` | -|
|Reset rigid body position | - |`Shift+P` |
|Fast forward/rewind scene| - | `Ctrl+leftright`|
|Pause/unpause scene | - | `H` |

## File Drag & Drop

Windows only

|What file to | Where to | While pressing key | What happens | Note |
|:--|:--|:--|:--|:--|
|.pmd|On model|-|Replace existing model with specified file||
|.pmd|Anywhere|Ctrl|Display new model||
|.vmd|On model|-|Play motion| Loop play ("base", FULL, LOOP)|
|.vmd|Anywhere|Ctrl|Play on all models| Apply to all models
|.vmd|On model|Shift|Add motion|Overlap motions and play once (PART, ONCE)
|.vmd|Anywhere|Ctrl+Shift|Add and play on all models|Apply to all models|
|image file|Anywhere|-|Replace background image|png, jpg, bmp, tga|
|image file|Anywhere|Ctrl|Replace floor image|png, jpg, bmp, tga|
|.xpmd|Anywhere|-|Replace stage||

## Voice Recognition (Plugin_Julius)

Only when Plugin_Julius is enabled

|Function|Mouse|Key|
|:--|:--|:--|
|Toggle voice input volume display ON/OFF|- |`a` |
|Change voice detection sensitivity | - | `<`, `>`|