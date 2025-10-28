---
title: Motion Control
slug: motion
---
# Motion Control

MMDAgent-EX's motion control is based on and extends the MikuMikuDance specification. This section explains the basic mechanism of motion control.

## How motion control works

A 3D model not only contains visual data such as vertices, faces, materials, and textures, but also defines "bones" and "morphs" that move those visuals. By changing bone positions/rotations and morph values, the model performs various motions. A sequence of movements combining these bones and morphs is called a "motion."

{{< hint info >}}
Names vary by use and tool and some 3D models include more diverse data, but here — following MikuMikuDance — we deal only with "bones" and "morphs."
{{< /hint >}}

In MMDAgent-EX, assigning a motion file (.vmd) to a displayed model starts playback of that motion. You can save small motion units as separate .vmd files and play them sequentially as needed during a conversation, enabling real-time motion playback and control while interacting. Multiple motions can be overlaid and looped, allowing flexible real-time control.

Below is a brief explanation of how MMDAgent-EX defines and handles these elements.

### Bones

Bones are control points used to move or rotate part or all of a model. For humanoid models, dozens of bones are typically defined to simulate movable parts such as the head, arms, legs, and fingers. Each bone has associated display points (vertices/faces), so moving or rotating a bone moves the linked parts.

Bones can be arranged in a hierarchy. If a bone has a parent bone, the parent's motion propagates to its child bones. This hierarchy is necessary to reproduce multi-joint movements like limbs.

Bone motion is defined on a keyframe basis. Instead of specifying values every frame, you define position and rotation at specific times (keyframes); during playback, frames between keyframes are automatically interpolated from the surrounding keyframe values.

### Morphs

A morph defines a deformation pattern. In a 3D model, it specifies the model’s shape before and after deformation; at runtime you give a morph an influence value from 0.0 to 1.0 to generate the in-between deformation automatically. Morphs are mainly used for facial expressions but also for deforming parts. Conversational humanoid models typically define dozens of expression morphs. Combining multiple morphs produces complex expressions and variations.

A morph consists of a set of target model parameters and their post-deformation values. The basic type is a vertex morph, which moves vertices to change the model. There are also bone morphs (move bone positions), UV morphs (shift texture coordinates), material morphs (change material properties such as transparency or color), and group morphs (wrap multiple morphs under a single parameter for convenience).

Morphs, like bones, are keyframe-based. Each keyframe specifies the morph value (0.0–1.0); values between keyframes are interpolated at runtime.

## Creating motions

Use MikuMikuDance or other MMD tools.

## Notes when applying motions to different models

A MikuMikuDance motion (.vmd) stores the names of the target bones and morphs and their respective keyframe sets.

When playing a .vmd, MMDAgent-EX checks whether the model contains bones and morphs with the exact names used by the .vmd. Only bones and morphs whose names match exactly will be played. Any motion targeting bones or morphs that do not exist in the model will be ignored.