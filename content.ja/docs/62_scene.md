---
title: シーンの設定
slug: scene
---
# シーンの設定

## 背景・床

**STAGE**

背景・床の画像、あるいはステージ用の3Dモデルの指定・変更。背景・床の表示サイズは .mdf の `stage_size` で指定。画像は指定サイズにフィットするよう伸長される。

```text
STAGE|(floor image file),(back image file)
STAGE|(stage file .xpmd or .pmd)
```

## 前景・フレーム

**WINDOWFRAME**

画面の一番上にフレーム画像 (.png) を重ね表示する。画像は画面の縦横比に合わせて伸長される。

![frame](/images/frame.png)

```text
WINDOWFRAME|filename.png
```
