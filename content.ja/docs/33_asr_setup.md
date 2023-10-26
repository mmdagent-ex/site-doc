---
title: 音声認識の準備
slug: asr-setup
---
# 音声認識のセットアップ

MMDAgent-EX には、デフォルトの音声認識エンジンとして [Julius](https://julius.osdn.jp/) が組み込まれています。
Julius はローカルマシンで動く高速・簡便な音声認識エンジンです。

{{< hint warning >}}
音声認識の利用には下記の準備・設定が必要です。ビルドした直後の状態では動作しません。必ず以下のセットアップを行ってください。
{{< /hint >}}

## モデルのダウンロード

音声認識用のモデルは日本語と英語のモデルが提供されています。レポジトリに同梱されていないので、別途以下からダウンロードしてください。ダウンロードサイズは約 791 MB、展開後に 1.7GB のディスクスペースを消費します。

{{< button href="https://drive.google.com/file/d/1d82CpinrlDmY9MgjTYa-awCdLOsz16MF/view?usp=sharing" >}}Download Recent: Julius_Models_20231015.zip{{< /button >}}

{{< details "以前のバージョンのダウンロード一覧" close >}}
- [Julius_Models_20231015.zip](https://drive.google.com/file/d/1d82CpinrlDmY9MgjTYa-awCdLOsz16MF/view?usp=sharing) - 2023.10.15
{{< /details >}}

展開して中身を `Release/AppData/Julius` フォルダに置いてください。以下のようにします。

    Release/
    └── AppData/
        └── Julius/
            ├── phoneseq/
            ├── jconf_phone.txt
            ├── jconf_gmm_ja.txt
            ├── jconf_dnn_ja.txt
            ├── jconf_dnn_en.txt
            ├── dictation_kit_ja/
            └── ENVR-v5.4.Dnn.Bin/

## セットアップ

Julius で使用するモデルや言語の設定を指定する必要があります。
コンテンツの .mdf ファイルをテキストエディタで開き、以下の2行を末尾に追加してください。

{{< mdf >}}
Plugin_Julius_lang=ja
Plugin_Julius_conf=dnn
{{< / mdf >}}

- 1つ目は言語名の指定：`ja`（日本語）と`en`（英語）のどちらかを指定。
- 2つ目は設定名の指定：ja では `dnn` と `dmm` が指定可能。en では `dnn` のみ指定可能。

## 音声入力デバイスの準備

Julius は既定の音声入力デバイスを開きます。音声入力デバイスを用意して、それを規定の音声入力デバイスに設定してください。

{{< hint warning >}}
音声入力デバイスが存在しない場合は、エラーとなり起動しません。
{{< /hint >}}

## 実行テスト

上記の設定をした .mdf ファイルでコンテンツを起動します。

起動後、しばらくして画面の左下に以下のような円形メータが表示されたら起動成功です。
円の大きさは入力ボリュームを表します。

![audiometer](/images/julius_indicator_1.png)

音声入力デバイスに向かって話しかけてください。音声認識が始まると円形メータは以下のようになります。

![audiometer2](/images/julius_indicator_2.png)

デフォルトで字幕が ON になっているので、認識結果は画面に表示されます。

## しくみの解説

認識開始時に以下のイベントメッセージが流れます。

{{< message >}}
RECOG_EVENT_START
{{< / message >}}

認識終了時には以下のイベントメッセージで音声認識結果が出力されます。

{{< message >}}
RECOG_EVENT_STOP|今日はいい天気ですね
{{< / message >}}

結果を単語ごとに区切って出力したい場合は、.mdf で以下のように指定できます。

{{< mdf>}}
Plugin_Julius_wordspacing=yes
{{< / mdf >}}

- `no`: 単語間に何も入れずに詰める（`ja` 時のデフォルト）
- `yes`: 単語間に空白を入れる（`ja` 以外のデフォルト）
- `comma`: 単語間にカンマを入れる（旧MMDAgentと互換）

## 他のエンジンを使いたいとき

Julius はコンパクトなオープンソースの音声認識エンジンですが、ひと昔前の技術で作られており、モデルの性能や耐雑音性、特に雑音環境下での認識精度は最新の音声認識エンジンに劣る部分があります。

Google STT や Whisper のようなクラウド音声認識エンジンを Python でシステムを作成した場合、

- Plugin_AnyScript で MMDAgent-EX のサブモジュールとして動かす
- WebSocket 機能で別プロセスの MMDAgent-EX と外部連携させる

の2つの方法で連携できます。
