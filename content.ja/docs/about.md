---
title: MMDAgent-EXとは
slug: about
---
# MMDAgent-EXとは

MMDAgent-EX は音声対話システム・アバターコミュニケーションのオープンソース研究開発プラットフォームです。CGキャラクターの表示・制御と音声・言語処理を組み合わせ、任意の音声対話システムを構築できる単体のシステムです。様々なモジュールの追加により、カメラやネットワークを組み合わせた多様なマルチモーダル対話システムを構築することが可能です。また、動作コマンドや音声データを外部からネットワーク経由で送り込むことでリップシンク付き音声再生やモーション再生・制御ができ、さまざまな既存の対話システムのフロントエンドとして動作させることもできます。

[MMDAgent](https://www.mmdagent.jp/) は2011年に音声インタラクションの研究開発のためのオープンソースのツールキットとして名古屋工業大学で開発されました。その後、研究のために対応フォーマット拡張、ネットワーク対応、UIの整備、外部操作機能などが開発されてきました。2020年12月より、[ムーンショット型研究開発事業「アバター共生社会」](https://avatar-ss.org/)において、CGキャラクターを介して会話するCGアバターコミュニケーションのプラットフォームとしても研究開発が進められています。ここでは、その研究開発の成果の一部をオープンソースで公開するものです。

## 特徴

MMDAgent-EX は [MMD (MikuMikuDance)](https://sites.google.com/view/vpvp/) 互換の独自のOpenGLベースの描画エンジンを持ち、MMDの形式の3Dモデルとモーションを用いて対話キャラクターを構築することができます。[Julius](https://github.com/julius-speech/julius)や [Open JTalk](https://open-jtalk.sp.nitech.ac.jp/) などの名工大で開発された音声認識・音声合成エンジンを持つほか、FSTベースの状態遷移型の原始的な対話スクリプト機能を内蔵しており、これ単体で音声対話システムを構築することが可能です。また、Python等のスクリプト言語と接続することができ、任意のクラウド音声認識・音声合成エンジンや ChatGPT 等の LLM をモジュールとして追加することができます。また、ソケット接続による外部制御にも対応していますので、既存の対話応答生成システムの入出力フロントエンドとして用いることもできます。

- 音声インタラクションや音声対話システムのためのオールインワンプラットフォーム（Windows, macOS, Linux）
- 軽量で高効率な内蔵 CG アバターレンダリングエンジン：MMD (MikuMikuDance) ファイル形式にフル対応
- CPUのみで高速に動く低遅延音声認識(Julius), 音声合成(Open JTalk)を内蔵、自由に入れ替え可能。
- 容易な開発と拡張：各種クラウドエンジンやLLMなどの任意のアプリケーションやスクリプトと容易に結合可能。
- 完全な集約されたドキュメント（本サイト）

## MMDAgent との違い

前身である MMDAgent からの差分は[こちらをご覧ください](../changes-since-original-mmdagent/)。

## 読み方

表記は **MMDAgent-EX** でも **MMD-Agent EX** でも可です。”MMD” の部分は “Multi-Modal Dialogue” と “MikuMikuDance” のダブルミーニングです。我々は「エムエムディーエージェント イーエックス」と呼んでいます。

## 文献引用

以下を使ってください。

**APA**

    Lee, A. (2023). MMDAgent-EX (Version 1.0.0) [Computer software].
    https://doi.org/10.5281/zenodo.10427369

**BibTeX**

    @software{Lee_MMDAgent-EX_2023,
        author = {Lee, Akinobu},
        doi = {10.5281/zenodo.10427369},
        license = {Apache-2.0},
        month = dec,
        title = {{MMDAgent-EX}},
        url = {https://github.com/mmdagent-ex/MMDAgent-EX},
        version = {1.0.0},
        year = {2023}
    }

## Acknowledgments

MMDAgent-EX:

- Akinobu Lee (Nagoya Institute of Technology, Japan)

MMDAgent:

- Keiichi Tokuda (Nagoya Institute of Technology, Japan)
- Akinobu Lee (Nagoya Institute of Technology, Japan)
- Keiichiro Oura (Nagoya Institute of Technology, Japan)
- Daisuke Yamamoto (Nagoya Institute of Technology, Japan)
