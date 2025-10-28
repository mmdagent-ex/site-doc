---
title: Julius Speech Recognition Engine Settings
slug: asr-setting
---
# Julius Speech Recognition Engine Settings

Plugin_Julius is a plugin that provides speech recognition using the Julius engine. It is characterized by compact operation. Below are explanations of the settings, messages, and usage for this plugin.

## .mdf settings

**Plugin_Julius_conf**, **Plugin_Julius_lang** (required)

Names of the recognition engine configuration and the language.

No defaults are provided. Prepare models and enable Plugin_Julius by specifying a valid combination of these in the .mdf.

Combinations supported by the default models:

- dnn, ja
- dnn, en
- gmm, ja

{{<mdf>}}
Plugin_Julius_conf=dnn
Plugin_Julius_lang=en
{{</mdf>}}

**Plugin_Julius_wordspacing**

Specifies whether to separate words in recognition output.

- `no`: join words without any separator (default for `ja`)
- `yes`: insert spaces between words (default for non-`ja`)
- `comma`: insert commas between words (compatible with old MMDAgent)

{{<mdf>}}
Plugin_Julius_wordspacing=yes
{{</mdf>}}

**Plugin_Julius_logfile**

Output Julius engine internal logs to a file.

{{<mdf>}}
Plugin_Julius_logfile=log.txt
{{</mdf>}}

**show_caption**

Display captions. Recognition results appear on the left side of the screen, and synthesized speech (the text provided by **SYNTH_START**) appears on the right.

{{<mdf>}}
show_caption=true
{{</mdf>}}

## Event messages

**RECOG_EVENT_START**

Emitted when voice input is detected.

{{<message>}}
RECOG_EVENT_START
{{</message>}}

**RECOG_EVENT_STOP**

Emitted when a recognition result is obtained.

{{<message>}}
RECOG_EVENT_STOP|Recognition result sentence
{{</message>}}

**RECOG_EVENT_OVERFLOW**

Emitted when the input level is too high and causes overflow.

{{<message>}}
RECOG_EVENT_OVERFLOW
{{</message>}}

**RECOG_EVENT_MODIFY**

Emitted when processing of a RECOG_MODIFY message is completed.

{{<message>}}
RECOG_EVENT_MODIFY|GAIN
RECOG_EVENT_MODIFY|USERDICT_SET
RECOG_EVENT_MODIFY|USERDICT_UNSET
RECOG_EVENT_MODIFY|CHANGE_CONF|(jconf_file_prefix)
{{</message>}}

**RECOG_EVENT_AWAY**

Emitted when speech recognition is temporarily paused (ON) or resumed (OFF) by menu operations or external control.

{{<message>}}
RECOG_EVENT_AWAY|ON
RECOG_EVENT_AWAY|OFF
{{</message>}}

**RECOG_EVENT_GMM**

Output tag for environment-sound classification when using Julius's environmental sound detection.

{{<message>}}
RECOG_EVENT_GMM|noise
{{</message>}}

## Command messages

**RECOG_MODIFY**

Command to change engine settings. Dynamically modifies the running engine.

- `GAIN`: input amplitude scaling factor (default 1.0)
- `USERDICT_SET`: load a user dictionary (replaces one already loaded)
- `USERDICT_UNSET`: remove the user dictionary
- `CHANGE_CONF`: restart the engine with the specified jconf configuration file

{{<message>}}
RECOG_EVENT_MODIFY|GAIN|(scale)
RECOG_EVENT_MODIFY|USERDICT_SET|(dict_file_path)
RECOG_EVENT_MODIFY|USERDICT_UNSET
RECOG_EVENT_MODIFY|CHANGE_CONF|(jconf_file_prefix)
{{</message>}}

**RECOG_RECORD_START**

Start automatic recording of input audio. Segmented audio fragments are sequentially saved as individual .wav files in the specified directory.

{{<message>}}
RECOG_RECORD_START|(directory)
{{</message>}}

**RECOG_RECORD_STOP**

Stop automatic recording of input audio.

{{<message>}}
RECOG_RECORD_STOP
{{</message>}}

## Audio input state synchronization

While running, across all display models the following morph values are continuously updated to reflect the audio input state (no change if the morph does not exist).

- Morph "`volume`": audio input volume value (0.0–1.0)
- Morph "`trigger`": 1.0 when the audio input is speech, 0.0 when non-speech

Using these, you can implement interactive behaviors such as changing morphs in response to input volume or toggling displays according to speech input ON/OFF.

Also, the audio input volume is set to the KeyValue value "`Julius_MaxVol`" as needed.

## Customization

### Content dictionary (.dic)

You can expand the vocabulary by preparing a dictionary that defines unknown words. A content-specific dictionary should be placed in the content directory with the same filename as the .mdf but with the extension changed to .dic (for example, if the .mdf is `foobar.mdf`, name it `foobar.dic`). Plugin_Julius searches for this .dic at startup and, if found, loads it as an additional user dictionary.

### Per-content configuration (.jconf)

Plugin_Julius also looks for files like `foobar.jconf` and, if present, loads them as additional configuration files. This allows you to provide different Julius parameters or settings per content.

### Further extensions such as adding models

The upstream Julius is fully integrated, allowing full customization. You can use all features, models, and settings supported by Julius. For example, by preparing a Julius language model and acoustic model for another language, you can add support for that language.

When using customized models or dictionaries, place the corresponding Julius configuration file under Release/AppData/Julius with the filename `jconf_configurationname_languagename.txt`.txt`. By specifying those configuration name and language in the .mdf, Plugin_Julius will start using that configuration file.

## Using other engines

Julius is a compact open-source speech recognition engine, but it was developed some time ago; model performance and noise robustness—especially recognition accuracy in noisy environments—may be inferior to modern speech recognition engines.

If you build a system using cloud speech recognition engines like Google STT or Whisper in Python, you can integrate them with MMDAgent-EX in two ways:

- Run them as a submodule of MMDAgent-EX using Plugin_AnyScript
- Connect an external process to MMDAgent-EX via the WebSocket feature

Refer to the respective documentation for details.