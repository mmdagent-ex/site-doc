

---
title: Specification for Network Operations with Plugin_Remote
slug: plugin-remote
---

This document explains the use of Plugin_Remote for external integration.

## Specifications

- Messages are sent in text mode, separated by a newline "\n" for each message.
- Parts that start with `SND` embed the packet length and are sent in binary mode.
- Reset to initial values for each disconnection → Value setting messages are sent again for each new connection

```text
__AV_START
  This is the external operation start flag. Upon receiving this, MMDAgent-EX will control the model according to the received information until __AV_END is received.

__AV_END
  This is the external operation end flag. Upon receiving this, MMDAgent-EX will pause external operations until __AV_START is received again.

__AV_SETMODEL, model alias
  This specifies the name of the model to be operated externally. Upon receiving this, MMDAgent-EX will make the model operating under the specified name the target of subsequent operations.

__AVCONF_DISABLEAUTOLIP,{NO|ARKIT|AU|ARKIT+AU|ALWAYS}
  This specifies when not to perform automatic lip-sync from the transmitted voice during voice transmission. The default is `NO`, which means to always perform lip-sync.

__AV_EXMORPH,name=rate,name=rate,...
  This is for external control of arbitrary morphs. Specify the strength of the morph corresponding to the name specified by name. The value is [0..1]. The name used here and the morph to be operated actually need to be specified in the shapemap as "EXMORPH_name bone name".

__AV_MESSAGE,string
  Send string as a control message to MMDAgent-EX. Any message can be specified.

SNDSTRM
  Treat subsequent SND parts as voice streams and enable VAD. (default)

SNDFILE
  Treat subsequent SND parts as file chunks and disable VAD. Voice file transmission is done in three steps: (1) send SNDFILE, (2) send voice data in SND part, (3) send termination signal with SNDBRKS.

SNDBRKS
  Cut off the incoming voice here.

Parts that start with SND
  Voice data. Specifications are described later.
```


## Specifications for Audio Transmission

Audio data is encoded using the method explained below and sent to the same socket as the external operation. The `xxxx` below is a 4-digit number, which represents the byte length of the following data body in 4-digit decimal format. Only data of 16kHz, 16bit, and mono is accepted. In order to avoid delay when transmitting long audio, please try to divide it into short segments of about 40ms (1280 Bytes) and transmit them sequentially.

```text
Per packet: Header 7bytes + Body
   String "SND"   From 1st to 3rd byte
   Number "xxxx"   From 4th to 7th byte, decimal
   Sound data body  From 8th byte to (value of xxxx + 7) byte
```

By default, MMDAgent-EX assumes that the incoming audio is long-term streaming media such as microphone recording, and it performs voice interval detection on the incoming audio, treating the detected voice intervals as units for processing. When sending an audio file as a unit, first send `SNDFILE\n` once to switch modes, then sequentially transfer the contents of the file with `SND`. When you finish transmitting to the end of the file, send `SNDBRKS\n` to signal the end of input to MMDAgent-EX.

## Model Configuration Files for External Operation (.shapemap)

If you want to perform external operations, you need to prepare a configuration file (.shapemap) for each CG model (.pmd) you want to operate, specifying which morph in the model corresponds to the lip signal, etc. This configuration file (.shapemap) is placed in the same folder as the model file (`xxx.pmd`) with the name `xxx.pmd.shapemap`. Please define this .shapemap for every model you use for external operation.

The configuration file (.shapemap) is a text file, and its content is as follows. Lines starting with `#` are ignored as comments.

```text
#### Morph name for lip sync
LIP_A a
LIP_I i
LIP_U u
LIP_O o

#### List of morph names to be reset to zero during lip sync
#### Specify all the morphs that open the mouth other than those specified above
NOLIP e, oo~, WA, eh, ah, ii, scream, are, mouth laugh, mouth_a_geo_C, mouth_i_geo_C, mouth_u_geo_C, mouth_e_geo_C, mouth_o_geo_C, mouth_oh_geo_C, mouth_smile_geo_C, mouth_surprise_geo
```

## ".pmd.loadmessage" and ".pmd.deletemessage" Files (MS only)