---
title: ボーン・モーフの値の直接指定
slug: motion-bind
---
# ボーン・モーフの値の直接指定

モーションを使わずボーンやモーフの値をメッセージで直接指定することができます。個別のモーフのON/OFFや .fst スクリプトでのボーン・モーフ制御に使えます。

なお、ボーンやモーフがモーションの影響下にある場合は、モーション側が優先されます。

## 値をセットする

### MODEL_BINDBONE

ボーンに固定値をセットします。`x,y,z` が移動量、`rx,ry,rz` が回転量です。

{{<message>}}
MODEL_BINDBONE|(model alias)|(bone name)|x,y,z|rx,ry,rz
{{</message>}}

値はモデルが表示されている間有効です。成功したら  **MODEL_EVENT_BINDBONE** が出力されます。

{{<message>}}
MODEL_EVENT_BINDBONE|(model alias)|(bone name)
{{</message>}}

### MODEL_BINDFACE

モーフに固定値をセットします。`(value)` は重みで 0.0 から 1.0 の値です。最後の `(transition_duration)` を指定することで、その指定時間（秒）だけかけてゆっくり値を指定値へ変更させることができます。

{{<message>}}
MODEL_BINDFACE|(model alias)|(morph name)|(value)
MODEL_BINDFACE|(model alias)|(morph name)|(value)|(transition_duration)
{{</message>}}

こちらもモデルが表示されている間適用されます。セットに成功したら  **MODEL_EVENT_BINDFACE** が出力されます。

{{<message>}}
MODEL_EVENT_BINDFACE|(model alias)|(morph name)
{{</message>}}

## 解除する

### MODEL_UNBINDBONE

ボーンの値のセットを解除する。終了時に **MODEL_EVENT_UNBINDBONE** を発行する。

```text
MODEL_UNBINDBONE|model alias|bone name
MODEL_EVENT_UNBINDBONE|model alias|bone name
```

### MODEL_UNBINDFACE

モーフの値のセットを解除する。終了時に **MODEL_EVENT_UNBINDFACE** を発行する。

```text
MODEL_UNBINDFACE|model alias|morph name
MODEL_EVENT_UNBINDFACE|model alias|morph name
```
