---
title: コンテンツのWeb配信
slug: web-content
---
# Webでコンテンツを配信する

コンテンツを Web サーバ上で公開して、MMDAgent-EX が直接ダウンロード・再生することができます。URLを指定するだけで当該コンテンツをダウンロード・再生できるほか、サーバのコンテンツと自動同期させることができます。

MMDAgent-EX のコンテンツを Web で公開するためには、いくつかの公開用の作業が必要です。以下、コンテンツの公開手順から利用方法までを順に説明します。

## 配信の準備

### PACKAGE_DESC.txt

コンテンツのトップフォルダにパッケージ設定ファイル `PACKAGE_DESC.txt` を用意します。[詳細なフォーマット](../package-desc-format)はさておき、とりあえず以下の最小限の設定を記述します。

```text
execMDFFile=some/where/foobar.mdf
label=string
image=hoge.png
readme=readme.txt
readmeForceAgreement=true
```

- **execMDFFile**: 起動する .mdf ファイル。必須。
- **label**: コンテンツ名。指定しない場合、.mdf のファイル名が使われる。"`label=`" と指定するとラベルを表示しない。
- **image**: コンテンツをメニューに表示する際に使う画像ファイルのパス。指定しない場合のデフォルトは `banner.png`。存在しなければ画像は使用されない。画像はアスペクト比 7:1 で作るのを推奨。
- **readme**: コンテンツユーザに最初に読んでほしい README テキストファイルのパス。指定した場合、コンテンツの初回起動時に全画面で表示される。UTF-8 であること。
- **readmeForceAgreement**: true にすると、README ファイルを表示したあと一番下に `Accept` と `Decline` の 2つのボタンを表示し、 `Decline` を押した場合は再生しない、という挙動を追加。

### ファイルインデックス

`mit` でファイルインデックスを作る。

## アップロード

`PACKAGE_DESC.txt` とインデックスファイル(`.mmdagent-content-files`)を含めたコンテンツ全体をWeb サーバにアップする。

> Webサーバはディレクトリアクセス可能である必要があります。すなわち、コンテンツ全体を `https://foo.bar/some/dir` という場所にアップした場合、そのコンテンツ内の `model/xxx.pmd` というファイルは `https://foo.bar/some/dir/model/xxx.pmd` というURLで直接アクセス可能になっている必要があります。これは MMDAgent-EX がファイルごとに個別にダウンロードステータスを管理しているためです。このため、Google Drive や DropBox といったファイルごとにユニークなダウンロードURLを生成するサイトは使えないので注意してください。

## Webにあるコンテンツを再生する

起動時に、Webコンテンツのトップディレクトリの URL をコマンド引数で与えることでダウンロードと再生が行われます。URLは `https://foo.bar/some/dir` のほか、`mmdagent://foo.bar/some/dir` のようにも指定可能です。

```shell
  % ./Release/MMDAgent-EX.exe mmdagent://foo.bar/some/dir
```

この方法でダウンロードされたコンテンツはディスクにキャッシュされ、２回目以降は高速に起動します。ダウンロードが中断した場合でも次回同じコンテンツを起動する際に続きから再開されます。キャッシュは Windows ではデスクトップ直下、macOSとLinuxではホームの直下に `MMDAgent-Contents` という名前のフォルダが作成され、その下に置かれます。

ブックマークしておけばブックマークからも起動可能。

### コンテンツの自動更新

Webコンテンツは、常に同期して最新に保たれます。Web コンテンツの更新は定期的にチェックされ、差があるときは自動的に差分のダウンロード・更新が行われます。これにより、再生する Web コンテンツが常に最新であることが保証されます。
