---
title: 音声認識の準備
slug: asr-setup
---
# 音声認識のセットアップ

MMDAgent-EX には、デフォルトの音声認識エンジンとして [Julius](https://julius.osdn.jp/) が組み込まれています。
Julius はローカルマシンでCPUのみで動く高速・簡便な音声認識エンジンです。

{{< hint warning >}}
音声認識の利用には下記の準備・設定が必要です。ビルドした直後の状態では動作しません。必ず以下のセットアップをコンテンツごとに行ってください。
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

Julius で使用するモデルや言語の設定を .mdf で指定する必要があります。日本語の音声認識を使う場合、Example の中の main.mdf ファイルをテキストエディタで開き、以下の2行を末尾に追加してください。

{{< mdf >}}
Plugin_Julius_lang=ja
Plugin_Julius_conf=dnn
{{< / mdf >}}

- 1つ目は言語名の指定：`ja`（日本語）と`en`（英語）のどちらかを指定。
- 2つ目は設定名の指定：ja では `dnn` と `dmm` が指定可能。en では `dnn` のみ指定可能。

## 音声入力デバイスの準備

音声認識モジュールは既定のサウンド入力デバイスを開いて音声認識を行います。音声入力デバイスを用意して、それを規定の音声入力デバイスに設定してください。

{{< hint warning >}}
音声入力デバイスが存在しない場合は、エラーとなり起動しません。
{{< /hint >}}

## 実行テスト

上記の設定をした .mdf ファイルで Example コンテンツを起動します。

起動後、しばらくして画面の左下に以下のような円形メータが表示されたら起動成功です。
円の大きさは入力ボリュームを表します。

![audiometer](/images/julius_indicator_1.png)

音声入力デバイスに向かって話しかけてください。音声認識が始まると円形メータは以下のようになります。

![audiometer2](/images/julius_indicator_2.png)

音声認識結果は画面に字幕で表示されます。

![result](/images/asr_test_ja.png)

## しくみの解説

音声認識モジュールの動作内容は内部にメッセージとして送信されます。認識開始時には以下のメッセージが音声認識モジュールから出力されます。

> [ログを出力](../log/#%e3%83%ad%e3%82%b0%e3%81%ae%e5%87%ba%e5%8a%9b%e3%81%ae%e6%96%b9%e6%b3%95)することで、メッセージを実際に見て確認することができます。


{{< message >}}
RECOG_EVENT_START
{{< / message >}}

認識結果は、認識終了時に以下のようなメッセージで出力されます。

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

字幕の表示をOFFにすることができます。OFFにするには、以下の1行を main.mdf に設定してください。

{{<mdf>}}
show_caption=false
{{</mdf>}}

## 他のエンジンを使いたいとき

Julius はコンパクトなオープンソースの音声認識エンジンですが、ひと昔前の技術で作られており、モデルの性能や耐雑音性、特に雑音環境下での認識精度は最新の音声認識エンジンに劣る部分があります。

Google STT や Whisper のようなクラウド音声認識エンジンを Python でシステムを作成した場合、

- Plugin_AnyScript で MMDAgent-EX のサブモジュールとして動かす
- WebSocket 機能で別プロセスの MMDAgent-EX と外部連携させる

の2つの方法で連携できます。
