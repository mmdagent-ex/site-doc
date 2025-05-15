---
headless: true
---

- [MMDAgent-EXとは]({{< relref "/docs/about" >}})
- [ライセンス・ガイドライン]({{< relref "/docs/license_and_guideline" >}})
<br />

- **チュートリアル**
- [入手およびビルド]({{< relref "/docs/00_build" >}})
- [Exampleの実行テスト]({{< relref "/docs/05_run_contents" >}})
- [画面]({{< relref "/docs/10_screen" >}})
- [基本操作]({{< relref "/docs/15_keybinds_basic" >}})
- [ログの表示]({{< relref "/docs/17_log" >}})
- [音声合成を試す]({{< relref "/docs/20_tts_test" >}})
- [[MS]音声認識のセットアップ]({{< relref "/docs/32_asr_setup_ms" >}})
- [音声対話を試す (fst)]({{< relref "/docs/34_dialog_fst" >}})
- [音声対話を試す (Python)]({{< relref "/docs/36_dialog_python" >}})
- [ChatGPTと繋ぐ]({{< relref "/docs/37_dialog_chatgpt" >}})
- [CGアバターを変える]({{< relref "/docs/38_change_model" >}})
- [.mdf 設定ファイル]({{< relref "/docs/41_mdf_basic" >}})
- [[MS]仮想Webカメラで配信]({{< relref "/docs/39_webcam" >}})
<br />

- **コンテンツ作成**
- [メッセージの単独実行]({{< relref "/docs/40_test_message" >}})
- [3Dモデル]({{< relref "/docs/43_3dmodel" >}})
  - [表示・削除・入れ替え]({{< relref "/docs/43_3dmodel#モデルの表示削除" >}})
  - [マウント]({{< relref "/docs/43_3dmodel#他のモデルにマウントする" >}})
  - [設定]({{< relref "/docs/43_3dmodel#設定パラメータ" >}})
  - [ロード時・削除時実行]({{< relref "/docs/43_3dmodel#設定パラメータ" >}})
  - [PMXモデルの利用手順]({{< relref "/docs/45_pmx" >}})
  - [エフェクト]({{< relref "/docs/46_effect" >}})
- [モデル動作の仕組み]({{< relref "/docs/47_motion#動作制御の仕組み" >}})
- [値をセット]({{< relref "/docs/52_motion_bind" >}})
  - [ボーン]({{< relref "/docs/52_motion_bind#model_bindbone" >}})
  - [モーフ]({{< relref "/docs/52_motion_bind#model_bindface" >}})
- [モーション制御]({{< relref "/docs/47_motion" >}})
  - [再生・終了・中断]({{< relref "/docs/48_motion_play" >}})
  - [入替・巻戻し]({{< relref "/docs/48_motion_play#別のモーションに入れ替える" >}})
  - [複数の重ね合わせ]({{< relref "/docs/49_motion_layer" >}})
    - [仕組みとデモ]({{< relref "/docs/49_motion_layer" >}})
    - [部分再生]({{< relref "/docs/49_motion_layer#部分モーション指定" >}})
    - [ループ再生]({{< relref "/docs/49_motion_layer#ループ再生指定" >}})
    - [スムージング切替]({{< relref "/docs/49_motion_layer#スムージングを切り替える" >}})
  - [ブレンド設定]({{< relref "/docs/50_motion_blend" >}})
    - [加算重ね・乗算重ね]({{< relref "/docs/50_motion_blend#上書き加算乗算" >}})
    - [ブレンド率]({{< relref "/docs/50_motion_blend#上書き加算乗算" >}})
- [タイマー]({{< relref "/docs/54_timer" >}})
- [視点（カメラ）]({{< relref "/docs/55_camera" >}})
- [背景・床]({{< relref "/docs/62_scene" >}})
- [画面フレーム]({{< relref "/docs/62_scene#画面フレーム" >}})
- [オーディオ再生]({{< relref "/docs/58_sound" >}})
  - [準備]({{< relref "/docs/58_sound#準備" >}})
  - [サウンド再生]({{< relref "/docs/58_sound#サウンド再生" >}})
  - [音声再生（リップ付き）]({{< relref "/docs/58_sound#音声再生-with-リップシンク" >}})
- [画像・テキスト]({{< relref "/docs/60_text_image" >}})
  - [3D空間内へ表示]({{< relref "/docs/60_text_image#画像テキストの3d空間内表示-textarea" >}})
  - [キャプション表示]({{< relref "/docs/60_text_image#テキストキャプション表示" >}})
  - [選択肢の提示]({{< relref "/docs/61_text_prompt" >}})
  - [テキストファイル表示]({{< relref "/docs/63_text_document" >}})
  - [文字列の表示]({{< relref "/docs/63_text_document#文字列をドキュメント表示" >}})
- [カスタムメニュー]({{< relref "/docs/64_menu" >}})
- [カスタムボタン]({{< relref "/docs/65_buttons" >}})
- [Webでコンテンツを配信する]({{< relref "/docs/68_web" >}})
<br />

- **開発・拡張**
- [ソケット接続による外部制御]({{< relref "/docs/71_remote" >}})
  - [WebSocket]({{< relref "/docs/72_remote_websocket" >}})
  - [TCP/IP]({{< relref "/docs/73_remote_tcpip" >}})
- [モジュールの追加]({{< relref "/docs/70_submodule" >}})
- [音声のストリーミング]({{< relref "/docs/74_remote_speech" >}})
- [リップシンク指定]({{< relref "/docs/74_remote_speech#方法３口パクさせる" >}})
- [パラメータの外部化]({{< relref "/docs/75_global_variables" >}})
- [パラメータとモーフのリンク]({{< relref "/docs/75_global_variables#model_bindface-でバインド" >}})
- [[MS]外部API]({{< relref "/docs/77_api" >}})
- [[MS]shapemap]({{< relref "/docs/78_shapemap" >}})
<br />

- **リファレンス**
- [メッセージ一覧]({{< relref "/docs/86_messages" >}})
- [mdf 設定項目一覧]({{< relref "/docs/85_mdf" >}})
- [環境変数一覧]({{< relref "/docs/81_environmental_variables" >}})
- [キー・マウス操作一覧]({{< relref "/docs/80_keybinds" >}})
- [FST の書式解説]({{< relref "/docs/88_fst" >}})
- [PACKAGE_DESC.txt 書式]({{< relref "/docs/95_package_desc" >}})
- [オリジナルとの違い]({{< relref "/docs/99_changes" >}})
<br />

- **関連リンク**
- [Twitter @MMDAgentEX](https://twitter.com/MMDAgentEX)
