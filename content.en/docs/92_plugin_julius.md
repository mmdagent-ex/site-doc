

---
title: Setting up the Julius Voice Recognition Engine
slug: asr-setting
---

# Setting up the Julius Voice Recognition Engine

Plugin_Julius is a plugin that provides voice recognition functionality using the Julius voice recognition engine. It is characterized by its compact operation. Below, we explain the settings, messages, and how to use this plugin.

## .mdf Configuration

**Plugin_Julius_conf**, **Plugin_Julius_lang** (Required)

The configuration name and language name of the voice recognition engine.

No default designation. By preparing a model and specifying these valid combinations in .mdf, Plugin_Julius is activated.

Combinations supported by the default model:

- dnn, ja
- dnn, en
- gmm, ja

{{<mdf>}}
Plugin_Julius_conf=dnn
Plugin_Julius_lang=en
{{</mdf>}}

**Plugin_Julius_wordspacing**

Specify whether to separate words in the recognition result output.

- `no`: Pack without putting anything between words (default for `ja`)
- `yes`: Insert a space between words (default for languages other than `ja`)
- `comma`: Insert a comma between words (compatible with old MMDAgent)

{{<mdf>}}
Plugin_Julius_wordspacing=yes
{{</mdf>}}

**Plugin_Julius_logfile**

Outputs the internal log of the Julius engine to a file.

{{<mdf>}}
Plugin_Julius_logfile=log.txt
{{</mdf>}}

**show_caption**

Displays subtitles. The voice recognition results are displayed on the left side of the screen and the voice synthesis content (the sentence given with **SYNTH_START**) is displayed on the right side. Set to false to disable it.

{{<mdf>}}
show_caption=true
{{</mdf>}}

## Event Messages

**RECOG_EVENT_START**

Output when voice input is detected.

{{<message>}}
RECOG_EVENT_START
{{</message>}}

**RECOG_EVENT_STOP**

Output when recognition results are obtained.

{{<message>}}
RECOG_EVENT_STOP|Recognition result sentence
{{</message>}}

**RECOG_EVENT_OVERFLOW**

Output when the input sound level is too high and causes an overflow.

{{<message>}}
RECOG_EVENT_OVERFLOW
{{</message>}}

**RECOG_EVENT_MODIFY**

Output when the processing of the RECOG_MODIFY message is complete.

{{<message>}}
RECOG_EVENT_MODIFY|GAIN
RECOG_EVENT_MODIFY|USERDICT_SET
RECOG_EVENT_MODIFY|USERDICT_UNSET
RECOG_EVENT_MODIFY|CHANGE_CONF|(jconf_file_prefix)
{{</message>}}

**RECOG_EVENT_AWAY**

Output when voice recognition is temporarily suspended (ON) or restarted (OFF) due to menu operations or external control.

{{<message>}}
RECOG_EVENT_AWAY|ON
RECOG_EVENT_AWAY|OFF
{{</message>}}

**RECOG_EVENT_GMM**

Output of identification result tag when using Julius's environmental sound identification function.

{{<message>}}
RECOG_EVENT_GMM|noise
{{</message>}}

## Command Messages

**RECOG_MODIFY**

This is a command to modify engine settings. It dynamically changes the engine that is running.

- `GAIN`: Amplitude scaling factor of the input voice (default 1.0)
- `USERDICT_SET`: Load user dictionary (if it's already loaded, it will be replaced)
- `USERDICT_UNSET`: Delete user dictionary
- `CHANGE_CONF`: Restart the engine with the specified jconf configuration file

{{<message>}}
RECOG_EVENT_MODIFY|GAIN|(scale)
RECOG_EVENT_MODIFY|USERDICT_SET|(dict_file_path)
RECOG_EVENT_MODIFY|USERDICT_UNSET
RECOG_EVENT_MODIFY|CHANGE_CONF|(jconf_file_prefix)
{{</message>}}

**RECOG_RECORD_START**

Starts automatic recording of the input voice. The cut-out voice fragments are sequentially saved as individual .wav files in the specified directory.

{{<message>}}
RECOG_RECORD_START|(directory)
{{</message>}}

**RECOG_RECORD_STOP**

Stops automatic recording of the input voice.

{{<message>}}
RECOG_RECORD_STOP
{{</message>}}

## Synchronization of Audio Input Status

During operation, in all display models, the morph values with the following names are automatically updated according to the state of the audio input (no change if there is no morph).

- Morph "`volume`": Volume value of audio input (0.0~1.0)
- Morph "`trigger`": 1.0 when the audio input is voice, 0.0 when it's not

By using this, you can, for example, change the morph in sync with the input volume or switch the display according to the voice input ON/OFF, implementing interactivity.

In addition, the volume of the audio input is also set to the KeyValue value "`Julius_MaxVol`" at any time.

## Customization

### Content Dictionary (.dic)

You can expand your vocabulary by preparing a dictionary that defines unknown words. A dictionary for each content is placed within the content under a file name with the extension of the .mdf file changed to .dic (if it is `foobar.mdf`, it would be `foobar.dic`). Plugin_Julius will search for the above .dic file at startup and, if found, will read it in as an additional user dictionary.

### Per Content Settings (.jconf)

Similarly, if there is a file like `foobar.jconf`, Plugin_Julius will read it in as an additional configuration file. By using this, it is also possible to provide different Julius parameters and settings for each content.

### Further Expansion such as Adding Models

The latest original version of Julius is fully incorporated, allowing for complete customization. You can use all the features, models, and settings that are available with Julius. For example, by preparing a language model and an acoustic model for Julius in a certain language, you can add support for other languages.

When using customized models or dictionaries, please place the Julius configuration file in `Release/AppData/Julius`, with a filename of `jconf_configurationname_languagename.txt`. By specifying these configuration names and language names in .mdf, Plugin_Julius will launch with that configuration file.

## When you want to use other engines

Julius is a compact open-source speech recognition engine, but it was created with technology from a bygone era, so its model performance, noise resistance, and recognition accuracy, especially in noisy environments, are inferior to the latest speech recognition engines.

If you create a system in Python using a cloud speech recognition engine like Google STT or Whisper,

- Operate as a submodule of MMDAgent-EX with Plugin_AnyScript
- Collaborate with the separate process of MMDAgent-EX through the WebSocket feature

You can collaborate in these two ways. Please refer to the relevant documentation for each.