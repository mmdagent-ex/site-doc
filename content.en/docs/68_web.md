---
title: Publishing Content on the Web
slug: web-content
---
# Publishing content on the Web

You can publish content on a web server so that MMDAgent-EX can download and play it directly. By specifying a URL, the content can be downloaded and played, and it can be automatically synchronized with the server's content.

Publishing MMDAgent-EX content on the web requires several preparatory steps. Below are the steps from preparing the content for publication to how to use it.

{{< hint warning >}}
Distributing content to others constitutes **secondary distribution (redistribution) of files**. Pay attention to the terms of use for files and materials included in the content.
{{< /hint >}}

## Preparing for distribution

### PACKAGE_DESC.txt

Place a package configuration file named `PACKAGE_DESC.txt` in the content's top-level folder. The [detailed format](../package-desc-format) aside, at minimum include the following settings.

```text
execMDFFile=some/where/foobar.mdf
label=string
image=hoge.png
readme=readme.txt
readmeForceAgreement=true
```

- **execMDFFile**: The .mdf file to launch. Required.
- **label**: The content name. If not specified, the .mdf filename is used. If set to "`label=`" (empty), no label is displayed.
- **image**: Path to an image file used when displaying the content in menus. Defaults to `banner.png` if not specified. If the file doesn't exist, no image is used. A 7:1 aspect ratio is recommended.
- **readme**: Path to a README text file you want users to read first. If specified, it will be shown fullscreen on the first launch of the content. Must be UTF-8.
- **readmeForceAgreement**: If true, two buttons — `Accept` and `Decline` — are shown at the bottom after displaying the README. If `Decline` is pressed, the content will not play.

### File index

Create an index of the files. Use the separately distributed tool [mit.py](https://github.com/mmdagent-ex/index-tool-mit). After obtaining `mit.py`, create the index with the following command:

```shell
cd content-top
mit.py create
```

The index is created at the top level as a `.mmdagent-content-files` file. It records the filenames and SHA256 hashes of the files to be distributed.

## Upload

Upload the entire content, including `PACKAGE_DESC.txt` and the index file (`.mmdagent-content-files`), to a web server.

> The web server must allow direct directory access. That is, if you upload the content to `https://foo.bar/some/dir`, a file inside the content like `model/xxx.pmd` must be directly accessible at `https://foo.bar/some/dir/model/xxx.pmd`. MMDAgent-EX manages download status per file, so this is required. Therefore, services that generate unique download URLs per file, such as Google Drive or DropBox, cannot be used.

## Play content hosted on the web

At startup, provide the URL of the web content's top directory as a command-line argument to download and play it. The URL can be `https://foo.bar/some/dir` or specified like `mmdagent://foo.bar/some/dir`.

```shell
  % ./Release/MMDAgent-EX.exe mmdagent://foo.bar/some/dir
```

Content downloaded this way is cached on disk and will start faster on subsequent runs. If a download is interrupted, it will resume from where it left off the next time the same content is launched. The cache is placed under a folder named `MMDAgent-Contents`: directly on the desktop on Windows, and directly in the home directory on macOS and Linux.

If bookmarked, it can also be launched from the bookmarks.

### Automatic content updates

Web content is kept synchronized and up to date. Updates to web content are checked periodically, and when differences are found, only the changed parts are downloaded and updated automatically. This ensures that web-hosted content you play is always current.