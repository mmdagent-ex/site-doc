---
title: 3Dモデルの表示
slug: 3d-model
---
# 3Dモデルの表示

MikuMikuDance の3-Dモデル形式である .pmd フォーマットを採用しており、人型モデルを含む任意の .pmd 形式のオブジェクトを表示できます。また、[PMX モデルも変換によって表示することができます](../pmx)。

## モデルの表示・削除

シーン内には複数のモデルを表示できます。シーンへのモデルの追加・入れ替え・削除はメッセージで行います。

{{< details "同時に表示できるモデルは最大で10個です。" close >}}
足りない場合は .mdf で以下のように上限数を設定してください。
{{< mdf>}}
max_num_model=20
{{< /mdf>}}
{{< /details >}}

### モデルをシーンに追加

**MODEL_ADD** メッセージを使ってモデルをロードし、シーン内に新たに追加表示します。以下の例の `agent1` の部分は、あとでこの読み込まれたモデルを参照するためのエイリアス名（モデルエイリアス）です。

{{<message>}}
MODEL_ADD|agent1|some/where/model.pmd
{{</message>}}

モデルの表示位置や向きを引数で指定できます。例えば座標 (8,0,0) に Y 軸まわりに30度回転させる場合は以下のように指定します。デフォルトはシーン原点 (0,0,0) 上、正面向きです。

{{<message>}}
MODEL_ADD|agent1|some/where/model.pmd|8,0,0|0,30,0
{{</message>}}

表示に成功したら以下のような　**MODEL_EVENT_ADD** イベントメッセージが発行されます。これを監視することで各種モジュールはモデルの表示が開始されたこととそのモデルエイリアス名を検知できます。

{{<message>}}
MODEL_EVENT_ADD|agent1
{{</message>}}

### 入れ替え

動作中のモデルと同じエイリアス名で `MODEL_ADD` するとエラーになります。表示中モデルの .pmd を入れ替える場合は **MODEL_CHANGE** メッセージを使います。

{{<message>}}
MODEL_CHANGE|agent1|some/where/other.pmd
{{</message>}}

成功したら以下のような　**MODEL_EVENT_CHANGE** イベントメッセージが発行されます。各種モジュールはこのメッセージで表示モデルが変更・更新されたことを検知できます。

{{<message>}}
MODEL_EVENT_CHANGE|agent1
{{</message>}}

### 削除

動作中のモデルを削除するには **MODEL_DELETE** を使います。

{{<message>}}
MODEL_DELETE|(model alias)
{{</message>}}

成功時には以下のような　**MODEL_EVENT_DELETE** イベントメッセージが発行されます。各種モジュールは、このメッセージでモデルがシーンから削除されたことを検知できます。

{{<message>}}
MODEL_EVENT_CHANGE|agent1
{{</message>}}

## 他のモデルにマウントする

`MODEL_ADD` ではモデルをグローバル座標上に置きますが、代わりに別のモデルにマウントさせることもできます。マウントされたモデルは、マウント先の動作に追従して動くようになります。これは、キャラクターにアクセサリを載せる場合等に使うことができます。例えば obj.pmd というモデルを `agent1` の `頭` ボーンにマウント表示するには、以下のようなメッセージを発行します。

{{<message>}}
MODEL_ADD|object1|/some/where/obj.pmd|0,0,0|0,0,0|ON|agent1|頭
{{</message>}}

なお、マウント指定時は `MODEL_ADD` で指定した座標および回転量は、グローバル座標ではなくマウント先ボーンを起点とした相対座標（ローカル座標）で扱われます。

## 設定パラメータ

モデル表示に関連する主な .mdf の設定項目を列挙します。

- ロード時にモデルの内部コメントを表示するときの持続時間（秒）。0で表示しない。

{{< mdf>}}
display_comment_time=0
{{< /mdf>}}

- シーン内に表示できるモデル数の最大値。最小は1、最大は1024。デフォルトは10。

{{< mdf>}}
max_num_model=10
{{< /mdf>}}

- アンチエイリアス (MSAA) の強度。大きいほど線が滑らかに表示される。0でOFFにする。デフォルトは 4。

{{< mdf>}}
max_multi_sampling=4
{{< /mdf>}}

- トゥーンエッジの太さ

（`K`, `Shift+K` でも変更可能）

![bold edge](/images/edge1.png)
![thin edge](/images/edge2.png)

{{< mdf>}}
cartoon_edge_width=0.35
{{< /mdf>}}

## モデルロード時・削除時メッセージ

モデルがロードされたとき、あるいは削除されたときに特定のメッセージをシステムへ発行するよう仕込むことができます。これを使うことで、例えば「モデルをロードしたときにメニューやボタンを追加する」「モデルをロードしたとき同時に背景も替える」といった処理をモデル側の指示として行うことができます。

モデル名 `xxx.pmd` に対して、`xxx.pmd.loadmessage` というテキストファイルを作り、その中に、1行1つずつメッセージを記述しておきます。そうすることで、このモデル `xxx.pmd` がロードされる際に、ロード直後に `xxx.pmd.loadmessage` の中に記述されているメッセージが順に実行されます。

同様に、`xxx.pmd.deletemessage` を記述することで、モデルが削除されたときに発行するメッセージを指定できます。

例が Example の「ジェネ」のモデルにあります。この `Gene.pmd.loadmessage` では、ジェネのモデルをロードした際に、アクセサリの ON/OFF を行うメニューを追加するように書かれています。

```text
MENU|ADD|Gene
MENU|SETITEM|Gene|0|頬なし|MODEL_BINDFACE|0|頬全消し|1
MENU|SETITEM|Gene|1|頬あり|MODEL_BINDFACE|0|頬全消し|0
MENU|SETITEM|Gene|2|メッシュなし|MODEL_BINDFACE|0|メッシュなし|1
MENU|SETITEM|Gene|3|メッシュあり|MODEL_BINDFACE|0|メッシュなし|0
MENU|SETITEM|Gene|4|髪留なし|MODEL_BINDFACE|0|髪留なし|1
MENU|SETITEM|Gene|5|髪留あり|MODEL_BINDFACE|0|髪留なし|0
```