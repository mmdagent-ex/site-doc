---
title: Directly Setting Bone and Morph Values
slug: motion-bind
---
# Directly Setting Bone and Morph Values

Some CG models include morphs that change appearance and bones that provide special motions. These morphs and bones can be included in motions, but it can be convenient to set fixed values for them from a scenario independently of motions.

In MMDAgent-EX, you can directly specify the values of bones and morphs that are not under motion influence via messages. For example, while the "Gene" model is running, sending the following message will hide the hair mesh.

{{<message>}}
MODEL_BINDFACE|0|メッシュなし|1.0
{{</message>}}

Note that if the specified bone or morph is under the influence of a motion, the motion takes precedence.

## Setting values

### MODEL_BINDBONE

Sets values on a bone. `x,y,z` are translation amounts and `rx,ry,rz` are rotation amounts.

{{<message>}}
MODEL_BINDBONE|(model alias)|(bone name)|x,y,z|rx,ry,rz
{{</message>}}

The values remain effective while the model is displayed. On success, **MODEL_EVENT_BINDBONE** is emitted.

{{<message>}}
MODEL_EVENT_BINDBONE|(model alias)|(bone name)
{{</message>}}

### MODEL_BINDFACE

Sets a value on a morph. `(value)` is the weight from 0.0 to 1.0. If you specify the final `(transition_duration)`, the value will be smoothly changed to the specified value over that many seconds.

{{<message>}}
MODEL_BINDFACE|(model alias)|(morph name)|(value)
MODEL_BINDFACE|(model alias)|(morph name)|(value)|(transition_duration)
{{</message>}}

This also applies while the model is displayed. On success, **MODEL_EVENT_BINDFACE** is emitted.

{{<message>}}
MODEL_EVENT_BINDFACE|(model alias)|(morph name)
{{</message>}}

## Unbinding

### MODEL_UNBINDBONE

Unbinds a bone value. Emits **MODEL_EVENT_UNBINDBONE** on completion.

{{<message>}}
MODEL_UNBINDBONE|model alias|bone name
MODEL_EVENT_UNBINDBONE|model alias|bone name
{{</message>}}

### MODEL_UNBINDFACE

Unbinds a morph value. Emits **MODEL_EVENT_UNBINDFACE** on completion.

{{<message>}}
MODEL_UNBINDFACE|model alias|morph name
MODEL_EVENT_UNBINDFACE|model alias|morph name
{{</message>}}