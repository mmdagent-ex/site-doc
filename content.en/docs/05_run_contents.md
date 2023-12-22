---
title: Running Example
slug: run
---
# Running Example

MMDAgent-EX is a software that plays "content".  In this section we explains what the "content" is in MMDAgent-EX, and explain the procedure to launch the example content.

## About the Content

MMDAgent-EX plays back the content. Content refers to a collection of files (assets) that comprise an interactive system, such as 3D models, motions, FST scripts, and audio-visual materials.

The general structure of the content is as follows. In the top directory, there should be always an .mdf file, which serves as both the launch file and the configuration file. Additionally, files such as .fst, .dic, .jconf, .ojt are placed with the same prefix as .mdf. Also, `BUTTON*.txt`, `PACKAGE_DESC.txt` can be placed in the top directory. All other files (models, motions, images etc.) can be placed anywhere under the folder.

    topdir/
        |- foobar.mdf         Startup / Configuration
        |- foobar.fst         Dialogue Script
        |- foobar.dic         Additional dictionary for Julius
        |- foobar.jconf       Additional Julius jconf file
        |- foobar.ojt         Open JTalk setting file
        |- PACKAGE_DESC.txt   Package info for web-based deploy
        |- README.txt         Readme doc
        +- (SubDirectories)
            |- 3-D models (.pmd)
            |- Motions (.vmd)
            |- TTS Voice model (.htsvoice)
            |- Background/Floor (images)
            |- Sound / Music files (sound files)
            |- Images, Text files, etc.

## Obtaining the Example Content

The [example content](https://github.com/mmdagent-ex/example) is a repository that includes a minimal script, sample images and motions, the model "mei" for Open JTalk, and the CG models ["Gene"](https://github.com/mmdagent-ex/gene) and ["Uka"](https://github.com/mmdagent-ex/uka).  Get the example content to learn about MMDAgent-EX on this site.

    example/
        |- main.mdf         Startup / Configuration
        |- main.fst         Dialogue Script
        |- main.ojt         Open JTalk setting
        |- images/
        |    |- ...
        |- motions/
        |    |- ...
        |- voice/           Voice model "mei" for Open JTalk
        |    |- mei/
        |- gene/            CG-CA model "Gene"
        |    |- Gene.pmd
        |- uka/             CG-CA model "Uka"
        |    |- Uka.pmd
        |- example_motion/     Example files for motion blending
        +- example_websocket/  Example files for websocket connection

Clone the sample content. Do not forget to use `--recursive` option ad clone, as it loads the CG-CA models as submodules.

```shell
git clone --recursive https://github.com/mmdagent-ex/example
```

## Launching Content

To launch content, specify the .mdf file at the top of the content folder as a command line argument for MMDAgent-EX.

macOS / Linux terminal:

```shell
./Release/MMDAgent-EX ./example/main.mdf
```

Windows Command shell:

```text
.\Release\MMDAgent-EX.exe .\example\main.mdf
```

If you see a screen like the one below, the launch was successful.

<img width="480" alt="example snapshot" src="/images/example_1.png"/>

{{< hint info >}}
If you set this example as "home content", the content will be start up just by starting the executable.

To set the content being executed as home:

- Press the `/` key on the MMDAgent-EX screen → the menu opens
- Move to the right menu with →
- Select "Set current as Home" with the up and down keys and press enter

{{< /hint >}}

### If it fails in WSL

If the screen doesn't appear and the launch fails in WSL, your version of WSL may be outdated. Please use the latest WSL2, which supports GUI apps. For details, [please refer to this site to update your WSL version](https://learn.microsoft.com/windows/wsl/tutorials/gui-apps).
