---
title: Displaying 3D Models
slug: 3d-model
---
# Displaying 3D Models

This uses the MikuMikuDance 3-D model format (.pmd), so you can display any .pmd-format object, including humanoid models. [PMX models can also be displayed after conversion](../pmx).

## Adding and removing models

You can display multiple models in a scene. Adding, replacing, or removing models in the scene is done via messages.

{{< details "You can display up to 10 models at the same time." close >}}
If that is not enough, set a higher limit in the .mdf like this:
{{< mdf>}}
max_num_model=20
{{< /mdf>}}
{{< /details >}}

### Adding a model to the scene

Use the MODEL_ADD message to load a model and add it to the scene. In the example below, the `agent1` part is an alias name (model alias) used later to refer to the loaded model.

{{<message>}}
MODEL_ADD|agent1|some/where/model.pmd
{{</message>}}

You can specify the model's display position and orientation as arguments. For example, to place it at coordinates (8,0,0) and rotate 30 degrees around the Y axis:

{{<message>}}
MODEL_ADD|agent1|some/where/model.pmd|8,0,0|0,30,0
{{</message>}}

If the model is displayed successfully, a MODEL_EVENT_ADD event message like the following is emitted. Monitoring this lets other modules detect that the model has started displaying and obtain its model alias.

{{<message>}}
MODEL_EVENT_ADD|agent1
{{</message>}}

### Replacing a model

If you call MODEL_ADD with an alias already in use, it will fail. To replace the .pmd of a model currently displayed, use MODEL_CHANGE.

{{<message>}}
MODEL_CHANGE|agent1|some/where/other.pmd
{{</message>}}

On success, a MODEL_EVENT_CHANGE event message like the following is emitted. Other modules can use this to detect that the displayed model has been changed/updated.

{{<message>}}
MODEL_EVENT_CHANGE|agent1
{{</message>}}

### Deleting a model

To remove a model in use, use MODEL_DELETE.

{{<message>}}
MODEL_DELETE|(model alias)
{{</message>}}

On success, a MODEL_EVENT_DELETE event message like the following is emitted. Other modules can use this to detect that the model has been removed from the scene.

{{<message>}}
MODEL_EVENT_DELETE|agent1
{{</message>}}

## Mounting onto another model

MODEL_ADD places a model in global coordinates by default, but you can instead mount it onto another model. A mounted model follows the movement of its mount target — useful for attaching accessories to a character. For example, to mount obj.pmd onto the `頭` bone of `agent1`, send:

{{<message>}}
MODEL_ADD|object1|/some/where/obj.pmd|0,0,0|0,0,0|ON|agent1|頭
{{</message>}}

Note that when mounting, the position and rotation specified in MODEL_ADD are treated as relative to the mount bone (local coordinates), not as global coordinates.

An example includes the glasses model glasses/glasses.pmd. Try sending the following message to put glasses on Gene:

{{<message>}}
MODEL_ADD|glass|glasses/glasses.pmd|0,-.30,.02|0,0,0|ON|0|頭
{{</message>}}

<img alt="gene with glasses" src="/images/gene_with_glasses.png"/>

## Configuration parameters

Main .mdf settings related to model display are listed below.

- Duration (seconds) to display a model's internal comment when loading. Set to 0 to disable.

{{< mdf>}}
display_comment_time=0
{{< /mdf>}}

- Maximum number of models that can be displayed in a scene. Minimum is 1, maximum is 1024. Default is 10.

{{< mdf>}}
max_num_model=10
{{< /mdf>}}

- Anti-aliasing (MSAA) level. Higher values smooth lines more. Set to 0 to disable. Default is 4.

{{< mdf>}}
max_multi_sampling=4
{{< /mdf>}}

- Toon edge thickness

(Can also be changed with `K`, `Shift+K`)

![bold edge](/images/edge1.png)
![thin edge](/images/edge2.png)

{{< mdf>}}
cartoon_edge_width=0.35
{{< /mdf>}}

## Messages on model load and delete

You can arrange for specific messages to be sent to the system when a model is loaded or deleted. This lets a model instruct actions such as "add menu items or buttons when the model is loaded" or "change the background when the model is loaded."

For a model named xxx.pmd, create a text file named xxx.pmd.loadmessage and list one message per line. When xxx.pmd is loaded, the messages in xxx.pmd.loadmessage will be executed in order immediately after loading.

Similarly, create xxx.pmd.deletemessage to specify messages emitted when the model is deleted.

For example, by putting a [command to change the background](../scene) in xxx.pmd.loadmessage like this, the background will change when the model is loaded:

```text
STAGE|stage/tatami_room/tatami_room.pmd
```

Below is the actual contents of Gene.pmd.loadmessage used for the "Gene" model. It adds a menu for toggling accessories on/off when Gene is loaded.

```text
MENU|ADD|Gene
MENU|SETITEM|Gene|0|No Cheek|MODEL_BINDFACE|0|頬全消し|1
MENU|SETITEM|Gene|1|With Cheek|MODEL_BINDFACE|0|頬全消し|0
MENU|SETITEM|Gene|2|No Mesh hair|MODEL_BINDFACE|0|メッシュなし|1
MENU|SETITEM|Gene|3|With Mesh hair|MODEL_BINDFACE|0|メッシュなし|0
MENU|SETITEM|Gene|4|No Hair Clip|MODEL_BINDFACE|0|髪留なし|1
MENU|SETITEM|Gene|5|With Hair Clip|MODEL_BINDFACE|0|髪留なし|0
```
