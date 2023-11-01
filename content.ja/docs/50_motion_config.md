---
title: モーションの調整
slug: motion-config
---
# モーションの調整

モーションの重ね合わせでは動作が衝突することがあります。例えば、[「モーションの重ね」のページの例](../motion-layer)で使った Example の動作例では、キャラクターが歩くモーションと手を振るモーションを重ねていますが、ジェネの右腕のボーンに着目すると、その際、それぞれのモーションから以下の2つの動作が重なって指示される状況が発生しています。

- `walk.vmd` による前後に振る動作
- `onehandwave.vmd` による手を上にあげて左右に振る動作

このような動作の重なりに対して、どう解決するかを設定する方法を説明します。

## 上書き・加算・乗算

重なり時のデフォルトは「上書き」です。すなわち、最も優先順位が高いモーションの動きが採用され、それ以下の動きは無視されます。優先順位は最も遅く開始したモーションが最も高くなります。なので Example の例では `onehandwave.vmd` による左右に振る動作が `walk.vmd` による動作より優先されて出ていました。

この挙動は、モーション追加後に **MOTION_CONFIGURE** メッセージで変更できます。指定できるのは以下の3種類です。

- **MODE_REPLACE**: 上書き
- **MODEL_ADD**: 加算
- **MODEL_MUL**: 乗算（モーフのみ）

デフォルトは `MODE_REPLACE` で、下位のモーションを上書きします。加算 `MODEL_ADD`を指定すると、下位のモーションの動きに対してそのモーションの動きが「加算」されます。`MODEL_MUL` は下位の動きで算出されたモーフ量に対してこのモーションが示すモーフ値を乗算します。

{{<message>}}
MOTION_CONFIGURE|(model)|(motion)|MODE_REPLACE
MOTION_CONFIGURE|(model)|(motion)|MODE_ADD
MOTION_CONFIGURE|(model)|(motion)|MODE_MUL
{{</message>}}

加算や乗算の主な使い方は、モーションに追加で効果を与える等です。加算は揺らぎの追加やオフセット調整等、乗算は動きの抑制や強調をその場で行うようなときに使えます。

## ブレンド率

上記の指定と並行して、さらにモーションごとのブレンド率を指定できます。0.0 から 1.0 の値で、無指定時は 1.0 です。

{{<message>}}
MOTION_CONFIGURE|(model)|(motion)|MODE_REPLACE|(rate)
MOTION_CONFIGURE|(model)|(motion)|MODE_ADD|(rate)
MOTION_CONFIGURE|(model)|(motion)|MODE_MUL|(rate)
MOTION_CONFIGURE|(model)|(motion)|BLEND_RATE|(rate)
{{</message>}}

重ね時は、このブレンド率を乗じてから上書き・加算等の処理が行われます。具体的には以下のとおりです。

- MODE_REPLACE + rate指定: そのモーションの動作量に rate を乗じた動きで上書きされる
- MODE_ADD + rate指定: そのモーションの動作量に rate を乗じた動きが加算される
- MODE_MUL + rate指定: そのモーションが示す変化量に rate を乗じた変化量で乗算される

また、`BLEND_RATE` で値だけ変更することもできます。

## ボーン単位の制御

また、上記はモーション全体の指定ですがこれをボーン単位で詳細に設定することもできます。詳しくはリファレンスを見てください。
