---
title: メニューの定義
slug: menu
---
# メニューの定義

MMDAgent-EX はメニューボタンあるいは `/` キーでメニューを出すことができます。

メッセージで新たなメニューを追加できます。コンテンツのスクリプトに仕込んでおくことで、コンテンツ固有のメニューを追加することができます。以下、メッセージによってメニューを追加・削除する方法を説明します。

## メニューに新たなページを追加する

**MENU|ADD** でメニューに新たにページを追加します。エイリアス名を新たに指定します。エイリアス名はユニークである必要があります。完了時に **MENU_EVENT|ADD** が発行されます。

{{<message>}}
MENU|ADD|(alias)
MENU_EVENT|ADD|(alias)
{{</message>}}

## ページに項目を追加する

メニューのページに「押したら特定のメッセージを発行する」項目を追加できます。追加するには
**MENU|SETITEM** を使います。`(alias)` はページ指定で、`(id)` はそのページ中で今回登録する項目の位置（一番上が 0）を指定します。`(label)` は表示テキストで、それ以降の `(type)|(arg1)|(arg2)|...` の部分で、そのメニュー項目が選択されたときに発行するメッセージを記述します。完了時に **MENU_EVENT|SETITEM** が発行されます。

{{<message>}}
MENU|SETITEM|(alias)|(id)|(label)|(type)|(arg1)|(arg2)|...
MENU_EVENT|SETITEM|(alias)|(id)
{{</message>}}

## ページの項目を削除する

追加した項目を削除するときは **MENU|DELETEITEM** を使います。完了時に **MENU_EVENT|DELETEITEM** を発行します。

{{<message>}}
MENU|DELETEITEM|(alias)|(id)
MENU_EVENT|DELETEITEM|(alias)|(id)
{{</message>}}

## ページ全体を削除する

**MENU|DELETE** でメニューの指定ページをまるごと削除します。完了時に **MENU_EVENT|DELETE** を発行します。

{{<message>}}
MENU|DELETE|(alias)
MENU_EVENT|DELETE|(alias)
{{</message>}}
