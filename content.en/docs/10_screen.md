---
title: Screen overview
slug: screen
---
# Screen overview

Sample screen during content playback:

![Sample screen](/images/screen.png)

### (1) Display state

Current display state. Toggle showing ON/OFF by the `s` key.

- `60.0fps` display frame rate (fps)
- `4x MSAA` anti-aliasing (MSAA) level
- `[AL<number>]` AutoLuminous (per-part emission) intensity
- `S` shadow display mode: S = projected shadow, SM = shadow map (heavier), none = no shadow
- `[DF<number|number>]` Diffusion Effect intensity and range

### (2) Error messages

If a system error occurs, the error details appear here.

### (3) Connection status

Icons indicate the connection state during WebSocket communication.

- ![Net Icon](/images/icon1.png): Connection to the WebSocket server
- ![Screen Icon](/images/icon2.png): Transmitting screen capture to the server (not implemented)
- ![Video Icon](/images/icon3.png): Transmitting audio and webcam video to the server (not implemented)

### (4) Connection messages

When using WebSocket server connection feature, related messages are shown when the connection state with the WebSocket server changes.

### (5) Help & guide

Contextual help and guides are shown based on current actions.

### (6) Tab bar

- **home**: Open the home content
- **readme**: View the README attached to the playing content
- **bookmark**: Open bookmarks
- **history**: Open history
- **menu**: Open the menu