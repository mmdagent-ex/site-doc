

---
title: Effects
slug: mmd-effect
---

# Effects

The current MMDAgent-EX cannot handle effect files for [MikuMikuEffect](https://w.atwiki.jp/vpvpwiki/pages/219.html#id_d854d03f) (an effect expansion tool for MikuMikuDance, commonly known as MME) due to technical constraints.

However, it does provide pseudo-support for the two post-effects listed below. Please note that these are only approximations and the rendering results may differ from the originals.

## AutoLuminous

We've pseudo-implemented the [Auto Luminous](https://www.nicovideo.jp/watch/sm16087751) effect (created by Soboro, commonly known as AL, an effect that makes objects glow) in MMDAgent-EX using Mipmaps. Just like the original, materials with a `Shininess` value of 101 or above in 3D models will be expressed as glowing.

This process is enabled by default, and rendering is automatically switched on when a model with the above-mentioned materials is displayed. If you want to turn the effect off, please press `Shift + L` several times.

## Diffusion Effect

{{< hint warning >}}
The diffusion effect only works on Windows and Linux. It does not work on macOS due to OpenGL incompatibility.
{{< /hint >}}

We've implemented a version of the MME-ready [modified diffusion filter](https://okoneya.jp/mme_study/index.php?o_Diffusion) (by Otamon) in MMDAgent-EX using GLSL. It is off by default, but can be switched on by setting `diffusion_postfilter=true` in the .mdf file as shown below.

{{<mdf>}}
diffusion_postfilter=true
diffusion_postfilter_intensity=0.6
diffusion_postfilter_scale=1.0
{{</mdf>}}

`diffusion_postfilter_intensity` specifies the brightness of the light, and `diffusion_postfilter_scale` specifies the range of the light. The default values are as shown above, and if you want to change them, you need to specify the values.