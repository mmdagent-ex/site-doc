---
title: Getting and Building
slug: build
---
# Getting and Building

MMDAgent-EX runs on Windows, macOS, and Linux. It also works on WSL2 on Windows.

We have verified building and running on the following environments:

- **Windows**: Windows 11 with Visual Studio 2022 (win32 / x64)
- **macOS**: M2 MacBook Air / macOS Ventura / Sonoma / Sequoia, Intel Mac / macOS Sonoma
- **Linux**: Ubuntu-22.04, Ubuntu-20.04
- **Linux on WSL**: Ubuntu-22.04, 24.04 on WSL2 on Windows

## Windows

Download MMDAgent-EX from the repository Releases page. Download `MMDAgent-EX-x64-vx.x.zip` from the latest release Assets (use the `win32` build if you need 32-bit), and extract all files into a folder.

- [Releases - MMDAgent-EX](https://github.com/mmdagent-ex/MMDAgent-EX/releases/latest)

{{< hint info >}}

On Windows, security features may block running .exe or .dll files extracted from ZIPs downloaded from the internet. This is part of antivirus/security measures and is not an error.

### If the executable is blocked

Right-click the downloaded zip file, open "Properties", and near the bottom you may see a warning that says "This file came from the Internet and might be blocked to help protect this computer." A checkbox (or an "Unblock" button) will be shown — check it and click OK. Then extract the ZIP.

{{< /hint >}}

Confirm the extracted files look like the following:

    (top)/
    ├── MMDAgent-EX.exe
    ├── MMDAgent-EX.mdf
    ├── AppData/
    ├── DLLs64/  (or DLLs on win32)
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

Run a quick start test. Double-click `MMDAgent-EX.exe` and check whether a window appears. If any window opens, the application is running correctly. Close the window and continue to the next section.

If nothing appears, you may need to install the Visual C++ 2022 Redistributable. Download `vc_regist.x64.exe` from the distribution site and run it, then try again: [Visual C++ 2022 Redistributable](https://learn.microsoft.com/ja-jp/cpp/windows/latest-supported-vc-redist?view=msvc-170) ([distribution site](https://learn.microsoft.com/ja-jp/cpp/windows/latest-supported-vc-redist?view=msvc-170))

{{< hint info >}}

The 32-bit build (win32) requires the "X86" package (`vc_regist_x86.ext`).

{{< /hint >}}

If it runs successfully, you're done — proceed to the next section.

If you want to build from source yourself, read the sections below.

## Build instructions

## Getting the source

Get the repository from [GitHub](https://github.com/mmdagent-ex/MMDAgent-EX).

```shell
git clone https://github.com/mmdagent-ex/MMDAgent-EX.git
```

## Build instructions

### macOS

Install the following packages in advance with brew:

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

Build with CMake. The executable and plugins will be output under the Release/ directory.

```shell
cd MMDAgent-EX
cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

#### Error case 1: Errors related to libomp

Run the following and retry:

```shell
brew link --force libomp
```

#### Error case 2: Errors related to Utf8Proc::Utf8Proc

MMDAgent-EX does not work with Poco library versions 1.4+ (Poco 14+). The repository includes an older Poco 1.12.4 source archive; use that to build. If you get the error, follow the steps below. (Do not type the comment lines that start with # — they are explanatory only.)

```shell
# Uninstall Poco installed via Homebrew
brew uninstall poco
# Install required modules
brew install pcre2
# Extract Poco 1.12.4 source code included under Library_Poco
cd Library_Poco
unzip poco-1.12.4-all.zip
cd poco-1.12.4-all
# Build with cmake and install to /usr/local
mkdir cmake-build
cd cmake-build
cmake .. -DPOCO_UNBUNDLED=ON
make -s -j
sudo make install
# Return and rebuild as usual
cd ../../..
cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

If your brew packages are installed in a nonstandard location, set the HOMEBREW_PREFIX environment variable. MMDAgent-EX will use HOMEBREW_PREFIX if defined; otherwise it will query `brew --prefix` to locate brew packages.

### Linux (Ubuntu, WSL2)

A list of required package names is provided in the `requirements-linux.txt` file. Install all those packages with apt. You can do this in one go with:

```shell
cd MMDAgent-EX
sudo apt update
sudo apt install `cat requirements-linux.txt`
```

Build with CMake:

```shell
cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

The executable and plugins will be generated under the Release/ directory.

### Windows

You can build with Visual Studio 2022.

When installing Visual Studio 2022, select the "Desktop development with C++" workload and make sure MSVC v143 and the Windows 11 SDK (confirmed with 10.0.22000.0) are installed.

Since version 2.1 (2025.10.1), the DLLs and prebuilt binaries required to build on Windows are no longer included in the repository. To build on Windows, download `MMDAgent-EX-deps_win.zip` included with the latest release. It is available in the Assets section of the latest release.

Where to get it:

- [Releases - MMDAgent-EX](https://github.com/mmdagent-ex/MMDAgent-EX/releases/latest) ← get `MMDAgent-EX-deps_win.zip` from the Assets there

After downloading, extract it into the repository (overlay the files), then follow the build steps below.

1. Open `MMDAgent_vs2022.sln` in Visual Studio 2022
2. In Solution Explorer, right-click `main` and set it as the Startup Project
3. Choose platform: select `x64` or `Win32`
4. Set the build configuration to `Release`
5. Run "Build Solution"

If the application immediately exits when you try to run it, you may need to install the Visual C++ 2022 Redistributable. Download and run `vc_regist.x64.exe` from the Visual C++ Redistributable page, then try again.

{{< hint info >}}

The 32-bit build (win32) requires the "X86" package (`vc_regist_x86.ext`).

{{< /hint >}}

## Files produced by the build

All files required to run are produced under the Release folder.
{{< hint info >}}
The example below is for Windows. On macOS and Linux there is no .exe extension and .dll files become .so.
{{< /hint >}}

`AppData` contains various runtime data files. `DLLs` and `DLLs64` are Windows-only folders containing external DLLs required for certain features.

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

That completes the build.

Only the files under the Release folder are required to run. To run on another machine or location, copy the entire Release folder.