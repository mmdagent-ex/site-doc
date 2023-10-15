---
title: 音声認識の準備
slug: asr-setup
---

デフォルトの音声認識エンジンとして Juliusが組み込まれています。
Julius はローカルマシン上で高速・簡便な音声認識を提供します。

音声認識の利用には下記の準備・設定が必要です。ビルドした直後の状態では動作しません。必ず以下のセットアップを行ってください。

## モデルのダウンロード

音声認識用モデルを以下からダウンロードしてください。日本語と英語のモデルが含まれています。
ダウンロードサイズは約 809 MBで、展開後に 1.7GB のディスクスペースを消費します。

- [Julius_Models_20231015.zip](https://drive.google.com/file/d/1d82CpinrlDmY9MgjTYa-awCdLOsz16MF/view?usp=sharing)

{{< details "以前のバージョンのダウンロード一覧" close >}}
- [Julius_Models_20231015.zip](https://drive.google.com/file/d/1d82CpinrlDmY9MgjTYa-awCdLOsz16MF/view?usp=sharing) - 2023.10.15
{{< /details >}}

ダウンロード後、展開して中身を `Release/AppData/Julius` フォルダに置いてください。以下のようにします。

```text
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
```

## セットアップ

コンテンツの .mdf に以下を追加。以下の2つの必須項目を指定することで音声認識が起動する。

```text
Plugin_Julius_conf=dnn
Plugin_Julius_lang=en
```

- 1つ目は設定名：日本語は `dnn` と `dmm`、英語は `dnn` のみ。
- 2つ目は言語名：現在のところ ja と en。

## 実行とテスト

コンテンツを起動後しばらくして左下に円形のメータが表示されたら成功。以降音声認識が利用可能。

認識結果は `RECOG_EVENT_STOP` で出る。なるべく静かな部屋で試すこと。

```text
RECOG_EVENT_STOP|今日はいい天気ですね
```

## 他のエンジンを使いたいとき

Julius はコンパクトなオープンソースの音声認識エンジンですが、ひと昔前の技術で作られており、モデルの性能や耐雑音性、特に雑音環境下での認識精度は最新の音声認識エンジンに劣る部分があります。

Google STT や Whisper のようなクラウド音声認識エンジンを Python でシステムを作成した場合、

- Plugin_AnyScript で MMDAgent-EX のサブモジュールとして動かす
- WebSocket 機能で別プロセスの MMDAgent-EX と外部連携させる

の2つの方法で連携できます。
