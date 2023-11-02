---
title: パラメータの設定
slug: mdf-basic
---
# パラメータの設定

様々な設定を .mdf ファイルで指定できます。

.mdf ファイルは、コンテンツ再生の起点となるファイルです。コンテンツの .mdf ファイルに記述した設定は、そのコンテンツを実行するときに読まれます。

また、MMDAgent-EX 実行ファイルと同じフォルダにあるシステム設定ファイル `MMDAgent-EX.mdf` は、起動時にデフォルト設定として読み込まれます。指定が重なる場合はコンテンツ側が優先されるので、コンテンツの .mdf に設定を記述すればデフォルト値はオーバーライドされます。

なお、ファイル中では環境編素 `％ENV{環境変数名}` の形で参照することができます。コンテンツ起動時に、この部分はその環境変数の値に入れ替えて解釈されます。

## サンプル

.mdf ファイルのサンプル例です。設定できる値は多岐にわたります。詳細は、 [mdfパラメータの一覧](../mdf) を見てください。

{{< mdf>}}
# ログを保存するファイル名
log_file=
# 指定したプラグイン以外を無効化
disablePlugin=ALL
enablePlugin=Audio,VIManager

# ウィンドウの初期サイズ（横,縦）
window_size=600,600
# trueで起動時にフルスクリーン化
full_screen=false
# 左上の状態表示
show_fps=true
# アンチエイリアス強度
max_multi_sampling=4
# ステージサイズ
stage_size=25.0,25.0,40.0

# 音声認識(Julius)
Plugin_Julius_conf=dnn
Plugin_Julius_lang=ja
show_caption=true
{{< /mdf>}}
