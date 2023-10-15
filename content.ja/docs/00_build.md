---
title: ビルド
slug: build
---
# ビルド

MMDAgent-EX の動作環境は macOS, Linux, Windows である。以下の環境でビルド動作を確認している。

- **macOS**: M2 Macbook Air / macOS Ventura 13.5
- **Linux**: Ubuntu-22.04, Ubuntu-20.04, Ubuntu-22.04 on WSL
- **WIndows**: Windows 11 with Visual Studio 2022

## コードの入手

Git LFS がインストールされているか事前にチェック。なければ先にインストールする。

{{< details "Git LFS のチェック方法とインストールの手順" close >}}
チェック

```shell
git lfs version
```

macOS

```shell
brew install git-lfs
```

Linux

```shell
sudo apt install git-lfs
```

Windows

[Git LFS のサイト](https://git-lfs.com/) から LFS 拡張をインストール。

{{< /details >}}

準備できたら [GitHub](https://github.com/mmdagent-ex/MMDAgent-EX)よりレポジトリを入手する。

```shell
git clone https://github.com/mmdagent-ex/MMDAgent-EX.git
cd MMDAgent-EX
```

## ビルド手順

### macOS

以下のパッケージが必要。全てあらかじめ `brew install` する。

- ffmpeg
- cmake
- poco
- glew
- libjpeg
- re2
- portaudio
- minizip
- opencv
- sox
- rabbitmq-c
- libomp

`libomp` のヘッダファイルがうまくインストールされないことがある。ビルドでエラーが出る場合は以下を追加で行う。

```shell
% brew link --force libomp
```

CMake でビルド。

```shell
% cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
% cmake --build build
```

ビルドした実行バイナリとプラグインが `Release/` ディレクトリ以下にコピーされる。

### Ubuntu

必要なパッケージ名の一覧が `requirements-linux.txt` ファイルにあるので、その中に記されているパッケージを全て事前に `apt install` しておく。以下の要領で一括で行える。

```shell
% sudo apt install `cat requirements-linux.txt`
```

CMake でビルド。

```shell
% cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
% cmake --build build
```

ビルド成功後、必要な実行バイナリとプラグインは `Release/` ディレクトリ以下にコピーされる。

### Windows

Visual Studio 2022 でビルドする。

1. `MMDAgent_vs2022.sln` を Visual Studio 2022 で開く
2. ソリューションエクスプローラで `main` を右クリックしてスタートアッププロジェクトに設定
3. ビルド設定を `Release` に設定
4. 「ソリューションをビルド」を実行

## ビルドファイル

実行に必要な全てのファイルは `Release` フォルダ以下に生成される。
{{< hint info >}}
以下はWindowsの例。macOSとLinuxでは .exe 拡張子は無く .dll は .so になる。
{{< /hint >}}

`AppData` 以下には実行時に必要な各種データファイルがあり、`DLLs` には動作に必要な外部 DLL が同梱されている（Windowsのみ）。

```text
Release/
├── MMDAgent-EX.exe
├── MMDAgent-EX.mdf
├── AppData/
├── DLLs/
└── Plugins/
    ├── Plugin_AnyScript.dll
    ├── Plugin_Audio.dll
    ├── Plugin_Flite_plus_hts_engine.dll
    ├── Plugin_Kafka.dll
    ├── Plugin_LookAt.dll
    ├── Plugin_Network.dll
    ├── Plugin_Open_JTalk.dll
    ├── Plugin_RabbitMQ.dll
    ├── Plugin_Remote.dll
    ├── Plugin_TextArea.dll
    ├── Plugin_Variables.dll
    └── Plugin_VIManager.dll
```

インストールが必要な場合、この `Release` フォルダ以下を、ディレクトリ構造を保ったままコピーする。

## 追記

以下の同梱ライブラリは Windows でのみ使われる。macOS / Ubuntu ではこれらの同梱ファイルは使われず、システムにインストールされているパッケージのものがリンクされる。

```text
Library_RE2
Library_zlib
Library_JPEG
Library_libsndfile
Library_PortAudio
Library_glew
Library_Poco
Library_ffmpeg
Library_OpenCV
```
