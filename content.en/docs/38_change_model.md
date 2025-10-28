---
title: Change the CG Avatar
slug: change-model
---
# About CG Avatars

## Gene

The avatar shown by default in Example is a CG avatar called "Gene". This is a conversational CG model developed at Nagoya Institute of Technology and provided under a CC-BY license as a CG-CA (CG Cybernetic Agent) developed in the Moonshot Research and Development program "Avatar Symbiotic Society". For terms of use and more details, see the public repository: https://github.com/mmdagent-ex/gene.

<img width="480" alt="example snapshot" src="/images/example_1.png"/>

## Uka

Example also ships with another CG avatar named "Uka". In example's main.fst, change the part that specifies the model file `Gene.pmd` to the following and restart to confirm the model has changed:

{{<fst>}}
    ...
    <eps> MODEL_ADD|0|uka/MS_Uka.pmd
    ...
{{</fst>}}

```shell
./Release/MMDAgent-EX.exe ./example/main.mdf
```

<img alt="example snapshot of uka" src="/images/Uka.png"/>

MMDAgent-EX supports MikuMikuDance-format 3D models and can load models in that format. For details, see the [Displaying 3D Models page](../3d-model).