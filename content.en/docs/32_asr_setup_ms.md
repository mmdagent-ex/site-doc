---
title: Set up for Voice Recognition (MS)
slug: asr-setup-ms
---
{{< hint ms >}}
Please use "R2-ASR" kit for moonshot version.  It is far more better engine than public version's Julius.

The content of this page is for MS version only.
{{< /hint >}}

# Voice Recognition Setup (MS Version)

MS向けに配布されている京大の実環境実時間音声認識キット R2-ASR を、MMDAgent-EX に組み込んで音声認識を行いましょう。

This page describes how to start using the "R2-ASR" speech recognition module provieded by Kyoto University for MS.

## Obtaining R2-ASR

The R2-ASR module tailored for use in MMDAgent-EX is available on the same place as the MS version of MMDAgent-EX.

## Quick Setup

After obtaining the repository, execute the following commands in the Anaconda shell to set up the environment. For detailed setup instructions, see the README of R2-ASR.

```shell
(If you don't have conda) Install miniconda
Execute the following in the Anaconda shell:
% cd r2-asr
% conda env create -f env_ms_asr.yml
% conda activate ms_asr

% (win32) where python
or
% (linux) which python
to get the execution path of Python
```

After the above, describe the following in the .mdf of the Example to start R2ASR as submodule in MMDAgent-EX. In the example below, replace `/some/where/python` with the execution path found above, and `/this/dir/ALL.py` with the path to `ALL.py` in R2ASR.

{{<mdf>}}
Plugin_AnyScript_Command=/some/where/python -u /this/dir/ALL.py --vad-conf conf.vad.yml --asr-conf conf.asr.yml --input mic
{{</mdf>}}

For other settings such as selecting a voice device, please see the README of R2-ASR.

## Execution Test

run the .mdf with MMDAgent-EX, then R2ASR will start with the content as a submodule, enabling voice recognition.

When voice input is detected and recognition begins, the following message is output.

{{< message >}}
RECOG_EVENT_START
{{< / message >}}

After recognition ends, the recognition result is output as the following message.

{{< message >}}
RECOG_EVENT_STOP|It is fine today
{{< / message >}}

## Messages R2ASR can receive

R2ASR can receive the following messages. By using these messages, you can control R2ASR to temporarily pause and resume its voice recognition.

### MSASR_DEACTIVATE

Pause voice recognition.

### MSASR_ACTIVATE

Resume voice recognition.

