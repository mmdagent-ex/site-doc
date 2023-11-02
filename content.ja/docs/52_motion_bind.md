---
title: ボーン・モーフの値の直接指定
slug: motion-bind
---
# ボーン・モーフの値の直接指定

CGモデルの中には、見た目を切り替えるモーフや特別な動きを与えるボーンが設定されていることがあります。これらのモーフ・ボーンは、モーションにも組み入れられますが、モーションとは別に固定値をシナリオから設定できるほうが便利なことがあります。

MMDAgent-EX では、モーション影響下でないボーンやモーフの値をメッセージで直接指定することができます。例えば「ジェネ」のモデルが起動しているときに以下のメッセージを送ると、髪の毛のメッシュを消すことができます。

{{<message>}}
MODEL_BINDFACE|0|メッシュなし|1.0
{{</message>}}

なお、指定したボーンやモーフがモーションの影響下にある場合はモーション側が優先されます。

## 値をセットする

### MODEL_BINDBONE

ボーンに値をセットします。`x,y,z` が移動量、`rx,ry,rz` が回転量です。

{{<message>}}
MODEL_BINDBONE|(model alias)|(bone name)|x,y,z|rx,ry,rz
{{</message>}}

値はモデルが表示されている間有効です。成功したら  **MODEL_EVENT_BINDBONE** が出力されます。

{{<message>}}
MODEL_EVENT_BINDBONE|(model alias)|(bone name)
{{</message>}}

### MODEL_BINDFACE

モーフに値をセットします。`(value)` は重みで 0.0 から 1.0 の値です。最後の `(transition_duration)` を指定することで、その指定時間（秒）だけかけてゆっくり値を指定値へ変更させることができます。

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
