

---
title: Direct Specification of Bone Morph Values
slug: motion-bind
---

# Direct Specification of Bone Morph Values

Inside CG models, there may be morphs that switch appearances or bones that provide special movements. These morphs and bones can be incorporated into motions, but it can sometimes be more convenient to set fixed values for them separately from the motions.

In MMDAgent-EX, you can directly specify the values of bones and morphs that are not under the influence of motion through a message. For example, if the model of "Gene" is running, you can send the following message to hide the hair mesh.

{{<message>}}
MODEL_BINDFACE|0|No Mesh|1.0
{{</message>}}

Note that if the specified bone or morph is under the influence of motion, the motion side will take precedence.

## Setting Values

### MODEL_BINDBONE

This sets a value to the bone. `x,y,z` represents the amount of movement, and `rx,ry,rz` represents the amount of rotation.

{{<message>}}
MODEL_BINDBONE|(model alias)|(bone name)|x,y,z|rx,ry,rz
{{</message>}}

The value remains valid while the model is displayed. If successful, **MODEL_EVENT_BINDBONE** is output.

{{<message>}}
MODEL_EVENT_BINDBONE|(model alias)|(bone name)
{{</message>}}

### MODEL_BINDFACE

This sets a value to the morph. `(value)` represents the weight, ranging from 0.0 to 1.0. You can gradually change the value to the specified value over the specified `(transition_duration)` in seconds.

{{<message>}}
MODEL_BINDFACE|(model alias)|(morph name)|(value)
MODEL_BINDFACE|(model alias)|(morph name)|(value)|(transition_duration)
{{</message>}}

This also applies while the model is displayed. If the set is successful, **MODEL_EVENT_BINDFACE** is output.

{{<message>}}
MODEL_EVENT_BINDFACE|(model alias)|(morph name)
{{</message>}}

## Unbinding

### MODEL_UNBINDBONE

This unbinds the set value of the bone. It issues **MODEL_EVENT_UNBINDBONE** at the end.

{{<message>}}
MODEL_UNBINDBONE|model alias|bone name
MODEL_EVENT_UNBINDBONE|model alias|bone name
{{</message>}}

### MODEL_UNBINDFACE

This unbinds the set value of the morph. It issues **MODEL_EVENT_UNBINDFACE** at the end.

{{<message>}}
MODEL_UNBINDFACE|model alias|morph name
MODEL_EVENT_UNBINDFACE|model alias|morph name
{{</message>}}