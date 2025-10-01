---
title: Installation and Build
slug: build
---

# Installation and Build

MMDAgent-EX runs on Windows, macOS, and Linux. It also works on WSL2 under Windows.

The following environments have been tested for build and execution:

- **Windows**: Windows 11 with Visual Studio 2022 (win32 / x64)
- **macOS**: M2 MacBook Air / macOS Ventura / Sonoma / Sequoia, Intel Mac / macOS Sonoma
- **Linux**: Ubuntu-22.04, Ubuntu-20.04
- **Linux on WSL**: Ubuntu-22.04, 24.04 on WSL2 on Windows

## Windows

Executables can be downloaded from the Release page of the MMDAgent-EX repository.  Download the file `MMDAgent-EX-x64-vx.x.zip` from the latest release.

- [Releases - MMDAgent-EX](https://github.com/mmdagent-ex/MMDAgent-EX/releases/latest)

{{< hint info >}}

If you need the 32-bit version (win32), download the `win32` package.  Normally, the 64-bit version (`x64`) is recommended.

{{< /hint >}}

Extract the downloaded `.zip` file and place the contents in a suitable location.

※ Do not run the program directly from the ZIP file. Always extract (unzip) it before running.

{{< hint info >}}

On Windows, attempting to run `.exe` or `.dll` files inside a ZIP archive downloaded from the Internet may result in them being "blocked" by Windows security features.  
This is part of antivirus protection and is not an error.

### If you cannot run the program

Right-click the downloaded ZIP file, select "Properties," and look for a message near the bottom such as:  
*"This file came from another computer and might be blocked to help protect this computer."*  
There will be a [Unblock] checkbox (or "Allow" button). Check it, click OK, and then extract the ZIP file.

{{< /hint >}}

After extraction, make sure the contents look like this:

    (top)/
    ├── MMDAgent-EX.exe
    ├── MMDAgent-EX.mdf
    ├── AppData/
    ├── DLLs64/  (or Dlls/ on win32)
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

Test the startup by double-clicking `MMDAgent-EX.exe`.  
If a window appears, the program is running. Since it won’t work without content, you can close the window right after confirming.

If the program exits immediately and does not run, install the [Visual C++ 2022 Redistributable Package](https://learn.microsoft.com/ja-jp/cpp/windows/latest-supported-vc-redist?view=msvc-170).  
Download and run `vc_regist.x64.exe`, then try again.

{{< hint info >}}

For the 32-bit version (win32), install the "X86" package (`vc_regist_x86.exe`).

{{< /hint >}}

If it works, you’re done. Continue to the next steps.

To build from source code, read the following.

## Build Instructions

## Getting the Code

Clone the repository from [GitHub](https://github.com/mmdagent-ex/MMDAgent-EX):

```shell
git clone https://github.com/mmdagent-ex/MMDAgent-EX.git
```

## Build Steps

### macOS

Install the following packages with `brew install`:

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

Build with CMake. The executable and plugins will be generated under the Release/ directory.

```shell
cd MMDAgent-EX
cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

**Error Case 1: Errors related to libomp**

Run the following and retry:

```shell
brew link --force libomp
```

**Error Case 2: Errors related to `Utf8Proc::Utf8Proc`**

If the Poco library version is 1.14 or newer, MMDAgent-EX will not work.  MMDAgent-EX includes Poco 1.12.4 source archive, which should be used. If this error occurs, follow these steps (lines beginning with # are comments for clarity and should not be entered):

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

If your brew package prefix is non-standard, define the environment variable `HOMEBREW_PREFIX`.
MMDAgent-EX uses this variable if defined, otherwise it uses the result of `brew --prefix`.

## Linux (Ubuntu, WSL2)

A list of required packages is in the file `requirements-linux.txt`. Install all of them via apt. For example:

```shell
cd MMDAgent-EX
sudo apt update
sudo apt install `cat requirements-linux.txt`
```

Then build with CMake:

```shell
cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

The executable and plugins will be generated under the `Release/` directory.

### Windows

You can build with Visual Studio 2022.

When installing Visual Studio 2022, check "Desktop development with C++" and install MSVC v143 and the Windows 11 SDK (confirmed with 10.0.22000.0).

Since version 2.1 (2025.10.1), required DLLs and prebuilt binaries are no longer included in the repository.
To build on Windows, download `MMDAgent-EX-deps_win.zip` from the latest release.

Download location:

- [Releases - MMDAgent-EX](https://github.com/mmdagent-ex/MMDAgent-EX/releases/latest)
- Download `MMDAgent-EX-deps_win.zip` in the `Assets`.

After download, unpack the .zip file, and copy the contents into the top directory of the repository.

Then follow the build steps:

1. Open MMDAgent_vs2022.sln in Visual Studio 2022
2. In Solution Explorer, right-click main and set it as the startup project
3. Select the platform: x64 or Win32
4. Set build configuration to Release
5. Run "Build Solution"

If the program exits immediately and does not run, install [the Visual C++ 2022 Redistributable Package](https://learn.microsoft.com/ja-jp/cpp/windows/latest-supported-vc-redist?view=msvc-170).  Download and run `vc_regist.x64.exe`, then try again.

{{< hint info >}}

For the 32-bit version (win32), install the "X86" package (`vc_regist_x86.exe`).

{{< /hint >}}

## Generated Files

All necessary runtime files are generated under the `Release` folder.

{{< hint info >}}
The following is an example for Windows.
On macOS and Linux, there is no .exe extension, and .dll files become .so.
{{< /hint >}}

`AppData` contains required runtime data files.
`DLLs` and `DLLs64 `are Windows-only external DLLs required for certain features.

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

Only the files under the Release folder are required to run the program.  To run in another location, simply copy the entire Release folder.

