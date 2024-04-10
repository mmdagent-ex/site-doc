

---
title: Sound Playback
slug: sound
---
{{< hint info >}}
Audio file playback is provided by Plugin_Audio, and voice lip sync playback is provided by Plugin_Remote. Please ensure these plugins are enabled when using them.
{{< /hint >}}

# Sound Playback

Effective use of music and sound effects can create richer interactions. MMDAgent-EX has the ability to play audio files, allowing you to play music in the background or play sound effects in response to events.

Additionally, MMDAgent-EX also offers the feature to play recorded (or synthesized) voice data while lip-syncing it to a character. This can be used for purposes such as responding with pre-recorded audio or making characters speak with voice files outputted by other voice synthesis engines.

The following will explain how to play sound files and how to play voice files with lip-sync.

## Preparation

MMDAgent-EX plays sound from the "default audio output device". Please set the sound device you want to play sound from as the default output device in advance.

For macOS and Linux, please install [sox](https://sourceforge.net/projects/sox/) in advance.

**macOS**:

```shell
brew install sox
```

**Linux**:

```shell
sudo apt install sox
```


## Sound Playback

Audio files such as .wav, .mp3 can be played using the **SOUND_START** message.

{{< details "About Supported Formats" close >}}
**Windows**: Supports .wav and .mp3 by default. To play other audio file formats, you need to install the appropriate codecs or drivers.

**macOS, Linux**: Uses the play command of [sox](https://sourceforge.net/projects/sox/) for playback, and supports most audio file formats including .wav and .mp3.
{{< /details >}}

When playback starts, a **SOUND_EVENT_START** is outputted.

{{<message>}}
SOUND_START|(sound alias)|(sound file name)
SOUND_EVENT_START|(sound alias)
{{</message>}}

To stop the sound during playback, use the **SOUND_STOP** message.

{{<message>}}
SOUND_STOP|(sound alias)
{{</message>}}

When audio playback ends (or is interrupted), a **SOUND_EVENT_STOP** is outputted.

{{<message>}}
SOUND_EVENT_STOP|(sound alias)
{{</message>}}

{{< hint warning >}}
If the sound does not play, please check your default audio output device. Also, the `play` command of sox is used for playback, but [you can specify a different command with environment variables](../envval/#audio_start-playback-command-play).
{{< /hint >}}

## Voice Playback with Lip Sync

### Preparation

Lip sync is expressed by mapping phoneme information extracted from audio files to the blends of mouth shapes "a", "i", "u", "o". Therefore, you need to describe in advance in a .shapemap file which morph on the model corresponds to "a", "i", "u", "o". This is already set in the distributed version of Gene Uka, but if you use other models, you'll need to create it yourself.

When creating, make and save a text file named `xxx.pmd.shapemap` in the same folder where the model file `xxx.pmd` is stored. Write the corresponding morph names in `LIP_A` to `LIP_O`. Specify all other mouth-opening morphs in `NOLIP` separated by commas. The character encoding must be UTF-8.

```text
#### Morph names for lip sync
LIP_A a
LIP_I i
LIP_U u
LIP_O o
#### List of morph names to reset to 0 during lip sync
#### Specify all mouth-opening morphs not specified above
NOLIP e, oo~, Wa, eh, ah, ii, shout, ah-le, mouth smile
```

### Execution

After launching, it plays the audio file with lip-sync using the **SPEAK_START** message. `(model alias)` specifies the alias of the model performing the lip-sync, and `(audio file)` is the audio file to be played. At the start of playback, a **SPEAK_EVENT_START** message is output.

{{<message>}}
SPEAK_START|(model alias)|(audio file)
SPEAK_EVENT_START|(model alias)
{{</message>}}

The audio file can use formats supported by [libsndfile](https://libsndfile.github.io/libsndfile/formats.html), such as .wav, .mp3, etc.

At the end of playback, a **SPEAK_EVENT_STOP** message is output.

{{<message>}}
SPEAK_EVENT_STOP|(model alias)
{{</message>}}

**SPEAK_STOP** is a message that stops currently playing audio started by **SPEAK_START**.  It issues **SPEAK_EVENT_STOP** after confirmed that speaking audio has been stopped.

{{<message>}}
SPEAK_STOP|(model alias)
{{</message>}}

### Play quality changes and gap issues (v1.0.4)

The audio output of **SPEAK_START** has been in 16kHz mono in the version before v1.0.3.  From v1.0.4, it has been improved so that voice file will be played as is with no conversion.

However, since it now uses Plugin_Audio features to play audio, the lip-sync process and audio-playing process are separated so a gap may arise for the start timing of lip sync and audio.

If you want **SPEAK_START** command to behave like older versions, set the following in .mdf file.  This will force MMDAgent-EX to use the old 16kHz playing.

{{<mdf>}}
Plugin_Remote_Speak_16k=true
{{</mdf>}}