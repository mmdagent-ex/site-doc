---
title: Effects
slug: mmd-effect
---
# Effects

Due to technical limitations, the current MMDAgent-EX cannot handle effect files for [MikuMikuEffect](https://w.atwiki.jp/vpvpwiki/pages/219.html#id_d854d03f) (the MikuMikuDance effect extension tool, commonly called MME).

However, the following two post-effects are pseudo-supported. Please note these are only approximations and do not reproduce the original rendering exactly.

## AutoLuminous

[Auto Luminous](https://www.nicovideo.jp/watch/sm16087751) (by Soboro, commonly called "AL" -- an effect that makes objects glow) is pseudo-implemented inside MMDAgent-EX using mipmaps. As in the original, materials on 3D models with `Shininess` of 101 or higher are rendered as emissive.

This effect is enabled by default and will automatically turn on when a model with such materials is displayed. To turn the effect off, press `Shift + L` several times.

## Diffusion Effect

{{< hint warning >}}
The diffusion effect only works on Windows and Linux. It does not work on macOS due to OpenGL incompatibilities.
{{< /hint >}}

MMDAgent-EX includes a GLSL implementation based on [Otamon's modified diffusion filter for MME](https://okoneya.jp/mme_study/index.php?o_Diffusion). It is off by default, but you can enable it by setting `diffusion_postfilter=true` in the .mdf file like this:

{{<mdf>}}
diffusion_postfilter=true
diffusion_postfilter_intensity=0.6
diffusion_postfilter_scale=1.0
{{</mdf>}}

`diffusion_postfilter_intensity` controls the glow intensity, and `diffusion_postfilter_scale` controls the glow radius. The defaults are shown above; specify values to change them.
