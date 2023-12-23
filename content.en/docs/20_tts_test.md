---
title: Try Speech Synthesis
slug: tts-test
---
# Try Speech Synthesis

MMDAgent-EX by default has two speech synthesis engines, [Open JTalk](https://open-jtalk.sp.nitech.ac.jp/) for Japanese and [FLite+HTS_Engine](http://flite-hts-engine.sp.nitech.ac.jp/) for English.  They are HMM-based light-weight, small latency engines.

{{< hint info >}}
You may prefer another modern synthesis engines.  If so, try running it [outside and connect via socket](../remote-control/) or [run as sub-module](../submodule/), and [feed the synthesized speech data to MMDAgent-EX](../remote-speech/).
{{< /hint >}}

The example content has sample voice models for both engines.  This page explains the procedure to test the text-speech function.

## Before start

MMDAgent-EX plays synthesized speech from the default audio output device.  Please set the sound device you want to play the speech as the default output device.

## Run test

The dialogue script of the Example content is pre-configured to perform speech synthesis.  After the content is launched,

- Press `1` key to hear Japanese synthesized speech saying "こんにちは！よろしくね！", along with the lip sync of the CG model.
- Press `2` key to hear English voice saying "Hello! My name is gene. How can I help you?".

{{< details "How it works" close >}}
The dialogue script waits in the `LOOP` state after loading the model and motion as shown below. Here, pressing the keys issue the speech synthesis message **SYNTH_START**.

The engines has different voice name definitions (`mei_voice_*` for Open JTalk and `slt_voice_*` for FLite+HTS_Engine), and the matching engine will take action.  The voice name definition is in the file `main.ojt` for Open JTalk and `main.fph` for FLite+HTS_Engine in the example content.

{{<fst>}}
0 LOOP:
    <eps> STAGE|images/floor_green.png,images/back_white.png
    <eps> MODEL_ADD|0|gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0

LOOP LOOP:
    KEY|1 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！

LOOP LOOP:
    KEY|2 SYNTH_START|0|slt_voice_normal|"Hello! My name is gene. How can I help you?"
{{< / fst>}}

{{< /details >}}

## Messages to Start Speech Synthesis

The various modules of MMDAgent-EX, including the synthesis modules, communicate through [messages](../messages). Below, some messages for speech synthesis is briefly described.

> You can see the live message by [output log](../log/#several-ways-of-outputting-logs).

### SYNTH_START

The speech synthesis module executes speech synthesis when a **SYNTH_START** message was issued by other modules.  To tell module to start synthesizing speech, issue the following **SYNTH_START** message.

{{<message>}}
SYNTH_START|(model alias)|(voice name)|"utterance text."
{{</message>}}

The `(voice name)` specifies the voice name defined in the voice definition file. The `.ojt` file (defs for Japanese Open JTalk) and `.fph` file (defs for English FLite+HTS_Engine) with the same prefix of the content .mdf file will be loaded. In the example content, the following names are defined:

    # English voice names (FLite+HTS_Engine)
    # defined in main.fph
    slt_voice_normal
    slt_voice_fast
    slt_voice_slow
    slt_voice_high
    slt_voice_low

    # Japanese voice names (Open JTalk)
    # defined in main.ojt
    mei_voice_normal
    mei_voice_angry
    mei_voice_bashful
    mei_voice_happy
    mei_voice_sad
    mei_voice_fast
    mei_voice_slow
    mei_voice_high
    mei_voice_low

Please enter the synthesizing text in UTF-8.

### SYNTH_EVENT_START, SYNTH_EVENT_STOP

The voice synthesis module outputs messages in response to internal state changes. It outputs **SYNTH_EVENT_START** when voice output begins, and **SYNTH_EVENT_STOP** when the output ends. By monitoring these events, you can trigger actions at the start of the voice and wait for the voice output to finish.

{{<message>}}
SYNTH_EVENT_START|(model alias)
SYNTH_EVENT_STOP|(model alias)
{{</message>}}

## Try with Any Text via Web interface

While running MMDAgent-EX, open the following page on the same machine. [A textbox connected to MMDAgent-EX will be displayed](../message-test).

- <a href="http://localhost:50000" target="_blank">http://localhost:50000</a> (← Click to open in a new window)

Paste the following message into the textbox and press the Send button. Verify that a synthesized voice is produced.

{{<message>}}
SYNTH_START|0|slt_voice_happy|"Nice to meet you!"
{{</message>}}

### Related Files

The Open JTalk module is located in the `Plugins` subdirectory of the directory containing the executable file, and is named `Plugin_Open_JTalk.dll` (or .so).  The Flite+HTS_Engine is `Plugin_Flite_plus_hts_engine.dll` (or .so).

The voice models and its voice name configuration files should be prepared on the content side. In the example, voice models are in the `voice/mei` and `voice/slt` directory, and the configuration file is `main.ojt` and `main.fph`. The configuration file defines the "voice names" specified in the messages.
