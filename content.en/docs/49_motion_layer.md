

---
title: Layering Motions
slug: motion-layer
---

# Layering Motions

To achieve high levels of interactivity in dialogue, it is necessary to dynamically perform complex actions in response to events that arise during conversation, such as "bowing while speaking", "stopping waving when spoken to and listening", or "noticing something while speaking and continuing the conversation". MMDAgent-EX has a mechanism to parallel play multiple partial motions combined for this purpose.

The following is a schematic diagram of layering motions. In the diagram, Glance.vmd is a motion that only moves the head and face, and Response.vmd is a motion (**partial motion**) that moves the fingers and facial expressions. All motions are calculated for posture in parallel, and the motion with higher priority is applied to the overlapping parts (blending or addition is also possible depending on the settings). With this mechanism, motions can be combined and played on the spot according to user input and situations, realizing complex movements in real time.

![motion blending](/images/motion_blending.png)

Below, we will introduce and explain how to use this mechanism through the demonstration of layering motions in the Example.


## Running the Motion Overlay Demo in Example

There's a motion overlay demo located in the `example_motion` folder of Example. Let's give it a try.

    example/
        |- example_motion/
             |- example_motion.fst         FST script
             |- example_motion.mdf         .mdf file
             |- gaze.vmd                   motion: gaze
             |- onehandwave.vmd            motion: waving a hand
             +- walk.vmd                   motion: walking

Please launch `example_motion.mdf` in MMDAgent-EX. It will start in a state where the `walk.vmd` motion is looping as shown below.

{{< figure src="/mov/walk.gif" alt="walking gene" width="400px">}}

In this state, pressing the `1` key will make Gene look at us. This is the "gaze.vmd" motion that only involves looking to the left, overlaid on the walking motion.

{{< figure src="/mov/walk-gaze.gif" alt="gazing while walking" width="400px">}}

Furthermore, pressing the `2` key will overlay the hand-waving motion `onehandwave.vmd`. The `onehandwave.vmd` motion only defines a smiling face and the movement of the right arm. By overlaying this on the walking and looking-left motions, you can observe how to control actions such as "looking at us and greeting at any time".

{{< figure src="/mov/all.gif" alt="walking, gazing, and smiling" width="400px">}}

## Motion Aliases and List Display

Looking at the `.fst` script `example_motion.fst` from the demo above, you can see that after the script is launched, pressing the `1` key triggers `gaze.vmd`, and pressing the `2` key triggers `onehandwave.vmd` to play, each under `MODEL_ADD`.

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

The `walk.vmd` is given the alias "base", `gaze.vmd` is "look", and `onehandwave.vmd` is "greet". These different motion aliases are managed independently and can be individually controlled with `MOTION_DELETE` or `MOTION_CHANGE`.

While in operation, you can press the `b` key to view information about the currently running motion. An example display is shown below (press `b` again to hide it). The model name is displayed in green, and the motion alias names are shown in light blue, listed in order of priority. The pink line is a simplified display of the motion of each bone being played.

![bone debug displays list of motion aliases in priority order](/images/bone.png)

## Detailed Overlay Playback

This section explains the detailed specifications of the `MOTION_ADD` message related to overlay playback.

### Specifying Partial Motions

When overlapping and playing motions, the motion to be overlaid later needs to start as a "**partial motion**", controlling only the moving parts rather than the full-body motion.

To play it as a partial motion, specify "**PART**" as the fourth argument in `MOTION_ADD` as shown below:

```
MOTION_ADD|gene|look|gaze.vmd|**PART**|ONCE
```

The motion started as a partial motion will ignore bones/morphs that are not defined to move (i.e., only defined at the 0th frame), and only the movements of bones/morphs that are defined to move (i.e., keyframes exist from the 1st frame onwards) will be applied.

If you want to treat it as a regular full-body motion, specify **FULL**. If omitted, the default is FULL.

### Specifying Loop Playback

In regular motion playback, the motion automatically disappears after playing up to the last frame. You can specify this to return to the first frame and loop playback.

If you want to loop the motion, specify **LOOP** as the fifth argument in `MOTION_ADD`. The loop-specified motion will return to the 0th frame after playing up to the last frame and will continue to play. Loop playback stops with `MOTION_DELETE` or by deleting the model.

```
MOTION_ADD|gene|base|walk.vmd|FULL|**LOOP**
```

To explicitly specify playback only once, specify **ONCE**. If omitted, the default is ONCE.

### Switching Smoothing

To avoid motion jumps at the seams during overlapping playback, MMDAgent-EX automatically adds motion smoothing at the start and end of the motion. If you want to turn this off for some reason, specify the sixth argument as OFF.

```
MOTION_ADD|gene|look|gaze.vmd|PART|ONCE|**OFF**
```