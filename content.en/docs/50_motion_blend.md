---
title: Motion Blending
slug: motion-blend
---
# Motion Blending

When layering motions, the movements specified by multiple motions can conflict. For example, in the [example on the "Motion Layer" page](../motion-layer), when blending a walking motion with a one-hand wave motion, the character's right arm bone receives both the arm-swing from `walk.vmd` and the arm-raise/side-to-side motion from `onehandwave.vmd`.

This section explains how to resolve such overlapping motions.

## Replace, Add, Multiply

The default behavior for overlaps is "replace". In other words, the motion with the highest priority is used and lower-priority motions are ignored. Priority is determined by start time: the most recently started motion has the highest priority. In the example, the side-to-side motion from `onehandwave.vmd` took precedence over the `walk.vmd` motion.

You can change this overlap behavior by issuing a **MOTION_CONFIGURE** message after adding a motion. The available modes are:

- **MODE_REPLACE**: Replace (overwrite)
- **MODEL_ADD**: Additive
- **MODEL_MUL**: Multiply (morphs only)

The default `MODE_REPLACE` overwrites lower-priority motions. Specifying `MODEL_ADD` will add this motion's movement to the lower-priority motion's movement. `MODEL_MUL` multiplies the morph amount calculated by the lower-priority motion by the morph values indicated by this motion.

{{<message>}}
MOTION_CONFIGURE|(model)|(motion)|MODE_REPLACE
MOTION_CONFIGURE|(model)|(motion)|MODE_ADD
MOTION_CONFIGURE|(model)|(motion)|MODE_MUL
{{</message>}}

As an example use case, additive mode can be used to add subtle jitter or offsets, similar to MMD's ["multi-stage bone"](https://www.google.com/search?q=%E5%A4%9A%E6%AE%B5%E3%83%9C%E3%83%BC%E3%83%B3) setups. Multiply can be used to disable part of a lower-priority motion's morph changes by specifying 0, for instance.

## Blend Rate

In addition to the above mode, you can set a blend rate per motion. The value ranges from 0.0 to 1.0; the default is 1.0.

{{<message>}}
MOTION_CONFIGURE|(model)|(motion)|MODE_REPLACE|(rate)
MOTION_CONFIGURE|(model)|(motion)|MODE_ADD|(rate)
MOTION_CONFIGURE|(model)|(motion)|MODE_MUL|(rate)
MOTION_CONFIGURE|(model)|(motion)|BLEND_RATE|(rate)
{{</message>}}

When layering, the blend rate is multiplied into the motion before performing the replace/add/multiply operation. Concretely:

- MODE_REPLACE + rate: the motion's movement is multiplied by rate and then used to replace the lower-priority movement
- MODE_ADD + rate: the motion's movement is multiplied by rate and then added to the lower-priority movement
- MODE_MUL + rate: the change indicated by this motion is multiplied by rate and then used to multiply the lower-priority morph values

You can also use `BLEND_RATE` to change only the rate value without changing the mode.

## Per-bone control

The above applies to entire motions, but you can also configure these settings in detail on a per-bone basis. See the reference for details.