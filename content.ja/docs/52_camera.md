---
title: カメラ（視点）
slug: camera
---
# カメラ（視点）

## 視点（カメラ）

**CAMERA**

視点を変更する。3つの指定方法がある。

**数値で指定**：`x,y,z|rx,ry,rz|(distance)|(fovy)` でパラメータを指定する。これらの値は `D` キーで簡易ログを表示したときに左下に出てくる値で設定できる。Transition time period は指定した視点までどう変化するかを指定。デフォルト（-1）は滑らかに視点移動、0で即座にジャンプ、0より大きい値でその秒数をかけて指定座標まで定速移動。

```text
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)|(transition time period)
```

**モデルにマウント**: モデルの動きにカメラの動きをリアルタイムに追従させる。ボーン名を指定しない場合は「センター」ボーンに追従する。

```text
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)|(transition time period)|(model alias)
CAMERA|x,y,z|rx,ry,rz|(distance)|(fovy)|(transition time period)|(model alias)|(bone name)
```

**モーションで指定**：カメラの動きをあらかじめ定義したカメラモーションファイル（.vmd）を指定して動作開始

```text
CAMERA|(camera motion file name)
```
