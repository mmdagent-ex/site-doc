---
title: How To Build
slug: build
---

# How To Build

MMDAgent-EX runs on macOS, Linux, and Windows. It can also runs on WSL2 environment.  The build operation has been confirmed in the following environments:

- **macOS**: M2 Macbook Air / macOS Ventura, Intel Mac / macOS Sonoma
- **Linux**: Ubuntu-22.04, Ubuntu-20.04
- **Windows**: Windows 11 with Visual Studio 2022
- **Linux on WSL**: Ubuntu-22.04 on WSL2 (v1.2.5.0) on Windows

Windows users can also get pre-built binaries from [GitHub Release page](https://github.com/mmdagent-ex/MMDAgent-EX/releases).

## Obtaining the Code

{{< hint danger >}}
[GIT LFS](https://git-lfs.com/) should be installed beforehand.
{{< /hint >}}

Before obtaining repository, make sure to have Git LFS installed on your envieonment; if not, install it.

{{< details "Check and Install Git LFS" close >}}
Check if it's installed

```shell
git lfs version
```

Install on macOS using brew:

```shell
brew install git-lfs
git lfs install
```

Install on Linux:

```shell
sudo apt install git-lfs
git lfs install
```

Windows:

Install the LFS extension from the [Git LFS website](https://git-lfs.com/).

{{< /details >}}

Obtain the repository from [GitHub](https://github.com/mmdagent-ex/MMDAgent-EX) using Git LFS:

```shell
git clone https://github.com/mmdagent-ex/MMDAgent-EX.git
```

## Build Procedure

### macOS

The following packages are required. Install all before build with `brew install`.

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

{{< hint ms >}}
Also install the following packages for moonshot version.

- ffmpeg
- opencv
{{< /hint >}}

Do build with CMake. The built executable and plugins will be stored under to the `Release/` directory.

```shell
cd MMDAgent-EX
cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

#### Error case 1: an error occurs for `libomp`

Perform the following and retry.

```shell
brew link --force libomp
```

#### Error case 2: an error for `Utf8Proc::Utf8Proc`

This error comes from Poco library.  Recent brew installes Poco-14.x, which is not compatible with MMDAgent-EX.  In such case you should use old Poco.  A source code of version 1.12.4 is included in the MMDAgent-EX repository, so build and install it.

After you see the above error, perform below (ignore `#` lines)

```shell
# uninstall poco previously installed by homebrew
brew uninstall poco
# install required library
brew install pcre2
# Unpack source code of Poco-1.12.4 that exists under Library_Poco folder
cd Library_Poco
unzip poco-1.12.4-all.zip
cd poco-1.12.4-all
# build it with cmake, and install to /usr/local
mkdir cmake-build
cd cmake-build
cmake .. -DPOCO_UNBUNDLED=ON
make -s -j
sudo make install
# return back to MMDAgent-EX top and redo build process from start
cd ../../..
cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

The brew package directory may change depending on your environment, i.e., `/usr/local/` or `/opt/homebrew`.  The build script will try to guess the prefix directory by executing `brew --prefix`.  If it does not work well, specify the brew prefix path with environment variable `HOMEBREW_PREFIX`.

### Linux (Ubuntu, WSL2)

The list of required packages is in the `requirements-linux.txt`, so install all the packages listed in it in advance with `apt install`. If you are using `Ubuntu`, you can do all at once as follows:

```shell
cd MMDAgent-EX
sudo apt install `cat requirements-linux.txt`
```

{{< hint ms >}}
Please install additional packages as the following.

```shell
sudo apt install libavcodec-dev
sudo apt install libopencv-dev
```
{{< /hint >}}

Build with CMake:

```shell
cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

After a successful build, the necessary executables and plugins are ready at the `Release/` directory.

### Windows

Build with Visual Studio 2022.  It requires C++ development environment and Windows SDK.  During Visual Studio's installation, check "Desktop development with C++" and install MSVC v143 and Windows 11 SDK (confirmed with 10.0.22000.0).

1. Open `MMDAgent_vs2022.sln` with Visual Studio 2022
2. Right-click on `main` in Solution Explorer and set as the startup project
3. Set the build configuration to `Release`
4. Execute "Build Solution"

{{< hint info >}}
Pre-built executable binaries are also provided at  [GitHub releases page](https://github.com/mmdagent-ex/MMDAgent-EX/releases). Download the latest zip file for win32 from the [GitHub releases page](https://github.com/mmdagent-ex/MMDAgent-EX/releases) and unzip the contents into the Release folder.
{{< /hint >}}

{{< hint info >}}
If MMDAgent-EX.exe does not work, try installing the latest x86 [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170).  You need to install **x86** version (vc_redist_x86.exe), even if your os is 64 bit, since the MMDAgent-EX.exe is compiled as 32bit application.
{{< /hint >}}

## Built Files

All the files required for execution will be generated under the `Release` folder.
{{< hint info >}}
On Windows, an executable file has ".exe" prefix and the plugin files has ".dll" suffix.  On macOS and Linux, there is no ".exe" for executable file, and plugin file has ".so" suffix instead.
{{< /hint >}}

Under `AppData`, there are various data files required for execution, and `DLLs` includes external DLLs necessary for operation for Windows.

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

If installation is necessary, copy everything under this `Release` folder, maintaining the directory structure.

## Libraries included in the archive but not used in macOS and Linux

The following bundled libraries are used only on Windows. On macOS / Ubuntu, these bundled files are not used, and the ones from the packages installed on the system are linked instead.

    Library_RE2
    Library_zlib
    Library_JPEG
    Library_libsndfile
    Library_PortAudio
    Library_glew
    Library_Poco
    Library_librdkafka
