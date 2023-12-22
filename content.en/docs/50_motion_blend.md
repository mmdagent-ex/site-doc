

---
title: Motion Blending
slug: motion-blend
---

# Motion Blending

In overlaying motions, there can be conflicts in the actions directed by multiple motions. For example, in the [example of the "Motion Overlay" page](../motion-layer), when overlaying a walking motion and a hand waving motion, the actions of swinging the arm back and forth by `walk.vmd` and the action of raising the hand and waving it left and right by `onehandwave.vmd` overlap for the right arm bone of the character.

This article explains how to resolve such overlapping actions.

## Overwrite, Add, Multiply

The default behavior in the event of overlap is "overwrite". That is, the motion with the highest priority is adopted, and all other motions are ignored. The motion that started last has the highest priority. In the example, the action of waving left and right by `onehandwave.vmd` was prioritized over the action by `walk.vmd`.

You can change this behavior upon overlap by issuing a **MOTION_CONFIGURE** message after adding the motion. You can specify one of the following three types.

- **MODE_REPLACE**: Overwrite
- **MODEL_ADD**: Add
- **MODEL_MUL**: Multiply (morphs only)

The default `MODE_REPLACE` overwrites the lower-ranking motion. If you specify `MODEL_ADD`, the motion will be "added" to the movement of the lower-ranking motion. `MODEL_MUL` multiplies the morph value indicated by this motion by the amount of morph calculated from the lower-ranking motion.

{{<message>}}
MOTION_CONFIGURE|(model)|(motion)|MODE_REPLACE
MOTION_CONFIGURE|(model)|(motion)|MODE_ADD
MOTION_CONFIGURE|(model)|(motion)|MODE_MUL
{{</message>}}

For example, addition can be used to add fluctuation or adjust offset, which can do similar things to ["Multi-stage bones"](https://www.google.com/search?q=%E5%A4%9A%E6%AE%B5%E3%83%9C%E3%83%BC%E3%83%B3) in MMD. Also, multiplication can be used to "specify 0 to disable the morph changes of some lower-ranking motions".

## Blend Rate

Along with the above specifications, you can also specify a blend rate for each motion. The blend rate can be any value from 0.0 to 1.0, with 1.0 being the default if not specified.

{{<message>}}
MOTION_CONFIGURE|(model)|(motion)|MODE_REPLACE|(rate)
MOTION_CONFIGURE|(model)|(motion)|MODE_ADD|(rate)
MOTION_CONFIGURE|(model)|(motion)|MODE_MUL|(rate)
MOTION_CONFIGURE|(model)|(motion)|BLEND_RATE|(rate)
{{</message>}}

When stacking motions, the processing such as overwriting or addition is performed after multiplying by this blend rate. Specifically, it works as follows:

- MODE_REPLACE + specified rate: The motion is overwritten with the movement obtained by multiplying the motion amount by the rate
- MODE_ADD + specified rate: The movement obtained by multiplying the motion amount by the rate is added
- MODE_MUL + specified rate: The change indicated by the motion is multiplied by the change obtained by multiplying the rate

Also, you can change the value of the rate without changing the setting with `BLEND_RATE`.

## Bone-level Control

Additionally, while the above is a specification for the entire motion, you can also set details on a bone-by-bone basis. Please refer to the reference for details.