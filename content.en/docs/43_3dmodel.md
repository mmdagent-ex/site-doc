

---
title: Displaying 3D Models
slug: 3d-model
---

# Displaying 3D Models

We use the .pmd format, which is a 3D model format of MikuMikuDance, and it can display any .pmd format objects including humanoid models. Also, [PMX models can be displayed by conversion](../pmx).

## Displaying and Deleting Models

You can display multiple models within a scene. Adding, swapping and deleting models in the scene are done through messages.

{{< details "The maximum number of models that can be displayed at the same time is 10." close >}}
If this is not enough, please set the upper limit as follows with .mdf.
{{< mdf>}}
max_num_model=20
{{< /mdf>}}
{{< /details >}}

### Adding Models to a Scene

Use the **MODEL_ADD** message to load a model and add it to the scene. In the example below, `agent1` is the alias (model alias) for referencing the loaded model later.

{{<message>}}
MODEL_ADD|agent1|some/where/model.pmd
{{</message>}}

You can specify the display position and direction of the model with arguments. For example, to rotate it 30 degrees around the Y-axis at the coordinates (8,0,0), specify as follows. The default is facing forward on the scene origin (0,0,0).

{{<message>}}
MODEL_ADD|agent1|some/where/model.pmd|8,0,0|0,30,0
{{</message>}}

If the display is successful, a **MODEL_EVENT_ADD** event message will be issued as follows. By monitoring this, each module can detect that the model display has started and its model alias.

{{<message>}}
MODEL_EVENT_ADD|agent1
{{</message>}}

### Swapping

If you `MODEL_ADD` with the same alias as the model in operation, it will result in an error. If you want to swap out the .pmd of the displayed model, use the **MODEL_CHANGE** message.

{{<message>}}
MODEL_CHANGE|agent1|some/where/other.pmd
{{</message>}}

If successful, a **MODEL_EVENT_CHANGE** event message will be issued as follows. Each module can detect that the displayed model has been changed/updated with this message.

{{<message>}}
MODEL_EVENT_CHANGE|agent1
{{</message>}}

### Deleting

To delete a model in operation, use **MODEL_DELETE**.

{{<message>}}
MODEL_DELETE|(model alias)
{{</message>}}

When successful, a **MODEL_EVENT_DELETE** event message will be issued as follows. Each module can detect that a model has been deleted from the scene with this message.

{{<message>}}
MODEL_EVENT_DELETE|agent1
{{</message>}}

## Mounting to Other Models

With `MODEL_ADD`, you can position a model on global coordinates, but you can also mount it to another model. The mounted model will move in sync with the model it's mounted to. This can be used, for example, when placing accessories on a character. To mount a model named obj.pmd to the `head` bone of `agent1`, issue the following message.

{{<message>}}
MODEL_ADD|object1|/some/where/obj.pmd|0,0,0|0,0,0|ON|agent1|head
{{</message>}}

When specifying a mount, the coordinates and rotation specified in `MODEL_ADD` are treated as relative coordinates (local coordinates) based on the destination bone, not as global coordinates.

The Example includes a glasses model `glasses/glasses.pmd` as a sample. Try issuing the following message to make Gene wear glasses.

{{<message>}}
MODEL_ADD|glass|glasses/glasses.pmd|0,-.30,.02|0,0,0|ON|0|head
{{</message>}}

<img alt="gene with glasses" src="/images/gene_with_glasses.png"/>

## Configuration Parameters

Here are the main .mdf configuration items related to model display.

- The duration (in seconds) to display the internal comments of the model when loading. 0 for no display.

{{< mdf>}}
display_comment_time=0
{{< /mdf>}}

- The maximum number of models that can be displayed in a scene. The minimum is 1, the maximum is 1024. Default is 10.

{{< mdf>}}
max_num_model=10
{{< /mdf>}}

- The strength of the anti-aliasing (MSAA). The larger the value, the smoother the lines will be displayed. 0 to turn it off. Default is 4.

{{< mdf>}}
max_multi_sampling=4
{{< /mdf>}}

- The thickness of the toon edges

(You can also change it with `K`, `Shift+K`)

![bold edge](/images/edge1.png)
![thin edge](/images/edge2.png)

{{< mdf>}}
cartoon_edge_width=0.35
{{< /mdf>}}

## Messages on Model Load/Deletion

You can set up the system to issue specific messages when a model is loaded or deleted. This allows you to perform operations directed by the model, such as "add menus and buttons when the model is loaded" or "change the background simultaneously when the model is loaded".

For a model named `xxx.pmd`, you would create a text file named `xxx.pmd.loadmessage` and write one message per line in it. This way, when this model `xxx.pmd` is loaded, the messages written in `xxx.pmd.loadmessage` are executed in order immediately after loading.

Similarly, by writing `xxx.pmd.deletemessage`, you can specify the messages to be issued when the model is deleted.

For example, by specifying the [change background](../scene) command in `xxx.pmd.loadmessage` as follows, you can change the background at the same time as you load the model.

```text
STAGE|stage/tatami_room/tatami_room.pmd
```

Below is the content of `Gene.pmd.loadmessage` set in the actual "Gene" model. When the Gene model is loaded, it is written to add a menu to turn the accessory ON/OFF.

```text
MENU|ADD|Gene
MENU|SETITEM|Gene|0|No Cheek|MODEL_BINDFACE|0|Total Cheek Wipe|1
MENU|SETITEM|Gene|1|With Cheeks|MODEL_BINDFACE|0|Total Cheek Wipe|0
MENU|SETITEM|Gene|2|No Mesh|MODEL_BINDFACE|0|No Mesh|1
MENU|SETITEM|Gene|3|With Mesh|MODEL_BINDFACE|0|No Mesh|0
MENU|SETITEM|Gene|4|No Hair Clip|MODEL_BINDFACE|0|No Hair Clip|1
MENU|SETITEM|Gene|5|With Hair Clip|MODEL_BINDFACE|0|No Hair Clip|0
```