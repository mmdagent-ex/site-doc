---
title: 実行
slug: run
---
# 実行

MMDAgent-EX は起動時に1つのコンテンツを再生できます。ここでコンテンツとは、3Dモデルやモーション、FSTスクリプト、音声・画像等といった対話システムを構成するファイルの集合（アセット）のことを差します。以下、コンテンツの基本構成と起動方法を説明します。

## コンテンツの構成

コンテンツはあるフォルダ以下に構成されます。以下はあるコンテンツの典型的な構成例です。トップディレクトリに、起動ファイル兼設定ファイルとなる .mdf ファイルが必ず１つおかれます。さらに、使用するモジュールに応じて .fst, .dic, .jconf, .ojt といった各種ファイルが .mdf と同じプレフィックスで置かれます。また `BUTTON*.txt`, `PACKAGE_DESC.txt` もトップディレクトリに置きます。そのほかのファイル（モデル・モーション・画像等）は、フォルダ以下の任意の場所に置くことができます。

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

## コンテンツを起動

MMDAgent-EX のコマンドライン引数に、コンテンツフォルダのトップの .mdf ファイルを指定します。

```shell
./Release/MMDAgent-EX.exe /some/where/topdir/foobar.mdf
```

{{< details ".mdfファイルを複数指定した場合" open >}}
指定した順に全ての .mdf 内を読み込んで設定を行い、その後、最後に指定した末尾の .mdf のコンテンツを起動します。
{{< /details >}}

{{< details "指定しない場合" open >}}
以下の順番でコンテンツが探され、見つかったものを起動します。

- その実行環境でホームとして設定されているコンテンツ
- MMDAgent-EX 実行ファイルと同じフォルダの `MMDAgent-EX.mdf` 

いずれも見つからない場合、ブランク画面で起動します。
{{< /details >}}



