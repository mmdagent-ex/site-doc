---
title: 音声対話をためす
slug: dialog-test
---
# 音声対話をためす

音声認識と音声合成が動けば、対話スクリプトを使ってごく簡単な音声応答を書くことができます。

{{< hint warning >}}
事前に[音声認識](../asr-setup)と[音声合成
](../tts-test)のセットアップを済ませてください。
{{< /hint >}}

## 一問一答のテスト

基本的に「音声認識の結果の `RECOG_EVENT_STOP` が来たら、対応する `SYNTH_START` コマンドを発行する」ようにスクリプトを書くことで簡単な発話応答が行えます。

Example の `main.fst` の末尾部分を以下のように書いてみましょう。

{{<fst>}}LOOP LOOP:
    RECOG_EVENT_STOP|こんにちは。 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！
{{</fst>}}

編集後、コンテンツを起動して「こんにちは」と話しかけてみてください。エージェントから「こんにちは、よろしくね」と返ってくれば成功です。

<img width="480" alt="snapshot" src="/images/example_2.png"/>

## モーションをつける

## 複数ターン会話

## 何種類かの認識結果に対応する

## 正規表現を使う