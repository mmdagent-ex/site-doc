---
title: Speech Recognition Setup
slug: asr-setup
---
# Speech Recognition Setup

MMDAgent-EX includes [Julius](https://julius.osdn.jp/) as the default speech recognition engine.
Julius is a lightweight, fast speech recognition engine that runs locally on CPU only.

{{< hint warning >}}
Using speech recognition requires the following preparation and configuration. It will not work right after building. Be sure to perform the setup below for each content package.
{{< /hint >}}

## Downloading Models

Speech recognition models are provided for Japanese and English. They are not bundled in the repository, so download them separately from the link below. The download size is about 791 MB, and it uses about 1.7 GB of disk space when unpacked.

{{< button href="https://drive.google.com/file/d/1d82CpinrlDmY9MgjTYa-awCdLOsz16MF/view?usp=sharing" >}}Download Recent: Julius_Models_20231015.zip{{< /button >}}

{{< details "List of older versions" close >}}
- [Julius_Models_20231015.zip](https://drive.google.com/file/d/1d82CpinrlDmY9MgjTYa-awCdLOsz16MF/view?usp=sharing) - 2023.10.15
{{< /details >}}

Unpack the archive and place the contents in the Release/AppData/Julius folder. For example:

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

You need to specify the models and language used by Julius in the .mdf file. To use English speech recognition, open the main.mdf file in the Example folder with a text editor and add the following two lines at the end:

{{< mdf >}}
Plugin_Julius_lang=en
Plugin_Julius_conf=dnn
{{< / mdf >}}

- The first line specifies the language: choose `ja` (Japanese) or `en` (English).
- The second line specifies the configuration: for `ja` you can choose `dnn` or `dmm`; for `en` only `dnn` is available.

## Preparing an Audio Input Device

The speech recognition module opens the system default sound input device to perform recognition. Prepare an audio input device and set it as the default input device.

{{< hint warning >}}
If no audio input device is available, an error will occur and the application will not start.
{{< /hint >}}

## Test Run

Start the Example content with the .mdf file configured as above.

After starting, if a circular meter like the one below appears in the lower-left corner of the screen, the engine has started successfully.
The circle size represents the input volume.

![audio meter](/images/julius_indicator_1.png)

Speak toward the audio input device. When recognition starts, the circular meter will look like this:

![audio meter active](/images/julius_indicator_2.png)

Recognition results are shown as captions on the screen.

![result](/images/asr_test_en.png)

## How it Works

The speech recognition module sends its internal activity as messages. When recognition starts, the module outputs the following message:

> You can view these messages by [enabling log output](../log/).

{{< message >}}
RECOG_EVENT_START
{{< / message >}}

Recognition results are output as a message when recognition stops, for example:

{{< message >}}
RECOG_EVENT_STOP|The weather is nice today
{{< / message >}}

If you want the result to be separated by words, you can specify the following in the .mdf:

{{< mdf>}}
Plugin_Julius_wordspacing=yes
{{< / mdf >}}

- `no`: Concatenate words without separators (default for `ja`).
- `yes`: Insert spaces between words (default for non-`ja`).
- `comma`: Insert commas between words (compatible with older MMDAgent).

You can turn off caption display. To disable captions, add the following line to main.mdf:

{{<mdf>}}
show_caption=false
{{</mdf>}}

## Using Other Engines

Julius is a compact open-source speech recognition engine, but it was developed with older techniques; model quality and noise robustness -- especially in noisy environments -- can be inferior to modern speech recognition engines.

If you build a system using cloud STT engines like Google STT or local models like Whisper via Python, you can integrate them with MMDAgent-EX in two ways:

- Run them as a submodule of MMDAgent-EX using Plugin_AnyScript
- Integrate with a separate MMDAgent-EX process via the WebSocket feature