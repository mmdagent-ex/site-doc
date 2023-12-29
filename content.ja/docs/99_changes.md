---
title: オリジナルのMMDAgentからの変更点
slug: changes-since-original-mmdagent
---
# オリジナルの MMDAgent からの変更点

[MMDAgent](https://www.mmdagent.jp/) から MMDAgent-EX の主な変更点をまとめます。

### 表示

- メニューの追加
- [下部タブバー](../screen)
- [詳細なログ表示](../log/) (`Shift+f`)
- [エラーがスクリーン上に常時表示されるように](../screen)

### 機能

- コンテンツ再生履歴（`Shift+H`）
- エディタでFSTを開く（`E`: Windowsのみ）
- エクスプローラでフォルダを開く（`Shift+E`: Windowsのみ）
- スクショ（`Shift+G`）
- マウスで視点変更：デフォルトでOFF（`c` キーで切替）
- カメラリセット（`Shift+C`）

### ポストエフェクト

- AutoLuminousエフェクト（`Shift+L` で強度調整）
- Diffusionエフェクト（`O`キーと`I`キーで強度調整、Windowsのみ）
- 二重影効果（`Shift+J`）

### 3Dモデル

- [PMXモデルのサポートと互換性の改善](../pmx/)
- [モーション間のブレンディング機能の強化](../motion-layer/)
- アニメーションPNG対応

### FST拡張

[FSTの書式を拡張](../fst-format/)（旧書式もそのまま利用可能）

- ブロック定義
- 正規表現
- ローカル変数 初期値
- グローバル変数(KeyValue)へのアクセス
- 環境変数へのアクセス
- VS Code 用拡張

### 音声認識

- 性能改善：エンジン・音響モデル・言語モデルを DNN ベースの最新版に更新
- 日本語に加えて英語モデルの提供

### マルチモーダル

- [画像・テキストの表示機能を強化](../image-and-text/)

### 外部連携

- [任意プログラムを組み込むプラグイン Plugin_AnyScript の追加](../submodule/)
- [外部音声を再生する機能の強化](../remote-speech/)
- [ソケット接続の改善](../remote-control/)
  - [WebSocket接続をサポート](../remote-websocket/)
- [モーフ単位の外部制御](../motion-bind/)

### mdfやメッセージの拡張

多くの設定やメッセージが追加されました。

- [mdfの設定項目一覧](../mdf/)
- [メッセージの一覧](../messages/)

### その他

- [Webコンテンツ](../web-content/)

詳しくは各ドキュメントを見てください。
