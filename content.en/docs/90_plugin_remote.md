---
title: Network operation specification using Plugin_Remote
slug: plugin-remote
---
External integration with Plugin_Remote.

## Specifications

- Send each message in text mode, separated by a newline "\n"
- `parts starting with SND` are sent in binary mode with the packet length embedded
- Reset to default values on each disconnection → value-setting messages must be resent on each new connection

```text
__AV_START
  Flag to start external control. When MMDAgent-EX receives this, it will operate the model according to received data until it receives __AV_END.

__AV_END
  Flag to end external control. When MMDAgent-EX receives this, it will suspend external control until it receives __AV_START again.

__AV_SETMODEL,model_alias
  Name of the model to be targeted by external control. When MMDAgent-EX receives this, it will target the model running under the specified name for subsequent operations.

__AVCONF_DISABLEAUTOLIP,{NO|ARKIT|AU|ARKIT+AU|ALWAYS}
  Specifies when to disable automatic lip-sync derived from transmitted audio during audio transmission. Default is `NO`, meaning lip-sync is always performed.

__AV_EXMORPH,name=rate,name=rate,...
  External control of arbitrary morphs. Specify the intensity for the morph corresponding to name. Values are in [0..1]. The names used here must be mapped to actual morphs in the shapemap, e.g. using a mapping like "EXMORPH_name bone name".

__AV_MESSAGE,string
  Send string as a control message to MMDAgent-EX. Any message string is allowed.

SNDSTRM
  Treat subsequent SND parts as an audio stream and enable VAD (default).

SNDFILE
  Treat subsequent SND parts as file chunks and disable VAD. Sending an audio file is a three-step process: (1) send SNDFILE, (2) send audio data in SND parts, (3) send SNDBRKS as end signal.

SNDBRKS
  Mark a boundary for the audio sent so far.

SND-started parts
  Audio data. Specification described below.

```

## Audio transmission specification

Audio data is encoded as described below and sent to the same socket used for external control. In the following, `xxxx` is four decimal digits that indicate the byte length of the following data payload. Only 16 kHz, 16-bit, mono data is supported. To avoid latency, do not send long audio in one chunk; split it into short segments of about 40 ms (around 1280 bytes) and stream them sequentially.

```text
Per pack: header 7 bytes + payload
   String "SND"    bytes 1–3
   Number "xxxx"   bytes 4–7, four decimal digits
   Audio payload   bytes 8–(xxxx + 7)
```

By default, MMDAgent-EX treats incoming audio as long streaming media such as microphone input, performs voice activity detection (VAD) on the incoming audio, and processes detected speech segments as units. If you want to send an entire audio file as a single unit, first switch mode by sending `SNDFILE\n`, then transfer the file contents via consecutive `SND` parts. After the file end has been sent, send `SNDBRKS\n` to notify MMDAgent-EX that input has finished.

## Model configuration file for external control (.shapemap)

For each CG model (.pmd) you want to control externally, you must provide a configuration file (.shapemap) that specifies which model morphs correspond to lip signals and other mappings. Place this .shapemap file in the same folder as the model file (`xxx.pmd`) with the name `xxx.pmd.shapemap`. Models used for external control must have this .shapemap defined.

The configuration file (.shapemap) is a text file and looks like the example below. Lines beginning with `#` are comments and ignored.

```text
#### Morph names for lip-sync
LIP_A あ
LIP_I い
LIP_U う
LIP_O お

#### List of morph names to reset to zero during lip-sync
#### Specify all mouth-opening morphs other than those listed above
NOLIP え,おお~,ワ,えー,ああ,いい,叫び,あーれー,口わらい,mouth_a_geo_C,mouth_i_geo_C,mouth_u_geo_C,mouth_e_geo_C,mouth_o_geo_C,mouth_oh_geo_C,mouth_smile_geo_C,mouth_surprise_geo
```

## ".pmd.loadmessage" and ".pmd.deletemessage" files (MS only)