---
title: Changes from the Original MMDAgent
slug: changes-since-original-mmdagent
---
# Changes from the Original MMDAgent

This article summarizes the main changes from [MMDAgent](https://www.mmdagent.jp/) to MMDAgent-EX.

### Screen and Display

- Added menu
- Added [tab bar](../screen) at the bottom
- [Message errors shown sticky on screen for noticability](../screen)

### Added functions

- [Detailed log on screen](../log/) (`Shift+f`)
- Show History (`Shift+H`)
- Open FST in editor (`E`: for windows only)
- Open folder (`Shift+E`: for windows only)
- Save screenshot (`Shift+G`)
- Disabled viewpoint change by mouse by default: `c` key to toggle
- Revert camera (`Shift+C`)

### Post effeects

- AutoLuminous (`Shift+L`)
- Soft diffusion effect (`O` key and `I` key, for Windows only)
- Doppel shadow effect (`Shift+J`)

### 3D model

- [Now supports PMX model, with improved compatibility](../pmx/)
- [Enhanced motion blending function](../motion-layer/)
- Now supports animated PNG format for all textures and images

### FST extension

[Extended FST format](../fst-format/), old version still works.

- Block definition
- Regular expression
- Local variable initialization
- Global variables (KeyValue) are now accessible in FST 
- Now can refer to environmental variables
- VS Code Extension to write FST file

### Speech recognition

- Updated engine and models to their latest versions, now DNN based
- Added English ASR / TTS example modules

### Multimodal

- [Added several ways to show image and text in the scene](../image-and-text/)

### Enhancements for development

- [Added "Plugin_AnyScript" to incorporate any program easily](../submodule/)
- [Added way to playing audio files or stream from other program](../remote-speech/)
- [Enhanced socket connection](../remote-control/)
  - [WebSocket support](../remote-websocket/)
- [Morph-level outer control](../motion-bind/)

### Extensions on mdf and messages

Many configurations in .mdf and messages are newly defined.

- [List of configuration items in .mdf](../mdf/)
- [List of all messages](../messages/)

### Others

- [Delivering content on Web](../web-content/)

For more details, please refer to each document.
