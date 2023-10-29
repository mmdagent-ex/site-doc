---
title: エフェクト
slug: mmd-effect
---
# エフェクト

現在の MMDAgent-EX は、技術上の制約から、[MikuMikuEffect](https://w.atwiki.jp/vpvpwiki/pages/219.html#id_d854d03f)（MikuMikuDance用エフェクト拡張ツール、通称MME）用のエフェクトファイルを扱うことはできません。

ただし、以下の２つのポストエフェクトについては、疑似的にサポートしています。あくまで疑似的なものであり本来のレンダリング結果とは異なりますので、利用の際はご了承ください。

## AutoLuminous

[Auto Luminous](https://www.nicovideo.jp/watch/sm16087751)（そぼろさん作、通称AL、オブジェクトを発光させるエフェクト）を MMDAgent-EX 内部で Mipmap を使って疑似的に実装しています。オリジナルと同様に、3Dモデルで `Shininess` が101以上の材質が発光表現されます。

この処理はデフォルトで有効になっており、上記のような材質を持つモデルを表示したときに自動的にレンダリングがONになります。効果を OFF にしたいときは `Shift + L` を何度か押して OFF にしてください。

## Diffusion Effect

{{< hint warning >}}
ディフュージョンエフェクトは Windows および Linux でのみ動作します。macOS では OpenGL の非互換性のため動作しません。
{{< /hint >}}

MME用の [改変版ディフュージョンフィルタ](https://okoneya.jp/mme_study/index.php?o_Diffusion)（おたもんさん）をベースに GLSL で実装したものを MMDAgent-EX 内部で実装しています。デフォルトでは off ですが、以下のように `diffusion_postfilter=true` を .mdf に設定することでONになります。

{{<mdf>}}
diffusion_postfilter=true
diffusion_postfilter_intensity=0.6
diffusion_postfilter_scale=1.0
{{</mdf>}}

`diffusion_postfilter_intensity` は光る強さ、`diffusion_postfilter_scale` は光る範囲の広さです。デフォルト値は上記のとおりで、変更する場合は値を指定します。
