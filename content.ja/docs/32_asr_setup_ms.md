---
title: 音声認識の準備(MS)
slug: asr-setup-ms
---
{{< hint ms >}}
MS版では、MS内部向けに配布されている「京大の実環境実時間音声認識キット R2-ASR」が利用できます。
MS版では、Julius のセットアップは行わず、R2-ASR を使用してください。

このページの内容は MS 版のみの内容です。
{{< /hint >}}

# 音声認識のセットアップ (MS版)

MS向けに配布されている京大の実環境実時間音声認識キット R2-ASR を、MMDAgent-EX に組み込んで音声認識を行いましょう。

## 入手

MMDAgent-EX で R2-ASR を使うには、京大が配布しているオリジナルの R2-ASR のパッケージではなく、それを MMDAgent-EX 向けに調整したバージョンを使います。
この MMDAgent-EX向け調整済み R2-ASR は、MS版 MMDAgent-EX と同じ場所で公開されています。所定の手順に従って入手してください。

## クイックセットアップ

レポジトリ入手後、以下をシェルで実行して環境を作ります。詳細なセットアップ手順は R2-ASR の README をご覧ください。

```shell
（condaコマンドが使えなければ）minicondaをインストール
Anaconda シェルで以下を実行
% cd r2-asr
% conda env create -f env_ms_asr.yml
% conda activate ms_asr
% where python または which python で Python の実行パスを取得
```

上記のあと、Example の .mdf に以下を記述します。`/some/where/python` の部分は上記で調べた `ms_asr` 環境用の Python の実行パスに、
`/this/dir/ALL.py` は R2ASR 内の `ALL.py` へのパスにそれぞれ入れ替えてください。

{{<mdf>}}
Plugin_AnyScript_Command=/some/where/python -u /this/dir/ALL.py --vad-conf conf.vad.yml --asr-conf conf.asr.yml --input mic
{{</mdf>}}

これで Example の起動と同時にサブモジュールとして R2ASR が起動・接続し、音声認識が行えるようになります。

音声デバイスの選択等、その他の設定については、R2-ASR の README をご覧ください。

## 実行テスト

上記の設定をした .mdf ファイルで Example コンテンツを起動します。

> [ログを出力](../log/#%e3%83%ad%e3%82%b0%e3%81%ae%e5%87%ba%e5%8a%9b%e3%81%ae%e6%96%b9%e6%b3%95)することで、メッセージを実際に見て確認することができます。

音声入力を検出して認識を開始した時に、以下のメッセージが出力されます。

{{< message >}}
RECOG_EVENT_START
{{< / message >}}

認識終了後、認識結果が以下のようなメッセージで出力されます。

{{< message >}}
RECOG_EVENT_STOP|今日はいい天気ですね
{{< / message >}}

## 制御メッセージ

R2ASR は以下のメッセージを受け取ることができます。これらのメッセージを発行することで、R2ASR に対して音声認識の一時停止および再開を指示することができます。

### MSASR_DEACTIVATE

音声認識を一時停止する。

### MSASR_ACTIVATE

一時停止した音声認識を再開する。
