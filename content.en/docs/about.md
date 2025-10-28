---
title: About MMDAgent-EX
slug: about
---
# What is MMDAgent-EX

MMDAgent-EX is a research and development platform for CG avatar based voice interaction, multimodal dialogue, and avatar communication.  It combines CG character rendering and control with speech and language processing to provide a standalone system for building custom voice dialogue systems. By adding various modules, you can build diverse multimodal dialogue systems that integrate cameras, networks, and other inputs. It also supports sending motion commands and audio data over the network from external sources, enabling lip-synced audio playback and motion playback/control, so it can serve as a frontend for many existing dialogue systems.

[MMDAgent](https://www.mmdagent.jp/) was originally developed at Nagoya Institute of Technology in 2011 as an open-source toolkit for research and development in voice interaction. Since then, the project has grown with extensions for additional formats, network support, improved UIs, and external control features. Since December 2020, research and development has continued under the [Moonshot-type R&D Program "Avatar Symbiotic Society"](https://avatar-ss.org/) to advance CG avatar communication—conversing via CG characters. This site publishes part of those research outcomes as open source.

## Features

MMDAgent-EX includes a custom OpenGL-based renderer compatible with [MMD (MikuMikuDance)](https://sites.google.com/view/vpvp/), allowing dialogue characters to be built using MMD-format 3D models and motions. It bundles speech recognition and synthesis engines developed at Nagoya Institute of Technology such as [Julius](https://github.com/julius-speech/julius) and [Open JTalk](https://open-jtalk.sp.nitech.ac.jp/), and it has a primitive FST-based state-transition dialogue scripting feature, enabling a complete voice dialogue system out of the box. It also supports connecting to scripting languages like Python, so you can add cloud speech recognition/synthesis engines or LLMs such as ChatGPT as modules. Socket-based external control is supported as well, allowing it to act as an I/O frontend for existing dialogue response generation systems.

- All-in-one platform for voice interaction and voice dialogue systems (Windows, macOS, Linux)
- Lightweight, high-efficiency built-in CG avatar rendering engine: full support for MMD (MikuMikuDance) file formats
- Built-in low-latency speech recognition (Julius) and speech synthesis (Open JTalk) that run fast on CPU only; components are freely replaceable
- Easy development and extensibility: straightforward integration with cloud engines, LLMs, and arbitrary applications or scripts
- Comprehensive consolidated documentation (this site)

## Differences between MMDAgent and MMDAgent-EX

See the differences from the original MMDAgent [here](../changes-since-original-mmdagent/).

## Name / Pronunciation

Both "MMDAgent-EX" and "MMD-Agent EX" are acceptable. The "MMD" part is a double meaning: "Multi-Modal Dialogue" and "MikuMikuDance." We refer to the project as "MMDAgent EX."

## Citations

Please use the following.

**APA**

    Lee, A. (2023). MMDAgent-EX (Version 1.0.0) [Computer software].
    https://doi.org/10.5281/zenodo.10427369

**BibTeX**

    @software{Lee_MMDAgent-EX_2023,
        author = {Lee, Akinobu},
        doi = {10.5281/zenodo.10427369},
        license = {Apache-2.0},
        month = dec,
        title = {{MMDAgent-EX}},
        url = {https://github.com/mmdagent-ex/MMDAgent-EX},
        version = {1.0.0},
        year = {2023}
    }

## Acknowledgments

MMDAgent-EX:

- Akinobu Lee (Nagoya Institute of Technology, Japan)

MMDAgent:

- Keiichi Tokuda (Nagoya Institute of Technology, Japan)
- Akinobu Lee (Nagoya Institute of Technology, Japan)
- Keiichiro Oura (Nagoya Institute of Technology, Japan)
- Daisuke Yamamoto (Nagoya Institute of Technology, Japan)