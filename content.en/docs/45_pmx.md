---
title: PMX Models
slug: pmx
---
# PMX Models

MMDAgent-EX can temporarily display 3D models in the PMX format. However, it cannot load .pmx files directly -- you must first convert them to another format (.pmd and .csv).

## Conversion steps

PMX models can be temporarily displayed in MMDAgent-EX by converting them to .pmd and .csv using [PMXEditor](https://kkhk22.seesaa.net/category/14045227-1.html) (by KyokuhokuP). The steps are as follows.

{{< hint info >}}
Please use the latest version if possible (tested version: 0.2.7.3)
{{< /hint >}}

- [Get PMXEditor](https://kkhk22.seesaa.net/category/14045227-1.html) and install it
- Open the target PMX file in PMXEditor
- From the menu "File - Export", save with the `.pmd` extension
- From the menu "File - Convert to Text(CSV) - Export to CSV file, save with the `.pmd.csv` extension

Place the .pmd and .csv files converted by the above steps in the same location as the original pmx. In particular, the filenames must be as follows -- pay attention to the .csv filename:

```text
  model.pmx
  model.pmd
  model.pmd.csv
```

## Usage

When using with MMDAgent-EX, specify the converted .pmd file with the `MODEL_ADD` command. The .csv file will be loaded automatically, enabling rendering close to the original PMX.

## Compatibility

The table below lists PMD and PMX features supported by MMDAgent-EX. Note that even if items are marked with "o", it does not guarantee them to work in all cases; some models may not function correctly.

|Feature|PMD|PMX|
|----|---|---|
|Physics|o|o|
|IK ON/OFF|o|o|
|Hidden morphs|o|o|
|Material info|o|o|
|Edge scale|-|o|
|BDEF4|-|o|
|SDEF|-|o(tentative)|
|Transform hierarchy|-|o|
|Post-physics deformation|-|o|
|Bone update order|-|o|
|Vertex morphs|-|o|
|Bone morphs|-|o|
|UV morphs|-|o|
|Material morphs|-|o (texture coefficients only)|
|Group morphs|-|o|
|Additional UV|-|-|
|External parent transform|-|-|

## Notes on use

Please comply with this software's ELSI guidelines and follow applicable terms of use and community practices when using models.

Note: When a PMX model is in use, the system will always display the text "PMX" in the upper-right corner.

## Tips

For very large models (vertices > ~200,000), CPU vertex calculations may not keep up and frames may drop. In that case, try setting the number of parallel skinning threads to `2` or `4` in the .mdf.

{{< mdf>}}
parallel_skinning_numthreads=2
{{< /mdf>}}