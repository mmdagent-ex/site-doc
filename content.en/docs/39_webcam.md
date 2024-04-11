---
title: Virtual Webcam Casting
slug: webcam
---
{{< hint ms >}}
The functions described in this page is for MS version only.
{{< /hint >}}

# Virtual Webcam Casting

You can directly cast the screen of MMDAgent-EX via virtual webcam (Windows only).

Softcam is used to implement this feature:

- https://github.com/tshino/softcam

## Install

Install the [Softcam](https://github.com/tshino/softcam) driver to your PC beforehand.

Pre-compiled installer is included in the `Plugin_Webcam/softcam/` folder of the code repository. Run the `RegisterSoftcam.bat` script on 64 bit Windows, or another one if you are running 32 bit version to install it.

- `Plugin_Webcam/softcam/RegisterSoftcam.bat`: installer for 64-bit Windows
- `Plugin_Webcam/softcam/RegisterSoftcam32.bat`: installer for 32-bit Windows

After running the install script above, the "`DirectShow Softcam`" virtual webcam will be added to your system as a virtual webcam.  If your app or browser does not show it, try restarting it.

## How to use

Start MMDAgent-EX, and then issue `WEBCAM_START` message to start casting.

{{<message>}}
WEBCAM_START
{{</message>}}

In your streaming app (Meet, Zoom, Teams, etc.), select `DirectShow softcam` virtual webcam, and the screen of MMDAgent-EX will be sent as a webcam stream.

The screen region to be captured is fixed to the upper-left corner of MMDAgent-EX's window (default 1280x720).  You would probably need to adjust the app window size to fit it.

You can issue `WEBCAM_STOP` to stop the casting.

{{<message>}}
WEBCAM_STOP
{{</message>}}

## Auto start

You can tell MMDAgent-EX to start casting as soon as it starts, by setting the following in your .mdf file:

{{< mdf>}}
Webcam_Enable=true
{{< /mdf>}}

## Changing the cast region

The size of the capture region can be changed by setting the values `Webcam_Width` and `Webcam_Height` in your .mdf file.  The default values are 1280 and 720, respectively.  Note that the origin of the region is fixed to the upper-left corner of the MMDAgent-EX and you can only change the width and height.  For example, if you want to set the capture region size to 640x360, set the values like this:

{{< mdf>}}
Webcam_Width=640
Webcam_Height=360
{{< /mdf>}}

The captured image will be automatically rescaled inside the driver to the required size designated by the streaming app who opens the device (for example 1280x720 or 640x360).  As software capture is used in this system, setting larger region may improve image quality but consumes more CPU power and too large region will causes frame drop.  Setting smaller size will make it light-weight, but the casted image can be juggy.
