---
title: 入手およびビルド
slug: build
---
# 入手およびビルド

MMDAgent-EX の動作環境は Windows, macOS, Linux, です。Windows上で WSL2 でも動作します。

以下の環境でビルド・動作を確認しています。

- **Windows**: Windows 11 with Visual Studio 2022 (win32 / x64)
- **macOS**: M2 Macbook Air / macOS Ventura / Sonoma / Sequoia, Intel Mac / macOS Sonoma
- **Linux**: Ubuntu-22.04, Ubuntu-20.04
- **Linux on WSL**: Ubuntu-22.04, 24.04 on WSL2 on Windows

## Windows

MMDAgent-EX のレポジトリの Release ページからダウンロードしてください。最新リリースの Assets にある `MMDAgent-EX-x64-vx.x.zip` （32ビット版が必要なときは `win32`）をダウンロードし、フォルダにすべて展開してください。

- [Releases - MMDAgent-EX](https://github.com/mmdagent-ex/MMDAgent-EX/releases/latest)

{{< hint info >}}

Windows では、インターネットからダウンロードした ZIP ファイルの中にある .exe や .dll をそのまま実行しようとすると、セキュリティ機能によって「実行がブロック」されることがあります。
これはウイルス対策の一環であり、異常ではありません。

### 実行できないときの対処方法

ダウンロードした zip ファイルを右クリックして「プロパティ」を開き、下の方に「このファイルはインターネットから取得したものです。コンピュータを保護するためにブロックされている可能性があります。」という注意書きと、[許可する] チェックボックス（または「ブロック解除」ボタン）が表示されるので、この チェックを入れて OK を押してください。その後、ZIP を展開してください。


{{< /hint >}}

展開したファイルが以下のようになっているかを確認してください。

    (top)/
    ├── MMDAgent-EX.exe
    ├── MMDAgent-EX.mdf
    ├── AppData/
    ├── DLLs64/  (win32版では Dlls/)
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

起動テストをします。`MMDAgent-EX.exe` をダブルクリックして、ウィンドウが出てくるか確認してください。何かウィンドウが開いたら、無事に動作している証拠です。ウィンドウを閉じて、次へ進んでください。

もし何も出てこない場合、[Visual C++ 2022の再配布可能パッケージ](https://learn.microsoft.com/ja-jp/cpp/windows/latest-supported-vc-redist?view=msvc-170) のインストールが必要かもしれません。[配布サイト](https://learn.microsoft.com/ja-jp/cpp/windows/latest-supported-vc-redist?view=msvc-170))にある `vc_regist.x64.exe` をダウンロードし、実行したあと、再び確認してみてください。

{{< hint info >}}

32ビット版(win32) は "X86" のほう (`vc_regist_x86.ext`) が必要です。

{{< /hint >}}

うまく動けばこれで終了です。次へ進んでください。

自分でソースコードからビルドする場合は、以下を読んでください。

## ビルド手順


## コードの入手


[GitHub](https://github.com/mmdagent-ex/MMDAgent-EX)よりレポジトリを入手する。

```shell
git clone https://github.com/mmdagent-ex/MMDAgent-EX.git
```

## ビルド手順

### macOS

以下のパッケージをあらかじめ `brew install` する。

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

CMake で以下の手順でビルド。実行バイナリとプラグインが `Release/` ディレクトリ以下に出力される。

```shell
cd MMDAgent-EX
cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

#### エラーケース１：`libomp` 関連でエラーが出る

以下を行ってから再トライする。

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

もし brew パッケージが通常と異なる場合は、環境変数 `HOMEBREW_PREFIX` を定義してください。MMDAgent-EX は `HOMEBREW_PREFIX` が定義されていればそれを使い、指定されていなければ `brew --prefix` の出力を brew パッケージのフォルダとしてビルドを行います。

### Linux (Ubuntu, WSL2)

必要なパッケージ名の一覧が `requirements-linux.txt` ファイルにあるので、その中のッケージを全てに `apt install` しておく。`apt` を使う場合以下の要領で一括で行える。

```shell
cd MMDAgent-EX
sudo apt update
sudo apt install `cat requirements-linux.txt`
```

CMake でビルド。

```shell
cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

実行バイナリとプラグインが `Release/` ディレクトリ以下に生成される。

### Windows

Visual Studio 2022 でビルドできます。

Visual Studio 2022 を新たにインストールする場合、インストールの際に「C++によるデスクトップ開発」にチェックを入れ、MSVC v143 と Windows 11 SDK (10.0.22000.0で確認）を併せてインストールしてください。

バージョン 2.1 (2025.10.1) 以降、Windows のビルドに必要な DLLおよびビルド済みバイナリはレポジトリに含まれなくなりました。Windows でビルドするには別途、最新リリースに付属の `MMDAgent-EX-deps_win.zip` を入手してください。最新リリースの Assets にあります。

入手先

- [Releases - MMDAgent-EX](https://github.com/mmdagent-ex/MMDAgent-EX/releases/latest) ←この中の Assets にある `MMDAgent-EX-deps_win.zip` 

ダウンロードしたら、レポジトリ内に重ねて展開してください。その後、以下のビルド手順に進みます。


1. `MMDAgent_vs2022.sln` を Visual Studio 2022 で開く
2. ソリューションエクスプローラで `main` を右クリックしてスタートアッププロジェクトに設定
3. プラットフォームを選択： `x64` あるいは`Win32` を選択
4. ビルド設定を `Release` に設定
5. 「ソリューションのビルド」を実行

起動を試したとき、すぐ終了してしまい動かない場合は、[Visual C++ 2022の再配布可能パッケージ](https://learn.microsoft.com/ja-jp/cpp/windows/latest-supported-vc-redist?view=msvc-170) のページにある `vc_regist.x64.exe` をダウンロードして実行したあと、再び確認してみてください。

{{< hint info >}}

32ビット版(win32) は "X86" のほう (`vc_regist_x86.ext`) が必要です。

{{< /hint >}}


## ビルドで生成されるファイル

実行に必要な全てのファイルは `Release` フォルダ以下に生成される。
{{< hint info >}}
以下はWindowsの例。macOSとLinuxでは .exe 拡張子は無く .dll は .so になる。
{{< /hint >}}

`AppData` 以下には実行時に必要な各種データファイルが格納されています。`DLLs` および `DLLs64` は Windows のみで、一部の機能の動作に必要な外部 DLL です。

    Release/
    ├── MMDAgent-EX.exe
    ├── MMDAgent-EX.mdf
    ├── AppData/
    ├── DLLs/
    ├── DLLs64/
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

以上でビルドは完了です。

動作に必要なのはこの `Release` フォルダ以下のファイルのみとなっています。別の場所で実行する場合、この `Release` フォルダごとコピーすればOKです。
