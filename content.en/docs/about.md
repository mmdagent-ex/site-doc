---
title: About MMDAgent-EX
slug: about
---
# About MMDAgent-EX

MMDAgent-EX is an open-source platform for voice dialogue systems and avatar communication. It is a standalone system that combines the display and control of CG characters with speech and language processing, allowing you to create various voice dialogue systems. By adding various modules, you can build diverse multimodal dialogue systems. Additionally, it supports features such as lip-synced speech playback and motion playback/control from external software, making it possible to operate as a human-agent frontend for a dialogue system.

[MMDAgent](https://www.mmdagent.jp/) was developed at Nagoya Institute of Technology since 2011 as an open-source toolkit for research and development in voice interaction.  Besides the its original version, it has been internally developed continuously for research purposes: support various formats, network capabilities, UI improvements, external control functions, and more.  Since December 2020, its research and development have been progressing in the ["Avatar Symbiosis Society" JST moonshot program](https://avatar-ss.org/en/index.html), as the platform for CG avatar communication. Here, we release some of the research and development results as open source.

## Features

MMDAgent-EX has its own OpenGL-based rendering engine compatible with [MMD (MikuMikuDance)](https://en.wikipedia.org/wiki/MikuMikuDance), and can create interactive characters using 3D models and motion data in MMD format. It also includes speech recognition and synthesis engines developed at Nagoya Institute of Technology, such as [Julius](https://github.com/julius-speech/julius) and [Open JTalk](https://open-jtalk.sp.nitech.ac.jp), as well as an embedded FST-based state-transition primitive dialogue scripting feature, allowing you to build voice dialogue systems independently. Aside from the internal engines, it can be easily connected to other scripts like Python, so you can add another modules such as cloud-based speech recognition, speech synthesis engines, or large language models like ChatGPT with this system. Furthermore, it supports external control via socket connections, making it suitable for use as the input/output frontend for existing dialogue systems.

- All-in-one platform for creating voice interaction systems on Windows, macOS and Linux
- Light-weight fine-grained CG avatar rendering engine, fully compatible with MMD (MikuMikuDance) format
- Low-latency ASR / TTS modules, running blazingly fast on CPU.
- Can add any modules and processes easily, such as cloud engines, LLMs, etc.
- Fully documented on this site.
- Runs on Windows, macOS and Linux.

## What differs from the original MMDAgent?

See [this page](../changes-since-original-mmdagent/).

## How do I represent or pronounce it?

The notation can be either **MMDAgent-EX** or **MMD-Agent EX**. The "MMD" part has a double meaning, representing both "Multi-Modal Dialogue" and "MikuMikuDance". We call it “Em-Em-Dee-Agent E-X”.

## Citation

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
