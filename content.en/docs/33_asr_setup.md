---
title: Set up for Voice Recognition
slug: asr-setup
---

# Setting Up Voice Recognition

MMDAgent-EX comes with [Julius](https://julius.osdn.jp/) as the default voice recognition engine. 
Julius is a fast and convenient voice recognition engine that runs only on the CPU of your local machine.

{{< hint warning >}}
To use speech recognition, do the set up below for each content.
{{< /hint >}}

## Download the Model

Voice recognition models for Japanese and English are provided. Please download them separately from the link below. The download size is about 791 MB, and it will consume 1.7GB of disk space after decompressing.

{{< button href="https://drive.google.com/file/d/1d82CpinrlDmY9MgjTYa-awCdLOsz16MF/view?usp=sharing" >}}Download Recent: Julius_Models_20231015.zip{{< /button >}}

{{< details "Older Versions" close >}}
- [Julius_Models_20231015.zip](https://drive.google.com/file/d/1d82CpinrlDmY9MgjTYa-awCdLOsz16MF/view?usp=sharing) - 2023.10.15
{{< /details >}}

After decompressing the file, move the whole fiels under the `Release/AppData/Julius` folder, to look as follows.

    Release/
    └── AppData/
        └── Julius/
            ├── phoneseq/
            ├── jconf_phone.txt
            ├── jconf_gmm_ja.txt
            ├── jconf_dnn_ja.txt
            ├── jconf_dnn_en.txt
            ├── dictation_kit_ja/
            └── ENVR-v5.4.Dnn.Bin/

## Setup

You should explicitly specify the model and language settings in .mdf file.  To test English speech recognition, open the main.mdf file in the Example with a text editor and add the following two lines at the end.

{{< mdf >}}
Plugin_Julius_lang=en
Plugin_Julius_conf=dnn
{{< / mdf >}}

- The first one is to specify the language name: Specify either `en` (English) or `ja` (Japanese).
- The second one is to specify the setting name: In `en`, only `dnn` can be specified.  In `ja`, you can specify either `dnn` or `dmm`.

## Preparing Audio Input Device

The speech recognition module opens the default audio input device. Prepare a voice input device and set it as the default voice input device.

{{< hint warning >}}
If there is no voice input device, it will result in an error and will not start.
{{< /hint >}}

## Run Test

Launch the example content with the .mdf file set up as above.

When launch was successfull, you will see a circular meter like the one below appears in the lower left corner of the screen after some time. The varying size of the circle represents the input volume.

![audiometer](/images/julius_indicator_1.png)

Try speaking English into the audio input device. When voice recognition starts, the circular meter will look like this:

![audiometer2](/images/julius_indicator_2.png)

By default, subtitles are ON, so the recognition results will be displayed on the screen.

## How it works

When recognition starts, the following event message is sent:

{{< message >}}
RECOG_EVENT_START
{{< / message >}}

When recognition ends, the voice recognition result is output with the following event message:

{{< message >}}
RECOG_EVENT_STOP|The weather is nice today
{{< / message >}}

If you want to output the results separated by each word, you can specify it in the .mdf file as follows:

{{< mdf>}}
Plugin_Julius_wordspacing=yes
{{< / mdf >}}

- `no`: nothing between words (default for `ja`)
- `yes`: Insert a space between words (default for languages other than `ja`)
- `comma`: Insert a comma between words (compatible with old MMDAgent)

## When You Want to Use Another Engine

Julius is a compact open-source voice recognition engine, but it was made with technology from a generation ago, and its model performance and noise resistance, especially recognition accuracy under noisy conditions, are inferior to the latest voice recognition engines.

If you create a system with Python using a cloud voice recognition engine like Google STT or Whisper, you can link it in two ways:

- Run as a submodule of MMDAgent-EX with Plugin_AnyScript
- Link with an external process of MMDAgent-EX using the WebSocket feature.
