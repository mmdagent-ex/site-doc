

---
title: Motion Control
slug: motion
---

# Motion Control

The motion control of MMDAgent-EX is an extended version based on the specifications of MikuMikuDance. Here, we will explain the basic mechanism of motion control.

## Mechanism of Motion Control

Moving 3D models are defined not only by visual information such as vertices, faces, materials, and textures, but also by "bones" and "morphs" that move these elements. By manipulating the position and rotation of bones and the degree of morphs, various movements are performed. This series of movement patterns, combining bones and morphs, is called "motion".

{{< hint info >}}
The terminology varies depending on the application and tool, and there are 3D models that carry more diverse information. However, here we only deal with "bones" and "morphs" following MikuMikuDance.
{{< /hint >}}

In MMDAgent-EX, you start playing a motion by specifying a motion file (.vmd) for the model being displayed. By saving small units of motion in individual .vmd files in advance and sequentially playing these motion files according to the situation during a conversation, it is possible to perform real-time motion playback and control while conversing. Overlapping multiple motions and loop playback are also possible, allowing for real-time and flexible control.

Below, we will briefly explain the definitions and handling in MMDAgent-EX.

### What is a Bone

A bone is a control point for moving and rotating the entire model or a part of it. For humanoid models, dozens of bones are defined to simulate movable parts such as the head, arms, legs, and fingers. Display points (vertices, faces) that should follow the movement of each bone are defined, and when the bone is moved or rotated, the associated parts move.

Bones can have a hierarchical structure. If a "parent bone" is specified for a bone, the movement of the parent bone is propagated to the child bone. This hierarchical structure is necessary to reproduce movements of multi-joint parts like arms and legs.

Bone movements are defined on a "keyframe basis". Instead of every frame, the position and rotation at a specific time (keyframe) are defined, and during motion, frames between keyframes are automatically interpolated and played back from the values at both ends.

### What is Morph?

"Morph" is a term that means "transformation", and in 3D models, it defines the transformation pattern of parts. It defines the initial state and the state after transformation, and during execution, the "amount of change" is given as a value from 0.0 to 1.0, automatically generating the transformation from one state to another. It is mainly used for changes in facial expressions, as well as for transformations of parts. In humanoid 3D models for dialogue, dozens of morphs corresponding to various expressions are usually defined. Complex expressions and performances are created by combining multiple morphs.

A single morph consists of a set of model parameters and their values after transformation. The basic "vertex morph" changes the model by moving vertices, but there are also "bone morphs" that move the position of bones, "UV morphs" that move texture coordinates to change textures, and "material morphs" that change material information such as transparency and color. Furthermore, for ease of use, there are "group morphs" that bundle multiple morphs so that they can operate with a single parameter.

Morphs, like bones, are defined to operate based on keyframes. For each keyframe, specify the morph change amount (from 0.0 to 1.0). During execution, interpolation calculations are automatically performed between keyframes.

## Creating Motions

Please use MMD (MikuMikuDance) tools.

## Points to Note when Applying to Different Models

MikuMikuDance's motion (.vmd) files save the "names" of the target bones and morphs, and their respective sets of keyframes.

When playing a .vmd, it checks whether there are bones or morphs with the same name as the ones the .vmd file handles in the target model, and playback is only performed for bones and morphs with exactly matching names. Please be aware that the operation of bones and morphs not present in the model will be ignored.