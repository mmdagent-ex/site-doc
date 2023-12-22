---
title: Trying Out Different CG Avatars
slug: change-model
---

# About CG Avatars

## Gene

The default CG avatar in Example is called "Gene". This is a CG character model designed for spoken dialogue system, developed at [Lee-Lab, NITech](https://www.slp.nitech.ac.jp/avatar/).  It is provided under the CC-BY license.  For more details and usage conditions, please refer to its [public repository](https://github.com/mmdagent-ex/gene). 
 
<img width="480" alt="example snapshot" src="/images/example_1.png"/>

## Uka

Another CG avatar called "Uka" is also included in the Example folder.  You can use "Uka" instead of Gene by editing the line below in `main.fst`.

{{<fst>}}
    ...
    <eps> MODEL_ADD|0|uka/MS_Uka.pmd
    ...
{{</fst>}}

```shell
./Release/MMDAgent-EX.exe ./example/main.mdf
```

<img alt="example snapshot of uka" src="/images/Uka.png"/>

MMDAgent-EX supports [MikuMikuDance format 3D model](../3d-model/).  Aside from the default avatars, you can use any 
character on this system.  For more detailed methods, please refer to the [Displaying 3D Models](../3d-model) page.
