---
title: External API 
slug: api
---

{{< hint ms >}}
The following content on this page is exclusive to the Moonshot version.
{{< /hint >}}

# External API

You can directly control MMDAgent-EX from an external program via socket communication. In addition to [standard message send/receive control](../remote-control/), the MS version has extra external API for using CG agents as avatars.  Below is an explanation of how to use it.

## Connecting to MMDAgent-EX

When using the external API from an external program, connect to MMDAgent-EX via a socket from the external program.  For methods of socket connection, please see the page ["Control via Socket Connection"](../remote-control/).

{{< hint warning >}}
Use WebSocket connections. Some features are not supported with TCP/IP connections.
{{< /hint >}}

## Specifications and Messages

Specification and the list of messages to be sent from outer program to MMDAgent-EX are as follows:

- Always append `\n` at the end of the message.
- For sending multiple messages in one transmission, append "\n" at the end of each message, like `Message1\nMessage2\n`.
- Use binary transmission mode of WebSocket.
- Settings will be reset when the socket is disconnected.
- Most of these messages are for avatar usage only, and will not be sent to the internal message queue.  Instead, any message not in the following list will be accepted and sent to internal message queue as normal socket connection behavior.

```text
__AV_SETMODEL,model_alias_name
__AV_AUTOCALIBRATE,{true|false}
__AV_AUTORETRACT,{true|false}
__AV_START
__AV_END
__AV_RECALIBRATE
__AV_ACTION,idx
__AVCONF_ALLOWFARCLOSEMOVE,{true|false}
__AV_TRACK,x,y,z,rx,ry,rz,eyeLrx,eyeLry,eyeLrz,eyeRrx,eyeRry,eyeRrz,flag
__AV_ARKIT,shape=rate,shape=rate,…
__AV_AU,num=rate,num=rate,…
__AV_EXBONE,name,x,y,z,rx,ry,rz,name,x,y,z,rx,ry,rz,…
__AV_EXBONEQ,name,x,y,z,rx,ry,rz,rw,name,x,y,z,rx,ry,rz,rw,…
__AV_EXMORPH,name=rate,name=rate,…
__AVCONF_DISABLEAUTOLIP,{NO|ARKIT|AU|ARKIT+AU|ALWAYS}
SNDSTRM
SNDFILE
SNDBRKS
SNDxxxx(body)
AVATAR_LOGSAVE_START|logfile.txt
AVATAR_LOGSAVE_STOP
AVATAR_EVENT_IDLE|START
AVATAR_EVENT_IDLE|STOP
```

## Basics for Tracking

In this API, especially the "tracking messages" (**__AV_TRACK**, **__AV_ARKIT**, **__AV_AU**, **__AV_EXBONE**, **__AV_EXMORPH**） will directly controls the CG agent.  Here is some basics you should know when using these tracking messages.

- Tracking will be applied only to the model specified by the **__AV_SETMODEL** message.  You should specify which model to control by **__AV_SETMODEL** before start tracking.
- Tracking will take effect after sending **__AV_START**, and ends at sending **__AV_END**.  Tracking messages after **__AV_END** will be ignored.
- Tracking control precedes autonomous actions: in case the tracking movement collides with autonomous motions on a bone or a morph, the movement by autonomous action will be disregarded and tracking movement will be taken.
- Tracking message gives target parameter to MMDAgent-EX, and MMDAgnet-EX will make the model move towards the specified parameter.  You can send messages successively at most 60fps for real-time control.
- "Auto Calibration" for head tracking is enabled by default.  Enabling this function makes MMDAgent-EX to use the first arriving 10 messages of **__AV_TRACK** to calibrates the orientation of the user's face.  You can disable or enable this feature by **__AV_AUTOCALIBRATE** message.
- "Auto Retraction" while no signal is enabled by default.  When enabled, if a tracking message is not sent for a while (default is 1 second), the motion control will stop temporarily, and will be resume at a new tracking message.  When disabled the last tracking state will be always maintained. You can disable or enable this ffeature by **__AV_AUTORETRACT** message.
- MMDAgent-EX will issue "avatar control idle" message.  It will issue **AVATAR_EVENT_IDLE|START** if any message has not been sent for 15 seconds.  When a message arrives after that, it will issue  **AVATAR_EVENT_IDLE|STOP**.

## Details of each message

### Start, End, Settings, and Logging

#### AV_SETMODEL,alias_name

Specifies the model to be operated on by the external API. All commands of external API are applied to the model specified in this message. Be sure to do this before starting tracking.

{{<message>}}
__AV_SETMODEL,0
{{</message>}}

- Specify the model by its alias name.
- If the alias name is not found, this message is ignored.
- Even during tracking control, it is possible to change the target model by this message at any time.
- Only one model can be operated on at the same time.

#### __AV_AUTOCALIBRATE

Disable/Enable automatic head orientation calibration.

The "automatic head orientation calibration" is a feature to calibrate the orientation of the operator's face and the webcam in face tracking.

When enabled, the first 10 instances of **__AV_TRACK** messages are saved without being applied, and their average is used as the correct position of the face in the subsequent **__AV_TRACK** messages.

When disabled, the values sent in **__AV_TRACK** will be applied as are, without no modification.

Enabled by default, and can be disabled / enabled by sending the following message:

To disable auto calibration,

{{<message>}}
__AV_AUTOCALIBRATE,false
{{</message>}}

To enable auto calibration,

{{<message>}}
__AV_AUTOCALIBRATE,true
{{</message>}}

#### __AV_AUTORETRACT

Disable/Enable automatic motion retraction.

The auto-retract function is a feature to avoid freezing of CG avatar in case of blank opertaion.

When enabled, when a situation occurs in which no tracking messages has been sent for a while (default is 1 second), MMDAgent-EX temporarily leaves tracking control. Subsequent new tracking messages will automatically restart to the tracking state.

When disabled, this automatic control leaving does not take effect: the tracking result is always kept and shown during tracking control.

Recommended: enable this at real-time tracking, and disable this at discrete control.  If you continuously send tracking messages during operation, turning this function ON can prevent the avatar from freezing in case of communication errors or tracking mistakes. Conversely, if you control the posture discretely, having it ON will cut off control after 1 second of giving the posture, so turning it OFF in such cases will maintain the last posture.

To disable the auto-retract feature,

{{<message>}}
__AV_AUTORETRACT,false
{{</message>}}

To enable the auto-retract feature,

{{<message>}}
__AV_AUTORETRACT,true
{{</message>}}

To set auto-retract wait time and enable it,

{{<message>}}
__AV_AUTORETRACT,seconds
{{</message>}}

Note: setting `0` is not equivalent to `false`.  Use `false` when you totally disable this feature.

#### __AV_START

Start tracking control.  After this message, the following tracking messages seize the part of the CG avatar's body and starts avatar operation through tracking messages (**__AV_TRACK**, **__AV_ARKIT**, **__AV_AU**, **__AV_EXBONE**, **__AV_EXMORPH**).

{{<message>}}
__AV_START
{{</message>}}

- MMDAgent-EX will issue message **AVATAR|START** and also set a KeyValue `Avatar_mode=1.0` when this message is received.
- Tracking messages (**__AV_TRACK**, **__AV_ARKIT**, **__AV_AU**, **__AV_EXBONE**, **__AV_EXMORPH**) will take effect after this.
- Model to be controlled should be specified prior to this by **__AV_SETMODEL** message.

#### __AV_END

Ends tracking control.  Control of body by external API is turned OFF. A tracking message (**__AV_TRACK**, **__AV_ARKIT**, **__AV_AU**, **__AV_EXBONE**, **__AV_EXMORPH**) that is sent during OFF will be ignored.

{{<message>}}
__AV_END
{{</message>}}

- MMDAgent-EX will issue message **AVATAR|END** and set a KeyValue `Avatar_mode=0.0` when this message is received.

#### AVATAR_LOGSAVE_START, AVATAR_LOGSAVE_STOP

Tell MMDAgent-EX to save all the sent messages into text file.

{{<message>}}
AVATAR_LOGSAVE_START|logfile.txt
AVATAR_LOGSAVE_STOP
{{</message>}}

#### __AV_RECALIBRATE

Tell MMDAgent-EX to perform calibration right now. When auto-calibration is enabled, MMDAgent-EX will perform calibration using the first **__AV_TRACK** messages.  This message activates the calibration from now.

{{<message>}}
__AV_RECALIBRATE
{{</message>}}

### Dialogue Actions

#### __AV_ACTION,number

Play the pre-defined dialogue action.  Give a number to play.  This works independently with tracking, even if tracking is not started.

{{<message>}}
__AV_ACTION,3
{{</message>}}

- The motion corresponding to the given number will be played on the target model as [part motion](../motion-layer)
- The started motion will play for once, not looped.
- Newer **__AV_ACTION** will override the older one which is still playing.
- Tracking control overrides dialogue action. The override will take effect per bone or face: only the bones and faces controlled by the tracking will be superceded.

The motion file that corresponds to the number is defined in [.shapemap file](../shapemap) at MMDAgent-EX side.  **__AV_ACTION** with undefined number will be ignored.  At CG-CA models, the following 39 actions are defined.

```text
ActionNumber Description
 0  ノーマル/ normal
 1  喜び/ joy, happy
 2  笑い/ laugh, amusing
 3  笑顔/ smile
 4  微笑/ little smile, agreement
 5  固い笑顔/ graceful smile
 6  照れ笑い/ embarassed smile
 7  困り笑い/ annoyed smile
 8  驚き・ショック/ surprise
 9  意外/ unexpected
10  感動/ impressed, excited
11  感心/ admired
12  期待・興味/ expectant, interested
13  納得・理解/ convinced
14  きりっと/ crisp, prepared
15  キメ顔/ proud, confident
16  考え中/ thinking
17  とんでもない/ no thank you (with smile)
18  同情・気遣い/ compassion, caring
19  ドヤ顔/ triumphant
20  困った/ in trouble, annoyed
21  軽い拒否・叱り/ no, accuse, disgust
22  謝り/ apology
23  緊張/ stressed
24  恥ずかしい/ embarassing
25  ジト目/ sharp eyes, suspicion
26  くやしい/ mortifying
27  煽り/ provoking
28  眠い/ sleepy
29  焦り・怖ろしい/ impatience, fear, terrible
30  呆然・唖然/ stunned, devastated
31  落胆/ disappointed
32  イライラ/ irritated, frustrated
33  怒り/ anger, furious
34  哀しみ/ sad
35  怖い/ afraid
36  不安・心のざわつき/ anxious
37  感傷的/ sentimental
38  恥じ入る/ ashamed
```

You can define new actions in .shapemap file.  The action number can be from 0 to 99.  For example, when you want to add greeting motion (ojigi.vmd) as dialogue action of number 40, you should add the line below to .shapemap file.  Note that the .vmd file path is relative to where .shapemap file exists, not the current directory.

```text
ACT40 somewhere/ojigi.vmd
```

After that, you can play the greeting action by sending **__AV_ACTION** with number `40`.

{{<message>}}
__AV_ACTION,40
{{</message>}}

### Head Tracking

#### __AV_TRACK,x,y,z,rx,ry,rz,eyeLrx,eyeLry,eyeLrz,eyeRrx,eyeRry,eyeRrz,flag

Send head and eye target parameters for head tracking.  MMDAgent-EX will then control the related bones of the target model according to the message.  Sending this message continuously will perform realtime head tracking.

- **x,y,z**: head movement (mm)
- **rx,ry,rz**: head rotation on X axis, Y axis and Z axis (radian)
- **eyeLrx,eyeLry,eyeLrz**: left eye rotation (radian)
- **eyeRrx,eyeRry,eyeRrz**: right eye rotation (radian)
- **flag**: eye rotation is global(1) or local(0)

The unit of the movement is millimeter.

Head rotation should be given as amount of local rotations around X axis, Y axis and Z axis in radian.  Note that all the rotation should be given as left-handed coordination system.

Eye rotation also should be given as X/Y/Z axis rotation in radian.

The **flag** is eye rotation flag. It should be set to `0` when the eye rotation is given in local rotation (i.e. relative to head).  It can be `1` if eye rotations are given in global (i.e. absolute rotation in world coordinates).  If you are going to send tracking parameters given by OpenFace, you should set this flag to `1`.  For Apple ARKit parameters, this should be set to `0`.

This **flag** will also switches how the given eye rotations are treated.  When this **flag** is set to `1`, the rotations of left eye and right eye are averaged to one and then the same averated rotation wil lbe applied to both eyes using the "both-eye" bone.  This forced normalization is to ensure that both eye has exactly the same direction in OpenFace.

When **__AV_AUTOCALIBRATE** is enabled (this is default), MMDAgent-EX assumes the first head position and rotation as the normal position, and calibrate the following sent parameters by the average of the first 10 messages.  This auto calibration can be disabled by **__AV_AUTOCALIBRATE,false**.

MMDAgent-EX does not just apply the head parameters to head of CG agent, instead it performs movement enhancement for CG-tailored tracking movement.  In addition to the head and eye of CG agent, it also controls body according to the head parameters.  The actual name of the bones that head tracking should be managed is defined in [.shapemap](../shapemap) file of the target model: `TRACK_HEAD`, `TRACK_NECK`, `TRACK_LEFTEYE`, `TRACK_RIGHTEYE`, `TRACK_BOTHEYE`, `TRACK_BODY`, `TRACK_CENTER`.  The distributed CG-CA model already has the following definitions, so you have to do nothing for CG-CA models.  For models other than CG-CA, you can start by just copying the .shapemap file to the new model, since the model structure is almost the same.

```text
TRACK_HEAD 頭
TRACK_NECK 首
TRACK_LEFTEYE 左目
TRACK_RIGHTEYE 右目
TRACK_BOTHEYE 両目
TRACK_BODY 上半身2,上半身２,上半身1,上半身
TRACK_CENTER センター
```

When you define multiple bone names as in the `TRACK_BODY` above, MMDAgent-EX will search for the bone of the name in its order, and the first found one will be adopted.

When you feel that the eye rotations of the CG model is too large or too small, check the eye rotation coefficient as defined in the .shapemap file.  Giving larger value will make CG model to rotate more.

```text
# Coef. of eye rotations
EYE_ROTATION_COEF 0.4
```

The sent head and eye rotations are applied to the bodies of the CG model with re-scaling.  The rescaling factors can be modified by defining the following items in .mdf file (the values are default values). 
Larger value makes more movement.

{{<mdf>}}
# Coef. of BODY rotation from head rotation
Plugin_Remote_RotationRateBody=0.5
# Coef. of NECK rotation from head rotation
Plugin_Remote_RotationRateNeck=0.5
# Coef. of HEAD rotation from head rotation
Plugin_Remote_RotationRateHead=0.6
# Coef. of CENTER up/down movement from head rotation
Plugin_Remote_MoveRateUpDown=3.0
# Coef. of CENTER left/right movement from head rotation
Plugin_Remote_MoveRateSlide=0.7
{{</mdf>}}

If you want to get the behaviors mirrored, set the following in your .mdf file.

{{<mdf>}}
# enable mirrored movement
Plugin_Remote_EnableMirrorMode=true
{{</mdf>}}

#### AVCONF_ALLOWFARCLOSEMOVE,value

Switch whether to apply forward/backward movement of the head parameters to modfel.  `true` will apply, and `false` will not.  The default is `true`.

{{<message>}}
__AVCONF_ALLOWFARCLOSEMOVE,true
{{</message>}}

### Facial tracking: Apple AR Kit

#### __AV_ARKIT,name=rate,name=rate,...

Send a set of shape target rates. Send this continously to perform real-time face tracking. The `name=rate,...` part is a set of shape names and its rates [0..1].  Any number of shape names can be sent at a message.

MMDAgent-EX will assign the received shape rates to model's morphs.  The mapping from the given shape names in the **__AV_ARKIT** message and the actual morph names in the target CG agent model SHOULD BE DEFINED IN THE [.shapemap](../shapemap) FILE at the model side.  The shape names undefined in the shapemap file will be ignored.

For simple example, assume you are going to control eye blink.  You are going to use a string `blink` as the shape name, whereas the target CG model has a blink morph as `まばたき`.  In this case, first define its mapping in the .shapemap file of the target model like this:

```text
blink まばたき
```

Then, you can send parameters like this to control it.  Value of `1.0` will make model blink, or `0.0` to unblink.

{{<message>}}
__AV_ARKIT,blink=1.0
{{</message>}}

The example above is a simplest case.  For actual facial tracking, you need every facial morphs to be moved according to the facial capture results.  CG-CAs are all equipped with 52 special morphs corresponding to [blendShapes](https://developer.apple.com/documentation/arkit/arfaceanchor/2928251-blendshapes) in [Apple ARKit](https://developer.apple.com/documentation/arkit/) facial tracking parameters, and its mapping has been already defined in their . shapemap files.

{{< details "ARKit compliant mappings defined in CG-CA shapemap" close>}}
```
browDown_L browDownLeft 
browDown_R browDownRight 
browInnerUp browInnerUp 
browOuterUp_L browOuterUpLeft 
browOuterUp_R browOuterUpRight 

cheekPuff cheekPuff 
cheekSquint_L cheekSquintLeft 
cheekSquint_R cheekSquintRight 

eyeBlink_R eyeBlinkRight 
eyeBlink_L eyeBlinkLeft 
eyeLookDown_L eyeLookDownLeft 
eyeLookDown_R eyeLookDownRight 
eyeLookIn_L eyeLookInLeft 
eyeLookIn_R eyeLookInRight 
eyeLookOut_L eyeLookOutLeft 
eyeLookOut_R eyeLookOutRight 
eyeLookUp_L eyeLookUpLeft 
eyeLookUp_R eyeLookUpRight 
eyeSquint_L eyeSquintLeft 
eyeSquint_R eyeSquintRight 
eyeWide_L eyeWideLeft 
eyeWide_R eyeWideRight 

jawForward jawForward 
jawLeft jawLeft 
jawOpen jawOpen 
jawRight jawRight 

mouthClose mouthClose 
mouthDimple_L mouthDimpleLeft 
mouthDimple_R mouthDimpleRight 
mouthFrown_L mouthFrownLeft 
mouthFrown_R mouthFrownRight 
mouthFunnel mouthFunnel 
mouthLeft mouthLeft 
mouthLowerDown_L mouthLowerDownLeft 
mouthLowerDown_R mouthLowerDownRight 
mouthPress_L mouthPressLeft 
mouthPress_R mouthPressRight 
mouthPucker mouthPucker 
mouthRight mouthRight 
mouthRollLower mouthRollLower 
mouthRollUpper mouthRollUpper 
mouthShrugLower mouthShrugLower 
mouthShrugUpper mouthShrugUpper 
mouthSmile_L mouthSmileLeft 
mouthSmile_R mouthSmileRight 
mouthStretch_L mouthStretchLeft 
mouthStretch_R mouthStretchRight 
mouthUpperUp_L mouthUpperUpLeft 
mouthUpperUp_R mouthUpperUpRight 

noseSneer_L noseSneerLeft 
noseSneer_R noseSneerRight 

tongueOut tongueOut 
```
{{< /details >}}

You should not mix using this message with AU based tracking (**__AV_AU**).

### Facial Tracking: Action Unit (AU)

#### __AV_AU,num=rate,num=rate,...

This message performs facial tracking based on AU ([Action Unit](https://en.wikipedia.org/wiki/Facial_Action_Coding_System)).  MMDAgent-EX controls facial morphs according to the sent AU parameters.  Sending this message continuously to perform real-time facial tracking based on AU.

Repeat `num=rate` part to send several AU parameters.  The `num` should be an index of Action Unit (from 1 to 46), and the rate should be from 0.0 to 1.0.  A rate value larger than 1.0 will be truncated to 1.0.

Action Unit does not directly corresponds to facial morphs, so you should define how morphs should be controlled for each AU parameters in [.shapemap](../shapemap) file at CG model side.  The following is an example of assigning AU number 6 (cheek raiser) to `笑い` (laughing eye) morph, number 1 (inner brow raiser) to `上` (brow raise), and number 4 (brow lowerer) to `困る` (annoying brow).

```text
AU6 笑い >0.7
AU1 上 0.5
AU4 困る
```

- `AUnumber morphName`: assign the sent rate to morph rate as is.
- `AUnumber morphName >value`: threshold-based: when the sent rate is above value, assign 1.0 to the morph, else 0.0 to the morph.
- `AUnumber morphName value`: rate-multiplied: the sent rate will be multiplied by the given value and then assigned to the morph. The value should be positive.

You can control several morphs with one AU parameter, and also several AU parameters can be summed up to a morph.

- When you repeat assigning different morphs to an Action Unit, they are all active: the sent AU rates will be applied to all mapped morphs.
- When AUs are mapped to the same morph, all the sent AU parameter values are summed up to the target morph.

You should not mix using this message with another tracking message **__AV_ARKIT**.

### Extra Bone Control

#### __AV_EXBONE, __AV_EXBONEQ

Controls a bone via API.  Any bone on the target model can be controlled.

- Auto calibration is not performed on this message.
- Auto retraction will be applied to this message.

Use **__AV_EXBONE** to give a rotation parameter by rotations around X-axis, Y-axis and Z-axis, or else use **__AV_EXBONEQ** to express rotation in quaternion.

{{<message>}}
 __AV_EXBONE,name,x,y,z,rx,ry,rz,rw,name,x,y,z,rx,ry,rz,rw,...**
{{</message>}}

- **name**: boneControlName
- **x,y,z**: moves (mm)
- **rx,ry,rz**: rotations around X-axis, Y-axis and Z-axis (radian)

{{<message>}}
 __AV_EXBONEQ,name,x,y,z,rx,ry,rz,rw,name,x,y,z,rx,ry,rz,rw,...**
{{</message>}}

- **name**: boneControlName
- **x,y,z**: moves (mm)
- **rx,ry,rz,rw**: rotation quaternion (radian)

The mapping of `boneControlName` used in the message above and the actual bone name in the target CG model should be defined in the model-side [.shapemap](../shapemap) file.  As shown below, the `name` part should be the boneControlName as used in the message, and `boneName` specifies actual bone name defined in the model.

{{<message>}}
EXBONE_name boneName
{{</message>}}

Example: you are going to control CG model's both arms with API.  To do this, first write the following lines in .shapemap file to define the control name `RUarm` and `LUarm` to be mapped to `右腕` (right upper arm) and `左腕` (left upeer arm) bones in the CG model.

```text
EXBONE_RUarm 右腕
EXBONE_LUarm 左腕
```

Then, send **__AV_EXBONE** or **__AV_EXBONEQ** to control them.

{{<message>}}
__AV_EXBONE,RUarm,0,0,0,0,0.8,0,LUarm,0,0,0,0,0.5,0
{{</message>}}

The control name should be unique to each corresponding bones.

Note: CG model has special bones like "IK bones" and "Physics-simulated bones".  Those are controlled by computation inside MMDAgent-EX. You can still give parameters to such bones but the result may not be what you expected.

### Extra Morph Control

#### __AV_EXMORPH,name=rate,name=rate,...

Control arbitrary morph via API.

- **name**: controlMorphName
- **rate**: morph value (from 0.0 to 1.0)

The mapping of `controlMorphName` used in the message above and the actual morph name in the target CG model should be defined in the model-side [.shapemap](../shapemap) file.  The `name` part in the following example should be the a `controlMorphName` to be sent, and `morphName` specifies actual mophr name to be controlled in the model.

{{<message>}}
EXMORPH_name morphName
{{</message>}}

The control name should be unique to each corresponding bones.

### Voice Transmission

Audio waveform data can be streamed via a socket and played back with lip-sync. This works even when not in tracking control mode.  The audio data should be raw waveform data in 16kHz, 16bit, mono format, other format is not acceptable.

There are two modes of voice transmission: File mode and Streaming mode.

In File mode, the audio data is sent in short chunks as described above (it's also possible to send the entire audio in one large chunk), and a speech end signal is sent at the end. MMDAgent-EX starts playing the audio upon receiving the first chunk, outputs the transmitted audio data.  When end-of-utterance message arrives, it ends the session and closes the lip-sync mouth.

In Streaming mode, audio transmission needs to be done in short chunks. Since no explicit speech end is given, MMDAgent-EX detects speech intervals from the detection of silent parts.

The default is Streaming mode. To switch to File mode, first send `SNDFILE` to change the mode, then sequentially transfer the contents of the file with `SND`. When you have finished transmitting the end of the file, send `SNDBRKS` to inform MMDAgent-EX that the input has ended. To switch back to Streaming mode, send `SNDSTRM`.

#### SNDxxxx(body)

Transmit audio data.  The `xxxx` is a 4-digit number representing the byte length of the data body in decimal, following the header.  To avoid delays, it's better to send the audio in short segments of about 40 ms (1280 Bytes) rather than sending long audio all at once.  This message does not require last `\n`.

Python example of sending an audio chunk:

```python
async def send_audio(chunk_data, chunk_bytes):
    header = ("SND" + f"{chunk_bytes:04}").encode('ascii')
    payload = bytearray()
    payload = header + chunk_data
    await websocket.send(payload)
```

#### SNDFILE

Switch to File mode.

- MMDAgent-EX play the sent audio as is, not try to detect voice part.
- Required to send `SNDBRKS` after an utterance has been sent.

{{<message>}}
SNDFILE
{{</message>}}

#### SNDBRKS

Send end-of-utterance for File mode.

{{<message>}}
SNDBRKS
{{</message>}}

#### SNDSTRM

Switch to Streaming mode.

- MMDAgent-EX detects voice part and only plays the part

{{<message>}}
SNDSTRM
{{</message>}}

#### __AVCONF_DISABLEAUTOLIP,{NO|ARKIT|AU|ARKIT+AU|ALWAYS}

When using facial tracking and voice transmission together, the mouth shape calculated by automatic lip-sync sometimes conflict with the mouth shape specified by facial tracking.  `__AVCONF_DISABLEAUTOLIP` is a message to set the handling of automatic lip-sync during these conflicts.

One of the following options can be specified. If not specified, the default is NO.

- **NO**: Always apply lip-sync. In case of a conflict, the mouth shapes from both lip-sync and facial tracking are added together and displayed.
- **ARKIT**: Stops the automatic lip-sync while receiving **__AV_ARKIT** messages.
- **AU**: Stops the automatic lip-sync while receiving **__AV_AU** messages.
- **ARKIT+AU**: Stops the automatic lip-sync while receiving either **__AV_ARKIT** or **__AV_AU** messages.
- **ALWAYS**: Turns off the automatic lip-sync feature totally, do nothing.
