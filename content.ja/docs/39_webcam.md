---
title: 仮想Webカメラで配信(MS)
slug: webcam
---
{{< hint ms >}}
このページの内容は MS 版のみの内容です。
{{< /hint >}}

# 仮想Webカメラで配信する

仮想Webカメラで MMDAgent-EX の画面を配信できます。現時点で対応OSはWindowsのみです。

仮想Webカメラとして Softcam を利用しています。

- https://github.com/tshino/softcam

## インストール

[Softcam](https://github.com/tshino/softcam) のドライバーを実行マシンにインストールします。ソースコードの `Plugin_Webcam/softcam` フォルダにインストーラーが同梱されているので、その中の `RegisterSoftcam.bat` を実行してください（OSが 32bit の場合は 32bit 版をインストール）

- `RegisterSoftcam.bat`: 64bit 版インストーラ（通常はこちら）
- `RegisterSoftcam32.bat`: 32bit 版インストーラ

インストール後、Webカメラの選択肢に "`DirectShow Softcam`" が出てくるはずです。出てこない場合はアプリやブラウザを再起動してください。

## 使い方

MMDAgent-EX を起動して画面を出したあと、`WEBCAM_START` メッセージを発行することでキャストが開始されます。

{{<message>}}
WEBCAM_START
{{</message>}}

開始後、アプリ等で Webカメラに `DirectShow softcam` を選ぶことで、MMDAgent-EX の画像を Webカメラ映像として送信・処理等行えます。

キャストされるのは MMDAgent-EX ウィンドウ内の左上からの固定されたサイズの区域（デフォルト 1280 x 720）です。キャストしたい内容が映るよう、ウィンドウの大きさを手動等で適宜調整してください。

キャストを終了するときは `WEBCAM_STOP` メッセージを発行します。

{{<message>}}
WEBCAM_STOP
{{</message>}}

## 起動直後からキャストする

.mdf に以下を書いておくことで、起動した直後から自動でキャストを開始させることができます。

{{< mdf>}}
Webcam_Enable=true
{{< /mdf>}}

## 画面範囲を変更

MMDAgent-EX内のキャストする画面の範囲を変更するには .mdf で幅 `Webcam_Width` と高さ`Webcam_Height` を指定します。デフォルト値はそれぞれ 1280 と 720 です。たとえば 640x360にしたい場合は以下のようにします。なお変更できるのは幅と高さだけで、起点はウィンドウ左上で固定です。

{{< mdf>}}
Webcam_Width=640
Webcam_Height=360
{{< /mdf>}}

キャプチャされた画像はドライバー側で仮想Webカメラで指定された解像度（1280x720 とか 640x360）に伸長されてキャストされます。上記で大きい範囲を指定するほど、画質はよくなりますがソフトウェアキャプチャなのでCPUの負担が大きくなります。小さい範囲にすれば負荷は下がりますが、画質が荒くなります。
