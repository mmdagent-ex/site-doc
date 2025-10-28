---
title: Changes Since the Original MMDAgent
slug: changes-since-original-mmdagent
---
# Changes Since the Original MMDAgent

This summarizes the main changes from [MMDAgent](https://www.mmdagent.jp/) to MMDAgent-EX.

### Display

- Added menus
- [Bottom tab bar](../screen)
- [Detailed log view](../log/) (`Shift+f`)
- Errors are now persistently displayed on-screen ([see screen](../screen))

### Features

- Content playback history (`Shift+H`)
- Open FST in editor (`E`: Windows only)
- Open folder in Explorer (`Shift+E`: Windows only)
- Screenshot (`Shift+G`)
- Change view with mouse: off by default (toggle with `c`)
- Camera reset (`Shift+C`)

### Post Effects

- AutoLuminous effect (adjust intensity with `Shift+L`)
- Diffusion effect (adjust intensity with `O` and `I`; Windows only)
- Double-shadow effect (`Shift+J`)

### 3D Models

- [PMX model support and compatibility improvements](../pmx/)
- [Enhanced motion blending between motions](../motion-layer/)
- Animated PNG support

### FST Extensions

[Expanded FST format](../fst-format/) (legacy format still supported)

- Block definitions
- Regular expressions
- Local variable initial values
- Access to global variables (KeyValue)
- Access to environment variables
- VS Code extension

### Speech Recognition

- Performance improvements: engine, acoustic models, and language models updated to the latest DNN-based versions
- Provides English models in addition to Japanese

### Multimodal

- [Enhanced image and text display features](../image-and-text/)

### External Integration

- [Added Plugin_AnyScript for embedding arbitrary programs](../submodule/)
- [Improved external audio playback](../remote-speech/)
- [Improved socket connections](../remote-control/)
  - [Added WebSocket support](../remote-websocket/)
- [External control per morph](../motion-bind/)

### mdf and Message Extensions

Many settings and messages have been added.

- [List of mdf settings](../mdf/)
- [List of messages](../messages/)

### Other

- [Web content](../web-content/)

For details, see the individual documents.