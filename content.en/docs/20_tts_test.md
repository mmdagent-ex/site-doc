---
title: Testing Speech Synthesis
slug: tts-test
---
# Testing Speech Synthesis

MMDAgent-EX includes Japanese [Open JTalk](https://open-jtalk.sp.nitech.ac.jp/) and English [FLite+HTS_Engine](http://flite-hts-engine.sp.nitech.ac.jp/) as default speech synthesis engines. These are lightweight, fast, and have low latency.

{{< hint info >}}
You can also integrate other engines into MMDAgent-EX. Options include running a synthesis engine as a separate process and [connecting via socket](../remote-control/), or embedding it as a [subprocess module](../submodule/). See also [feeding synthesized audio from an external process](../remote-speech/) for integration patterns.
{{< /hint >}}

The Example content includes voice models for both engines. Below are the steps to actually try speech synthesis using them.

## Preparation

Synthesis audio is played through the default audio output device. Before starting, set the sound device you want to use as the system default output device.

## Test

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

## Messages

MMDAgent-EX modules communicate via [messages](../messages). Below we explain this using speech synthesis as an example.

> You can actually view the messages by [outputting logs](../log/).

### SYNTH_START message

The speech synthesis module monitors MMDAgent-EX's message queue. When it detects a **SYNTH_START** message, it performs speech synthesis. You can trigger synthesis from an .fst file by issuing the following **SYNTH_START** message:

{{<message>}}
SYNTH_START|model alias|voice name|text
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

Provide text in UTF-8.

### SYNTH_EVENT_START, SYNTH_EVENT_STOP messages

The speech synthesis module emits messages for internal state changes such as start and end of processing. Specifically, it emits **SYNTH_EVENT_START** when audio output begins and **SYNTH_EVENT_STOP** when output finishes. By monitoring these you can trigger actions at voice start or wait until speech output is finished.

{{<message>}}
SYNTH_EVENT_START|model alias
SYNTH_EVENT_STOP|model alias
{{</message>}}

## Try it

[Use the browser interface](../message-test) to experiment with **SYNTH_START** messages.
With MMDAgent-EX running on the same machine, open the following page to connect to MMDAgent-EX and display a text box:

- <a href="http://localhost:50000" target="_blank">http://localhost:50000</a> (opens in a new window)

Paste the message below into the text box and press Send to confirm a cheerful voice is produced.

{{<message>}}
SYNTH_START|0|slt_voice_happy|"Nice to meet you!"
{{</message>}}

### Related files

The Open JTalk module is provided as `Plugin_Open_JTalk.dll` (or `.so`) under the `Plugins` directory in the executable folder. FLite+HTS_Engine is `Plugin_Flite_plus_hts_engine.dll` (or `.so`).

Voice models and configuration files are provided by the content. In the Example, voice models are in `voice/mei` and `voice/slt`, and configuration files are `main.ojt` and `main.fph`. Each configuration file defines the "voice name" used in messages.