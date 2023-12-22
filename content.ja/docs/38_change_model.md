---
title: CGアバターを変えてみる
slug: change-model
---
# CGアバターについて

## ジェネ / Gene

Example のデフォルトで表示されているのは「ジェネ」というCGアバターです。これは[名工大で開発された](https://www.slp.nitech.ac.jp/avatar/)対話用のCGモデルで、ムーンショット型研究開発「アバター共生社会」で開発された CG-CA（CG Cybernetic Agent）として CC-BY ライセンスで提供されています。利用条件など詳しくは[公開レポジトリ](https://github.com/mmdagent-ex/gene) をご覧ください。

<img width="480" alt="example snapshot" src="/images/example_1.png"/>


## うか / Uka

Example にはもう1体、「うか」というCGアバターも同梱されています。example の `main.fst` のモデルファイル `Gene.pmd` をしているところを以下のように変更して起動しなおして、モデルが変わることを確かめてください。

{{<fst>}}
    ...
    <eps> MODEL_ADD|0|uka/MS_Uka.pmd
    ...
{{</fst>}}

```shell
./Release/MMDAgent-EX.exe ./example/main.mdf
```

<img alt="example snapshot of uka" src="/images/Uka.png"/>

MMDAgent-EX は MikuMikuDance 形式の3Dモデルをサポートしており、同形式のモデルを読み込むことができます。詳しい方法は[3Dモデルの表示](../3d-model)のページを見てください。
