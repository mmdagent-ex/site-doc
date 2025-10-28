---
title: Motion layering
slug: motion-layer
---
# Motion layering

To achieve highly interactive conversations, you need to dynamically perform composite actions in response to events during a dialogue — for example, "bow while speaking", "stop waving mid-wave when spoken to and listen", or "notice something mid-sentence and continue talking". MMDAgent-EX provides a mechanism to combine multiple partial motions and play them in parallel for this purpose.

Below is a schematic of motion layering. In the figure, Glance.vmd moves only the head and face, and Response.vmd moves the hands and facial expression (these are "partial motions"). All motions are evaluated in parallel, and overlapping parts are resolved by applying the motion with higher priority (blending or additive behavior is also possible depending on settings). With this mechanism, you can combine motions on the fly according to user input or context and play them to realize complex real-time behaviors.

![motion blending](/images/motion_blending.png)

Below we introduce and explain how to use this mechanism through the motion layering demo included in the Example.

## Try the motion layering demo in Example

There is a motion layering demo in the Example `example_motion` folder — let's run it.

    example/
        |- example_motion/
             |- example_motion.fst         FST script
             |- example_motion.mdf         .mdf file
             |- gaze.vmd                   motion: gaze
             |- onehandwave.vmd            motion: waving a hand
             +- walk.vmd                   motion: walking

Start `example_motion.mdf` with MMDAgent-EX. It will start with the motion `walk.vmd` looping as shown below.

{{< figure src="/mov/walk.gif" alt="walking gene" width="400px">}}

In this state, pressing the 1 key makes Gene glance toward you. This overlays the gaze motion `gaze.vmd` (just looking to the left) on top of the walking motion.

{{< figure src="/mov/walk-gaze.gif" alt="gazing while walking" width="400px">}}

Pressing 2 overlays the waving motion `onehandwave.vmd`. `onehandwave.vmd` defines only a smiling facial expression and the right-arm motion; by layering it over the walking and gaze motions you can see how to control behavior like "glance and greet at arbitrary timings".

{{< figure src="/mov/all.gif" alt="walking, gazing, and smiling" width="400px">}}

## Running example

If you look at the .fst script `example_motion.fst` used in the demo above, you can see it is written so that pressing the 1 key after startup plays `gaze.vmd` and pressing the 2 key plays `onehandwave.vmd` via MOTION_ADD.

{{<fst>}}
0 LOOP:
    <eps> STAGE|../images/floor_block.png,../images/back_white.png
    <eps> MODEL_ADD|gene|../gene/Gene.pmd
    MODEL_EVENT_ADD|gene  MOTION_ADD|gene|base|walk.vmd|FULL|LOOP
    <eps> CAMERA|0,11.25,0|13.5,-50.0,0|46.4|27.0

LOOP LOOP:
    KEY|1 MOTION_ADD|gene|look|gaze.vmd|PART|ONCE

LOOP LOOP:
    KEY|2 MOTION_ADD|gene|greet|onehandwave.vmd|PART|ONCE
{{</fst>}}

Here `walk.vmd` is given the alias "base", `gaze.vmd` is "look", and `onehandwave.vmd` is "greet". These concurrently played motions are managed independently and can each be controlled with `MOTION_DELETE` or `MOTION_CHANGE`.

Pressing the b key during playback displays information about currently running motions. Below is an example (press b again to hide it). The green text shows the model name. The cyan names below are the motion aliases, listed from lowest to highest priority. The pink lines are a simplified visualization of the bones each motion animates.

![bone debug displays list of motion aliases in priority order](/images/bone.png)

## Details of layered playback

This section explains the detailed specification of the `MOTION_ADD` message relevant to layered playback.

### Specifying partial motions

When overlaying motions, the overlaying motion should be started as a "partial motion" that controls only the parts that move, rather than as a full-body motion.

To play a motion as a partial motion, specify "PART" as the 4th argument to `MOTION_ADD` like this:

{{<message>}}
MOTION_ADD|gene|look|gaze.vmd|**PART**|ONCE
{{</message>}}

A motion started as a partial motion ignores bones and morphs that have no motion defined in the file (i.e., only defined on frame 0), and applies only those bones and morphs that have keyframes from frame 1 onward.

To treat a motion as a full-body motion, specify **FULL**. The default when omitted is FULL.

### Specifying loop playback

By default a motion is removed after it plays to its last frame. You can specify that it loops back to the first frame instead.

To loop a motion, specify **LOOP** as the 5th argument to `MOTION_ADD`. A motion with LOOP returns to frame 0 after the last frame and continues playing indefinitely. Looping stops when you issue `MOTION_DELETE` or remove the model.

{{<message>}}
MOTION_ADD|gene|base|walk.vmd|FULL|**LOOP**
{{</message>}}

To explicitly specify one-time playback, use **ONCE**. The default when omitted is ONCE.

### Toggling smoothing

MMDAgent-EX automatically applies motion smoothing at the start and end of motions to avoid visible jumps at seams when layering motions. If you need to disable this smoothing for some reason, specify OFF as the 6th argument.

{{<message>}}
MOTION_ADD|gene|look|gaze.vmd|PART|ONCE|**OFF**
{{</message>}}