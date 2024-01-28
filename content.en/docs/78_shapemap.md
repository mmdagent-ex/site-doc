---
title: Shapemap
slug: shapemap
---

{{< hint ms >}}
The content of this page is for MS version only.
{{< /hint >}}

# Shapemap file

Shapemap file (.shapemap) is a definition file for lip-sync and external API control for CG avatars. It specifies which parts of the CG model should be controlled by lip-sync and tracking commands from external APIs.

The structure and composition of parts in CG models vary greatly between models. Therefore, complete bone / morph mappings should be given at each CG model by the .shapemap file.

## File Placement

The Shapemap file (.shapemap) should be placed in the same folder as the CG avatar's model file `xxx.pmd`, with a filename like `xxx.pmd.shapemap`, appending `.shapemap` after the model file name. Note that it should be `xxx.pmd.shapemap`, not `xxx.shapemap`.

When using a CG agent as an avatar, make sure to prepare a .shapemap file for each model. If a Shapemap file is not available, the CG model will not operate in response to external APIs and automatic lip-sync.

For complete reference, see the Shapemap file of CG-CA. CG-CA comes with a Shapemap file already defined, and many MMD models have a similar structure, so they generally work fine as is. When setting up a new CG model, it's a good idea to start by copying the .shapemap file included with CG-CA.

## Example

The Shapemap file is a text file. Lines starting with `#` are comments and are ignored. Below is an example of a Shapemap file included with CG-CA.

{{< details "CG-CA .shapemap" close>}}

```text
#### Morphs for lip sync
LIP_A あ
LIP_I い
LIP_U う
LIP_O お

#### Morphs to be set to 0.0 while lip sync is ongoing
NOLIP え,おお~,ワ,∧,はんっ！,えー,にやり,にっこり,口締め,結び,む,ああ,いい,にたり,叫び,あーれー,口わらい,mouth_a_geo_C,mouth_i_geo_C,mouth_u_geo_C,mouth_e_geo_C,mouth_o_geo_C,mouth_oh_geo_C,mouth_smile_geo_C,mouth_surprise_geo

#### Head Tracking parameters
## bones to be controlled
TRACK_HEAD 頭
TRACK_NECK 首
TRACK_LEFTEYE 左目
TRACK_RIGHTEYE 右目
TRACK_BOTHEYE 両目
TRACK_BODY 上半身2,上半身２,上半身1,上半身
TRACK_CENTER センター
## eye rotation coefficient to tune amount of eye rotation
EYE_ROTATION_COEF 0.4

#### Preset motions for __AV_ACTION
ACT0  motion/00_normal.vmd
ACT1  motion/01_happy.vmd
ACT2  motion/02_laugh.vmd
ACT3  motion/03_smile.vmd
ACT4  motion/04_littlesmile.vmd
ACT5  motion/05_gracefulsmile.vmd
ACT6  motion/06_embarassedsmile.vmd
ACT7  motion/07_annoyedsmile.vmd
ACT8  motion/08_surprise.vmd
ACT9  motion/09_unexpected.vmd
ACT10 motion/10_impressed.vmd
ACT11 motion/11_admiration.vmd
ACT12 motion/12_expectant.vmd
ACT13 motion/13_convinced.vmd
ACT14 motion/14_crisp.vmd
ACT15 motion/15_proud.vmd
ACT16 motion/16_thinking.vmd
ACT17 motion/17_nothankyou.vmd
ACT18 motion/18_compassion.vmd
ACT19 motion/19_triumphant.vmd
ACT20 motion/20_introuble.vmd
ACT21 motion/21_disgust.vmd
ACT22 motion/22_apology.vmd
ACT23 motion/23_stressed.vmd
ACT24 motion/24_embarrasing.vmd
ACT25 motion/25_sharpeyessuspicion.vmd
ACT26 motion/26_mortifying.vmd
ACT27 motion/27_provoking.vmd
ACT28 motion/28_sleepy.vmd
ACT29 motion/29_Terrified.vmd
ACT30 motion/30_stunned.vmd
ACT31 motion/31_disappointed.vmd
ACT32 motion/32_frustrated.vmd
ACT33 motion/33_angry.vmd
ACT34 motion/34_sad.vmd
ACT35 motion/35_Afraid.vmd
ACT36 motion/36_Anxious.vmd
ACT37 motion/37_Sentimental.vmd
ACT38 motion/38_Ashamed.vmd

#### Bone mapping for __AV_EXBONE
#EXBONE_name boneName

#### Morph mapping for __AV_EXMORPH
#EXMORPH_name モーフ名

#### Facial tracking by Action Unit
## AU to morph
AU6 笑い >0.7
AU1 上 0.5
AU2 上 0.5
AU4 困る
AU5 見開き
AU12 にこり
AU45 まばたき
## Morph tune setting
MORPH_TUNE 笑い まばたき

#### Facial tracking by Shapes
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

# hapihapi

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

## 書式

Below, we explain the configurable items group by group.

### Lip sync

Specifies the mouth shape morphs used for automatic lip-sync. The names of the morphs that correspond to the Japanese sounds "あ" (A), "い" (I), "う" (U), and "お" (O) should be specified with `LIP_A`, `LIP_I`, `LIP_U`, and `LIP_O`, respectively.

```text
LIP_A あ
LIP_I い
LIP_U う
LIP_O お
```

You can specify a list of morphs that should be always set to 0 during automatic lip-sync using `NOLIP`. This feature is to prevent the expression from becoming strange due to the overlap of automatic lip-sync and dialogue actions or autonomous motions. Typically, you would specify all the mouth-related morphs in the model other than the four mentioned above.

```text
NOLIP え,おお~,ワ,∧,はんっ！,えー,にやり,にっこり,口締め,結び,む,ああ,いい,にたり,叫び,あーれー,口わらい,mouth_a_geo_C,mouth_i_geo_C,mouth_u_geo_C,mouth_e_geo_C,mouth_o_geo_C,mouth_oh_geo_C,mouth_smile_geo_C,mouth_surprise_geo
```

### 対話アクション

Specify the motion files corresponding to the numbers in the dialogue action playback messages by the external API (`__AV_ACTION,number`). Write the one or two-digit number following `ACT`, and the path to the corresponding motion file, as shown below.

Note that the relative path is interpreted as relative to the folder where this .shapemap file is placed, not relative to the current directory.

```text
ACT0  motion/00_normal.vmd
ACT1  motion/01_happy.vmd
...
ACT38 motion/38_Ashamed.vmd
```

### Head Tracking

Specify the bone names that are the target of the head tracking message (**__AV_TRACK**). All of the following ones should be specified.

Multiple bone names can be specified, separated by commas. If multiple names are specified, the bone name is searched from left to right within the model, and the first one found is used.

```text
TRACK_HEAD 頭
TRACK_NECK 首
TRACK_LEFTEYE 左目
TRACK_RIGHTEYE 右目
TRACK_BOTHEYE 両目
TRACK_BODY 上半身2,上半身２,上半身1,上半身
TRACK_CENTER センター
```

If the rotation amount of the eyes in tracking is too large or too small, adjust it using the following `EYE_ROTATION_COEF`. A larger value results in greater rotation, and a smaller value results in less rotation.

```text
EYE_ROTATION_COEF 0.4
```

### Individual Bone Control

Define mapping from control name to bone name for **__AV_EXBONE**.
Use the format as shown below. The `name` part should be the name as used in the message, and `boneName` specifies actual bone name defined in the model.

```text
EXBONE_name boneName
```

Example: you are going to control CG model's both arms with API.  To do this, write the following lines to define the control name s`RUarm` and `LUarm` to be mapped to `右腕` (right upper arm) and `左腕` (left upeer arm) bones in the CG model.

```text
EXBONE_RUarm 右腕
EXBONE_LUarm 左腕
```

Then, send **__AV_EXBONE** or **__AV_EXBONEQ** to control them.

{{<message>}}
__AV_EXBONE,RUarm,0,0,0,0,0.8,0,LUarm,0,0,0,0,0.5,0
{{</message>}}

The control name should be unique to each corresponding bones.

### Individual Morph Control

Define mapping from control name to morph name for **__AV_EXMORPH**.
Use the format as shown below. The `name` part should be the name as used in the message, and `morphName` specifies actual morph name defined in the model.

```text
EXMORPH_name morphName
```

In addition to just the morph name as mentioned above, it is also possible to specify threshold values and coefficients, similar to AU.

The control name should be unique to each corresponding bones.

### Facial Tracking by Action Unit

In facial tracking using AU (Action Units) (**__AV_AU**), define how morphs are moved in response to the values of Action Units. Describe the mapping settings to morphs one by one for each Action Unit received.

The following is an example of assigning AU number 6 (cheek raiser) to `笑い` (laughing eye) morph, number 1 (inner brow raiser) to `上` (brow raise), and number 4 (brow lowerer) to `困る` (annoying brow).

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

In AU-based control, settings to suppress excessive addition can be made using `MORPH_TUNE`. For example, in CG-CA, both `まばたき` and `笑い` are morphs related to opening and closing the eyes, but setting both to 1.0 would result in an overly squinted, unnatural expression. In such cases, it is possible to constrain so that the total of these multiple morphs after control does not exceed 1.0.

```text
MORPH_TUNE 笑い まばたき
```

`MORPH_TUNE` can be specified repeatedly, up to a maximum of 30 times. Also, the number of morphs that can be specified per instance is up to 10 morphs.

### Facial Tracking by Shapes

Any lines that do not fit the above descriptions are interpreted as the correspondence between shape names and the morph names for the facial tracking message **__AV_ARKIT**. If a shape specified in **__AV_ARKIT** is not defined in the mapping here, the operation with that shape name will be ignored.

All CG-CA models are built with 52 morphs for [Apple ARKit](https://developer.apple.com/documentation/arkit/) [blendShape](https://developer.apple.com/documentation/arkit/arfaceanchor/2928251-blendshapes) for face tracking, one by one to perform full face tracking based on ARKit.

So, the .shapemap file in CG-CA model already contains all the shape names mapping that fully supports ARKit. Note that the shape names described in the included .shapemap are not the names as defined on ARKit itself, but are written to match the names output by the app `iFacialMoCap`, which transmits facial capture information using ARKit.

In the specification, in addition to just the morph name, it is also possible to specify threshold values and coefficients, similar to AU.
