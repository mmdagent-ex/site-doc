

---
title: Playing Motions
slug: motion-play
---

# Playing Motions

The basic procedure is to play motions by assigning a motion file (.vmd) to a model. Here we introduce the basic messages to play motions.

## Starting the Motion Playback

By specifying the motion file (.vmd) you want to play with the **MOTION_ADD** message, you can start the motion playback. `(model alias)` is the alias name of the target model, and `(motion_alias)` is the motion alias name given to the motion you are about to start.

{{<message>}}
MOTION_ADD|(model alias)|(motion alias)|file.vmd
{{</message>}}

If the specified model alias does not exist, or if the motion alias already exists, the system will output a Warning and does nothing.

At the time of starting the playback, the following **MOTION_EVENT_ADD** event message is issued.

{{<message>}}
MOTION_EVENT_ADD|(model alias)|(motion alias)
{{</message>}}

When the motion has been played to the end, it is automatically deleted, and a **MOTION_EVENT_DELETE** message is issued.

{{<message>}}
MOTION_EVENT_DELETE|(model alias)|(motion alias)
{{</message>}}

## Interrupting in the Middle

You can interrupt the motion being played with the **MOTION_DELETE** message.

{{<message>}}
MOTION_DELETE|(model alias)|(model alias)
{{</message>}}

When the motion is interrupted and deleted, a **MOTION_EVENT_DELETE** message is issued.

{{<message>}}
MOTION_EVENT_DELETE|(model alias)|(model alias)
{{</message>}}

## Switching to Another Motion

To switch the motion being played to another motion, use **MOTION_CHANGE**. After the switch, the playback of the switched motion starts.

{{<message>}}
MOTION_CHANGE|(model alias)|(motion alias)|other.vmd
{{</message>}}

If the switch is successful, **MOTION_EVENT_CHANGE** is issued at the same time as the playback of the switched motion starts from the beginning.

{{<message>}}
MOTION_EVENT_CHANGE|(model alias)|(model alias)
{{</message>}}

## Rewinding

To rewind the motion being played and start playing from the beginning, use **MOTION_RESET**.

{{<message>}}
MOTION_RESET|(model alias)|(motion alias)
{{</message>}}