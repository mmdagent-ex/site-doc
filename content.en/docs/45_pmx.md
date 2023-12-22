

---
title: PMX Model
slug: pmx
---

# PMX Model

MMDAgent-EX can temporarily display 3D models in the PMX format. However, it is not possible to directly read .pmx files, so they need to be converted to another format (.pmd and .csv) in advance.

## Conversion Procedure

PMX models can be temporarily displayed in MMDAgent-EX by converting them to .pmd and .csv using [PMXEditor](https://kkhk22.seesaa.net/category/14045227-1.html) (created by HokkyokuP). The procedure is as follows:

{{< hint info >}}
Please use the latest version if possible (tested version: 0.2.7.3)
{{< /hint >}}

- [Acquire PMXEditor](https://kkhk22.seesaa.net/category/14045227-1.html) and install it
- Open the target PMX file with PMXEditor.
- From the menu, select "File - Export" and save with the extension `.pmd`.
- From the menu, select "File - Convert to Text(CSV) - Export to CSV file" and save with the extension `.pmd.csv`.

Please place the .pmd and .csv converted by the above procedure in the same location as the original pmx. In particular, the file names need to be as follows. Please pay attention to the name of the .csv.

```text
  model.pmx
  model.pmd
  model.pmd.csv
```

## How to Use

When using MMDAgent-EX, specify the converted .pmd file with the `MODEL_ADD` command. The .csv file is read at the same time, and rendering close to PMX is performed.

## Compatibility

This is a list of the features of PMD and PMX supported by MMDAgent-EX. Please note that even for items marked with ○, operation is not guaranteed and it may not work depending on the model.

|Item|PMD|PMX|
|----|---|---|
|Physics Calculation|○|○|
|IK ON/OFF|○|○|
|Hidden Morph|○|○|
|Material Information|○|○|
|Edge Ratio|-|○|
|BDEF4|-|○|
|SDEF|-|△(Temporary)|
|Transformation Hierarchy|-|○|
|Post-Physics Deformation|-|○|
|Bone Update Order|-|○|
|Vertex Morph|-|○|
|Bone Morph|-|○|
|UV Morph|-|○|
|Material Morph|-|○(Only TeX coefficient is ×)|
|Group Morph|-|○|
|Additional UV|-|×|
|External Parent Transformation|-|×|


## Usage Guidelines

Please ensure you adhere to the ELSI guidelines of this software, respect the terms of use and community practices, and use it appropriately.

Note: When using the PMX model in this system, the word "PMX" will continuously be displayed in the top right corner.

## Tips

Attempting to display a large model (vertices > around 200,000) may result in the CPU not keeping up with vertex calculations, leading to dropped frames. In such cases, try setting the number of parallel skinning threads to `2` or `4` in the .mdf file.

{{< mdf >}}
parallel_skinning_numthreads=2
{{< /mdf >}}
