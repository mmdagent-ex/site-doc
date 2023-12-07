---
title: モーションのブレンド
slug: motion-blend
---
# モーションのブレンド

モーションの重ね合わせにおいて、複数のモーションが指示する動作が衝突することがあります。例えば[「モーションの重ね」のページの例](../motion-layer)では、歩くモーションと手を振るモーションを重ねたとき、キャラクターの右腕のボーンについて、`walk.vmd` による腕を前後に振る動作と `onehandwave.vmd` による手を上にあげて左右に振る動作が重なってしまいます。

このような動作の重なりに対して、どう解決するかを設定する方法を説明します。

## 上書き・加算・乗算

重なり時のデフォルトは「上書き」です。すなわち、最も優先順位が高いモーションの動きが採用され、それ以下の動きは無視されます。優先順位は最も遅く開始したモーションが最も高くなります。Example の例では `onehandwave.vmd` による左右に振る動作が `walk.vmd` による動作より優先されて出ていました。

この重なり時の挙動はモーション追加後に **MOTION_CONFIGURE** メッセージを発行することで変更できます。指定できるのは以下の3種類です。

- **MODE_REPLACE**: 上書き
- **MODEL_ADD**: 加算
- **MODEL_MUL**: 乗算（モーフのみ）

デフォルトの `MODE_REPLACE` は下位のモーションを上書きします。加算 `MODEL_ADD`を指定すると、下位のモーションの動きに対してそのモーションの動きが「加算」されます。`MODEL_MUL` は下位の動きで算出されたモーフ量に対してこのモーションが示すモーフ値を乗算します。

{{<message>}}
MOTION_CONFIGURE|(model)|(motion)|MODE_REPLACE
MOTION_CONFIGURE|(model)|(motion)|MODE_ADD
MOTION_CONFIGURE|(model)|(motion)|MODE_MUL
{{</message>}}

利用方法の例としては、加算は揺らぎの追加やオフセット調整など、MMDで言うところの[「多段ボーン」](https://www.google.com/search?q=%E5%A4%9A%E6%AE%B5%E3%83%9C%E3%83%BC%E3%83%B3)と同様のことが行えます。また、乗算は「0 を指定して下位モーションの一部モーフの変化を無効化する」といった使い方ができます。

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

また、`BLEND_RATE` で設定を変更することなくレートの値だけ変更することもできます。

## ボーン単位の制御

また、上記はモーション全体の指定ですがこれをボーン単位で詳細に設定することもできます。詳しくはリファレンスを見てください。
