---
title: 環境変数
slug: envval
---
# 環境変数

MMDAgent-EX のファイルで環境変数を参照する方法、および MMDAgent-EX の動作に影響を与える環境変数について。

## .mdf ファイルでの環境変数の参照

`％ENV{名前}` で環境変数を参照可能。指定された名前の環境変数が定義されていない場合、空白になる。

## `AUDIO_START` 用再生コマンド play

Ubuntu と macOS では、`AUDIO_START` メッセージでのサウンドファイル再生に sox 付属のコマンド "play" を使用する。再生は MMDAgent-EX 内部から以下の要領で `-q` をつけて起動される。

```shell
play -q file.mp3
```

この `play` コマンドは、まず最初に PATH 上で探される。もしパス上に `play` が無い等の理由でエラーになる場合は、`/opt/homebrew/bin/play`, `/usr/local/bin/play`, `/usr/bin/play` の順で探し、最初に見つかったものが使われる。

`play` の代わりのサウンド再生コマンドを指定したい場合は環境変数 `MMDAGENT_AUDIO_PLAY_COMMAND` で指定する。

### コンテンツフォルダ

コンテンツフォルダはダウンロードしたコンテンツや履歴情報などを保存するワークエリアで、デフォルトではデスクトップ直下の "MMDAgent-Contents"だが、
環境変数 `MMDAgentContentDir` でその場所を別の場所に指定できる。

