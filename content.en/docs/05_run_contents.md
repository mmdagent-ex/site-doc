---
title: Running the Example
slug: run
---
# Running the Example

MMDAgent-EX launches by specifying a content package. Below is an overview of content in MMDAgent-EX and the steps to run the Example content.

## About Content

MMDAgent-EX plays content. Content refers to a collection of files (assets) that make up the dialogue system, such as 3D models, motions, FST scripts, audio, and images.

A typical content structure looks like this. The top directory always contains exactly one .mdf file, which serves as the startup/configuration file. Depending on the modules used, files like .fst, .dic, .jconf, and .ojt are placed with the same prefix as the .mdf. Also put BUTTON*.txt and PACKAGE_DESC.txt in the top directory. Other files (models, motions, images, etc.) can be placed anywhere under subdirectories.

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

The [sample content](https://github.com/mmdagent-ex/example) repository contains minimal scripts, sample images and motions, the Open JTalk voice model "mei", and the CG models "Gene" and "Uka". This site's explanations use this sample content, so please obtain it.

    example/
        |- main.mdf         Startup / Configuration
        |- main.fst         Dialogue Script
        |- main.ojt         Open JTalk setting
        |- main.fph         FLite+HTS_Engine setting
        |- gene/            CG-CA model "Gene" (git submodule)
        |    |- Gene.pmd
        |- uka/             CG-CA model "Uka"  (git submodule)
        |    |- Uka.pmd
        |- motions/
        |    |- ...
        |- voice/           Voice model "mei" for Open JTalk
        |    |- mei/
        |- images/
        |    |- ...
        |- glasses/
        |    |- ...
        |- stage/
        |    |- ...
        |- demo/            Demonstration
        |    |- Gene_en
        |    |- Gene_jp
        |    |- Uka_en
        |    +- Uka_jp
        |- example_motion/     Example files for motion blending
        +- example_websocket/  Example files for websocket connection

Clone the sample content. The CG-CA repositories are cloned inside using submodules, so include --recursive.

```shell
cd MMDAgent-EX
git clone --recursive https://github.com/mmdagent-ex/example
```

## Launching Content

Start MMDAgent-EX with the .mdf file at the top of the content folder as a command-line argument.

Terminal (macOS / Linux):

```shell
./Release/MMDAgent-EX ./example/main.mdf
```

Windows Command Prompt:

```text
.\Release\MMDAgent-EX.exe .\example\main.mdf
```

If you see a screen like the following, startup succeeded.

<img width="480" alt="example snapshot" src="/images/example_1.png"/>

{{< hint info >}}
If you set this Example as Home, from next time the Example can be started using only the executable binary.

To set the running content as Home:

- Press `/` in the MMDAgent-EX window -> menu opens
- Press right arrow to move to the right menu
- Use the Up/Down keys to select "Set current as Home" and press Enter
{{< /hint >}}

### If it fails on WSL

If the window does not appear and startup fails under WSL, your WSL version may be old. Use the latest WSL2 that supports GUI apps. For details, refer to this site to update WSL to the latest version: https://learn.microsoft.com/windows/wsl/tutorials/gui-apps