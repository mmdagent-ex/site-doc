

---
title: Camera (Viewpoint)
slug: camera
---

# Controlling the Camera (Viewpoint)

By changing the camera (viewpoint), you can alter the direction and distance of an entire scene, including CG agents. It's also possible to create camera direction by setting a series of camera movements as motions.

The camera can also be operated with [keys and a mouse](../keybind-basic/#%e8%a6%96%e7%82%b9%e7%a7%bb%e5%8b%95). This section explains the following aspects of setting the camera viewpoint:

- Changing and setting the position and parameters
- Setting the speed of change
- Automatic tracking and bone mounting
- Playing back camera motion

## Setting the Camera

You can specify the viewpoint parameters with the **CAMERA** command.

- **x,y,z**: Camera position coordinates
- **rx,ry,rz**: Amount of camera rotation
- **distance**: Distance from the center of the screen to the camera
- **fovy**: Field of view (in degrees)

{{<message>}}
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)
{{</message>}}

When you press the `d` key, the second line of numbers that appears at the bottom left is the current value of the camera parameters. These are displayed in the same format as the one passed to the **CAMERA** message, so you can adjust the camera position with the keys or mouse and then use this displayed value.

![camera parameter on screen](/images/camera_param.png)

## Setting the Movement Speed

When you give a command to the camera parameters with the **CAMERA** message, the camera smoothly moves from its current state to the instructed position in about a second. If you want to change this camera movement speed, specify the **fifth argument** `transition time period`. By specifying a value larger than 0, it will move at a constant speed over the specified number of seconds. In the example below, it moves to the specified position over 5 seconds.

{{<message>}}
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)|5
{{</message>}}

By specifying 0, you can switch to the specified parameters immediately without any camera transition.

{{<message>}}
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)|0
{{</message>}}

The default when omitted is -1 (smooth movement).

## Auto-follow Models with the Camera

While navigating a scene, models may make large movements that take them outside the frame. In such cases, you can mitigate this problem by allowing the camera to automatically follow (only horizontally) the movements of the model.

To use this, enter the alias name of the model to follow as the sixth argument for the **CAMERA** parameter. When a model is specified, the camera first moves to the given parameters, and then begins to automatically follow the model's horizontal movements. (More precisely, it follows the model's "center" bone)

{{<message>}}
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)|1|(model alias)
{{</message>}}

In this case, the fifth argument, the transition time (shown as `1` above), specifies the camera's response to the model's movement. If set to `0`, the camera will closely follow the model's movement without any delay. By providing positive values, the camera can follow the model's movements with a certain amount of lag. Adjust this as per your requirement.

## Mounting the Camera on a Bone

By specifying a bone name following the model's alias, you can mount the camera on a specific bone and make it follow that. The principle is the same as the model auto-follow mentioned above.

{{<message>}}
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)|1|(model alias)|(bone name)
{{</message>}}

## Using Camera Motion

You can reproduce camera work by specifying a pre-defined camera motion file (.vmd). Camera motions can be created with the MMD tool. When using it, provide the camera motion file (.vmd) as shown below.

{{<message>}}
CAMERA|(camera motion file name)
{{</message>}}