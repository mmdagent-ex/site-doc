---
title: Motion Playback
slug: motion-play
---
# Motion Playback

The basic way to play motions is to give a model a motion file (.vmd). This section explains the basic messages used for motion playback.

## Starting Motion Playback

Send a **MOTION_ADD** message specifying the motion file (.vmd) you want to play to start playback. `(model alias)` is the alias name of the target model, and `(motion_alias)` is the alias to assign to the new motion.

{{<message>}}
MOTION_ADD|(model alias)|(motion alias)|file.vmd
{{</message>}}

If the model does not exist, the system will output a Warning and take no action.

If a motion with the specified motion alias is already playing, that motion will be overwritten by the new one.

When playback starts, the following **MOTION_EVENT_ADD** event message is emitted.

{{<message>}}
MOTION_EVENT_ADD|(model alias)|(motion alias)
{{</message>}}

When the motion finishes playing, it is automatically removed and a **MOTION_EVENT_DELETE** message is emitted.

{{<message>}}
MOTION_EVENT_DELETE|(model alias)|(motion alias)
{{</message>}}

## Interrupting Playback

Use the **MOTION_DELETE** message to interrupt a motion that is currently playing.

{{<message>}}
MOTION_DELETE|(model alias)|(model alias)
{{</message>}}

When a motion is interrupted and deleted, a **MOTION_EVENT_DELETE** message is emitted.

{{<message>}}
MOTION_EVENT_DELETE|(model alias)|(model alias)
{{</message>}}

## Switching to Another Motion

Use **MOTION_CHANGE** to replace a currently playing motion with another motion. After the replacement, the new motion will start playing.

{{<message>}}
MOTION_CHANGE|(model alias)|(motion alias)|other.vmd
{{</message>}}

If the replacement succeeds, a **MOTION_EVENT_CHANGE** is emitted and the new motion will start playing from the beginning.

{{<message>}}
MOTION_EVENT_CHANGE|(model alias)|(model alias)
{{</message>}}

## Rewinding

Use **MOTION_RESET** to rewind a motion that is playing and restart it from the beginning.

{{<message>}}
MOTION_RESET|(model alias)|(motion alias)
{{</message>}}