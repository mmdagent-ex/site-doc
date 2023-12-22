---
title: Screen
slug: screen
---
# Screen

Here is a sample screen during content playback:

![Sample Screen](/images/screen.png)

### (1) Status

This part indicates the current status. You can toggle it by `s` key.

- `60.0fps` Display speed (fps)
- `4x MSAA` Anti-aliasing (MSAA) intensity
- `[AL number]` AutoLuminous intensity (part luminance)
- `S` Shadow display method
  - `S`: projection shadow
  - `SM`: shadow map rendeing (high graphical cost)
  - `none`: no shadow
- `[DF number|number]` Diffusion Effect intensity and range

### (2) Error Messages

If a system error occurs, the details of the error will be displayed here.

### (3) Network Status

Some icons may indicate current connection status when WebSocket communication is enabled.

- ![Net Icon](/images/icon1.png): Now communicating with WebSocket server
- ![Screen Icon](/images/icon2.png): Transmitting screen capture to the server (not yet implemented)
- ![Video Icon](/images/icon3.png): Transmitting audio and webcam video to the server (not yet implemented)

### (4) Network Communication Messages

Messages are displayed when the connection status is changed when connected with WebSocket server.

### (5) Help Guide

Help guide text may appear at this area according to the status.

### (6) Tab Bar

- **home**: Opens the home content
- **readme**: Views the README attached to the content currently playing
- **bookmark**: Opens bookmarks
- **history**: Opens history
- **menu**: Opens the menu
