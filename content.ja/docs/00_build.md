---
title: ビルド
slug: build
---
# ビルド

MMDAgent-EX の動作環境は macOS, Linux, Windows です。Windows上での WSL2 もサポートしています。以下の環境でビルド動作を確認しています。本ページの手順でビルドを実行して実行環境を構築してください。

- **Windows**: Windows 11 with Visual Studio 2022
- **macOS**: M2 Macbook Air / macOS Ventura / Sonoma / Sequoia, Intel Mac / macOS Sonoma
- **Linux**: Ubuntu-22.04, Ubuntu-20.04
- **Linux on WSL**: Ubuntu-22.04, 24.04 on WSL2 on Windows

Windows のビルド済み実行バイナリは、[GitHubのReleaseページ](https://github.com/mmdagent-ex/MMDAgent-EX/releases)にバージョンごとに置いてあるので、ビルド環境を構築できない場合はそちらをご利用ください。

## コードの入手

{{< hint danger >}}
！MMDAgent-EX 関連のレポジトリを clone するには [Git LFS](https://git-lfs.com/) が必須です。
{{< /hint >}}

Git LFS がインストールされているか事前にチェックし、なければインストールします。

{{< details "チェックおよびインストール方法" close >}}
インストールされているかどうかチェック

```shell
git lfs version
```

macOS (brew)

```shell
brew install git-lfs
git lfs install
```

Linux

```shell
sudo apt install git-lfs
git lfs install
```

Windows

[Git LFS のサイト](https://git-lfs.com/) から LFS 拡張をインストール。

{{< /details >}}

準備できたら [GitHub](https://github.com/mmdagent-ex/MMDAgent-EX)よりレポジトリを入手する。

```shell
git clone https://github.com/mmdagent-ex/MMDAgent-EX.git
```

## ビルド手順

### macOS

以下のパッケージが必要。全てあらかじめ `brew install` する。

- cmake
- poco
- glew
- libjpeg
- jpeg-turbo
- re2
- portaudio
- minizip
- libsndfile
- libsamplerate
- sox
- rabbitmq-c
- libomp
- librdkafka

CMake でビルド。ビルドした実行バイナリとプラグインが `Release/` ディレクトリ以下にコピーされる。

```shell
cd MMDAgent-EX
cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

#### エラーケース１：`libomp` 関連でエラーが出る

環境によっては関連ファイルがうまくインストールされないことがある。以下を行ってから再トライする。

```shell
brew link --force libomp
```

#### エラーケース２：`Utf8Proc::Utf8Proc` 関連でエラーが出る。

Poco ライブラリのバージョンが 14 以降だと、MMDAgent-EX が動きません。MMDAgent-EX に古い Poco 1.12.4 のソースアーカイブが同梱されているので、それを使ってビルドして使います。エラーが出たら、その後以下の手順に従ってください。(# の行は分かりやすくするためのコメントなので実際には入力しないでください)

```shell
# homebrew で入れた poco をアンインストール
brew uninstall poco
# 必要なモジュールをインストール
brew install pcre2
# Library_Poco 直下にある Poco 1.12.4 のソースコードを展開
cd Library_Poco
unzip poco-1.12.4-all.zip
cd poco-1.12.4-all
# cmake でビルドして /usr/local へインストール
mkdir cmake-build
cd cmake-build
cmake .. -DPOCO_UNBUNDLED=ON
make -s -j
sudo make install
# 戻ってビルドを通常どおりやりなおす
cd ../../..
cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

なお、brew パッケージの場所は、環境変数 `HOMEBREW_PREFIX` が定義されていればそれを使い、指定されていなければ `brew --prefix` の出力を用います。

### Linux (Ubuntu, WSL2)

必要なパッケージ名の一覧が `requirements-linux.txt` ファイルにあるので、その中に記されているパッケージを全て事前に `apt install` しておく。`Ubuntu` であれば以下の要領で一括で行える。

```shell
cd MMDAgent-EX
sudo apt install `cat requirements-linux.txt`
```

CMake でビルド。

```shell
cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

ビルド成功後、必要な実行バイナリとプラグインは `Release/` ディレクトリ以下にコピーされる。

### Windows

Visual Studio 2022 でビルドする。インストールの際には「C++によるデスクトップ開発」にチェックを入れ、MSVC v143 と Windows 11 SDK (10.0.22000.0で確認）を併せてインストールする。

1. `MMDAgent_vs2022.sln` を Visual Studio 2022 で開く
2. ソリューションエクスプローラで `main` を右クリックしてスタートアッププロジェクトに設定
3. ビルド設定を `Release` に設定
4. 「ソリューションのビルド」を実行

{{< hint info >}}
※ビルドがうまくいかない場合、リリースごとに公開されている実行バイナリを使うこともできます。[GitHubのリリースページ](https://github.com/mmdagent-ex/MMDAgent-EX/releases)から最新の win32 用の zip ファイルをダウンロードし、中身を `Release` フォルダ以下にコピーしてください。
{{< /hint >}}

## ビルドファイル

実行に必要な全てのファイルは `Release` フォルダ以下に生成される。
{{< hint info >}}
以下はWindowsの例。macOSとLinuxでは .exe 拡張子は無く .dll は .so になる。
{{< /hint >}}

`AppData` 以下には実行時に必要な各種データファイルがあり、`DLLs` には動作に必要な外部 DLL が同梱されている（Windowsのみ）。

    Release/
    ├── MMDAgent-EX.exe
    ├── MMDAgent-EX.mdf
    ├── AppData/
    ├── DLLs/
    └── Plugins/
        ├── Plugin_AnyScript.dll
        ├── Plugin_Audio.dll
        ├── Plugin_Flite_plus_hts_engine.dll
        ├── Plugin_Julius.dll
        ├── Plugin_Kafka.dll
        ├── Plugin_LookAt.dll
        ├── Plugin_Network.dll
        ├── Plugin_Open_JTalk.dll
        ├── Plugin_RabbitMQ.dll
        ├── Plugin_Remote.dll
        ├── Plugin_TextArea.dll
        ├── Plugin_Variables.dll
        └── Plugin_VIManager.dll

インストールが必要な場合、この `Release` フォルダ以下を、ディレクトリ構造を保ったままコピーする。

## 追記

以下の同梱ライブラリは Windows でのみ使われる。macOS / Ubuntu ではこれらの同梱ファイルは使われず、システムにインストールされているパッケージのものがリンクされる。

    Library_RE2
    Library_zlib
    Library_JPEG
    Library_libsndfile
    Library_PortAudio
    Library_glew
    Library_Poco
    Library_librdkafka
