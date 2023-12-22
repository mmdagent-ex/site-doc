

---
title: Web Distribution of Contents
slug: web-content
---

# Distributing Content on the Web

Content can be published on a web server, allowing MMDAgent-EX to directly download and play it. You can download and play the content just by specifying the URL, and it can be automatically synchronized with the server's content.

To publish MMDAgent-EX content on the web, several publication tasks are necessary. Here, we will explain the process from publication to usage in order.

{{< hint warning >}}
Distributing content to others constitutes **secondary distribution (redistribution)** of files. Please pay attention to the usage conditions of the files and materials included in the content.
{{< /hint >}}

## Preparing for Distribution

### PACKAGE_DESC.txt

Prepare a package configuration file `PACKAGE_DESC.txt` in the top folder of the content. Leaving aside the [detailed format](../package-desc-format) for now, let's start by describing the following minimum settings.

```text
execMDFFile=some/where/foobar.mdf
label=string
image=hoge.png
readme=readme.txt
readmeForceAgreement=true
```

- **execMDFFile**: The .mdf file to be launched. Required.
- **label**: The name of the content. If not specified, the filename of the .mdf will be used. If "`label=`" is specified, the label will not be displayed.
- **image**: The path to the image file used when displaying the content in the menu. The default if not specified is `banner.png`. If it does not exist, no image will be used. It is recommended to create images with a 7:1 aspect ratio.
- **readme**: The path to the README text file that you want the content user to read first. If specified, it will be displayed in full screen when the content is first launched. Must be in UTF-8.
- **readmeForceAgreement**: If set to true, after displaying the README file, two buttons, `Accept` and `Decline`, are displayed at the bottom. If the `Decline` button is pressed, the content will not play.

### File Index

Create an index of the files. For this, use the separately distributed tool [mit.py](https://github.com/mmdagent-ex/index-tool-mit). After obtaining `mit.py`, you can create an index with the following command.

```shell
cd content-top
mit.py create
```

The index is created as a `.mmdagent-content-files` file at the top. This records the file names and SHA256 hashes of the files to be distributed.

## Upload

Please upload the entire content, including `PACKAGE_DESC.txt` and the index file (`.mmdagent-content-files`), to the web server.

> The web server needs to allow directory access. In other words, if you upload the entire content to a location like `https://foo.bar/some/dir`, the file `model/xxx.pmd` within the content should be directly accessible via the URL `https://foo.bar/some/dir/model/xxx.pmd`. This is because MMDAgent-EX manages the download status for each file individually. Therefore, please note that sites like Google Drive or DropBox, which generate unique download URLs for each file, cannot be used.

## Playing Content on the Web

At launch, the URL of the top directory of the web content is given as a command argument, and download and playback are performed. The URL can be specified as `https://foo.bar/some/dir` or `mmdagent://foo.bar/some/dir`.

```shell
  % ./Release/MMDAgent-EX.exe mmdagent://foo.bar/some/dir
```

Content downloaded in this way is cached to disk and launches quickly from the second time onwards. Even if the download is interrupted, it will resume from where it left off the next time the same content is launched. The cache is stored in a folder named `MMDAgent-Contents` directly under the desktop on Windows, and directly under home on macOS and Linux.

It is also possible to launch from bookmarks if you bookmark it.

### Automatic Content Updates

Web content is always synced and kept up-to-date. Web content updates are checked regularly, and when there is a difference, the difference is automatically downloaded and updated. This ensures that the web content you play is always the latest.