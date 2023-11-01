---
title: メニューの定義
slug: menu
---
# メニューの定義

## メニュー追加

**MENU|ADD**

メニューに新たにページを追加する。デフォルトと合わせて最大20ページまで可能。追加完了時に **MENU_EVENT|ADD** を発行する。

```text
MENU|ADD|(alias)
MENU|ADD|(alias)|backgroundImagePath
MENU_EVENT|ADD|(alias)
```

**MENU|SETITEM**

メニューの指定ページの指定位置に項目を登録する。`id` は0から始まる項目番号。1ページあたり項目は30個まで登録可能。登録完了後に **MENU_EVENT|SETITEM** を発行する。

```text
MENU|SETITEM|(alias)|(id)|(label)|(type)|(arg1)|(arg2)|...
MENU_EVENT|SETITEM|(alias)|(id)
```

**MENU|DELETEITEM**

メニューの指定ページの指定位置の項目内容を削除する。削除完了時に **MENU_EVENT|DELETEITEM** を発行する。

```text
MENU|DELETE|(alias)
MENU_EVENT|DELETE|(alias)
```

**MENU|DELETE**

メニューの指定ページをまるごど削除する。削除完了時に **MENU_EVENT|DELETE** を発行する。

```text
MENU|DELETEITEM|(alias)|(id)
MENU_EVENT|DELETEITEM|(alias)|(id)
```
