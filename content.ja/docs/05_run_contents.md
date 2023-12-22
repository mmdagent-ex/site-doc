---
title: Exampleの実行
slug: run
---
# Exampleの実行

MMDAgent-EX はコンテンツを指定して起動します。以下、MMDAgent-EX におけるコンテンツの概略と、実際に Example コンテンツを起動する手順を説明します。

## コンテンツについて

MMDAgent-EX はコンテンツを再生します。コンテンツとは、3Dモデルやモーション、FSTスクリプト、音声・画像等といった対話システムを構成するファイルの集合体（アセット）を指します。

コンテンツの一般的な構成は以下のようになります。トップディレクトリに、起動ファイル兼設定ファイルとなる .mdf ファイルが必ず１つおかれます。さらに、使用するモジュールに応じて .fst, .dic, .jconf, .ojt といった各種ファイルが .mdf と同じプレフィックスで置かれます。また `BUTTON*.txt`, `PACKAGE_DESC.txt` もトップディレクトリに置きます。そのほかのファイル（モデル・モーション・画像等）は、フォルダ以下の任意の場所に置くことができます。

    topdir/
        |- foobar.mdf         Startup / Configuration
        |- foobar.fst         Dialogue Script
        |- foobar.dic         Additional dictionary for Julius
        |- foobar.jconf       Additional Julius jconf file
        |- foobar.ojt         Open JTalk setting file
        |- PACKAGE_DESC.txt   Package info for web-based deploy
        |- README.txt         Readme doc
        +- (SubDirectories)
            |- 3-D models (.pmd)
            |- Motions (.vmd)
            |- TTS Voice model (.htsvoice)
            |- Background/Floor (images)
            |- Sound / Music files (sound files)
            |- Images, Text files, etc.

## Example コンテンツの入手

[サンプルコンテンツ](https://github.com/mmdagent-ex/example)は最小限のスクリプト、サンプルの画像・モーション、Open JTalk 用のモデル mei、およびCGモデル[「ジェネ」](https://github.com/mmdagent-ex/gene)と[「うか」](https://github.com/mmdagent-ex/uka)を含むレポジトリです。このサイトの説明はこのサンプルコンテンツを使って行われますので、入手してください。

    example/
        |- main.mdf         Startup / Configuration
        |- main.fst         Dialogue Script
        |- main.ojt         Open JTalk setting
        |- images/
        |    |- ...
        |- motions/
        |    |- ...
        |- voice/           Voice model "mei" for Open JTalk
        |    |- mei/
        |- gene/            CG-CA model "Gene"
        |    |- Gene.pmd
        |- uka/             CG-CA model "Uka"
        |    |- Uka.pmd
        |- example_motion/     Example files for motion blending
        +- example_websocket/  Example files for websocket connection

サンプルコンテンツを clone してください。CG-CAのレポジトリを内部で clone するために submodule を使っているので `--recursive` をつけます。

```shell
git clone --recursive https://github.com/mmdagent-ex/example
```

## コンテンツを起動

MMDAgent-EX のコマンドライン引数にコンテンツのフォルダのトップにある .mdf ファイルを指定して起動します。

macOS / Linux ターミナル：

```shell
./Release/MMDAgent-EX ./example/main.mdf
```

Windows コマンドシェル：

```text
.\Release\MMDAgent-EX.exe .\example\main.mdf
```

以下のような画面が出たら起動成功です。

<img width="480" alt="example snapshot" src="/images/example_1.png"/>

{{< hint info >}}
この Example をホームにセットすれば、次回以降は実行バイナリのみで Example が起動するようにできます。

実行中のコンテンツをホームに設定するには：

- MMDAgent-EX の画面で `/` キーを押す→メニューが開く
- → で右のメニューへ移動
- 上下キーで "Set current as Home" を選択してエンター

{{< /hint >}}

### WSL で失敗する場合

WSL で画面が出てこず起動に失敗する場合は、WSL のバージョンが古い可能性があります。GUIアプリがサポートされた最新の WSL2 を使ってください。詳細は[こちらのサイトを参考に WSL のバージョンを最新にしてください](https://learn.microsoft.com/windows/wsl/tutorials/gui-apps)。
