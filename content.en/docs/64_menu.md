

---
title: Defining Menus
slug: menu
---

# Defining Menus

MMDAgent-EX allows you to display a menu either by pressing the menu button or the `/` key.

You can add new menus through messages. By incorporating it into the content script, you can add content-specific menus. Below, we'll explain how to add and remove menus through messages.

## Adding a New Page to the Menu

You can add a new page to the menu with **MENU|ADD**. You need to specify a new alias name, which needs to be unique. When completed, **MENU_EVENT|ADD** is issued.

{{<message>}}
MENU|ADD|(alias)
MENU_EVENT|ADD|(alias)
{{</message>}}

## Adding an Item to a Page

You can add an item to a menu page that issues a specific message when pressed. Use **MENU|SETITEM** to add it. `(alias)` specifies the page, while `(id)` specifies the position of the item to register in that page (where the top is 0). `(label)` is the display text, and the `(type)|(arg1)|(arg2)|...` part describes the message to be issued when that menu item is selected. When completed, **MENU_EVENT|SETITEM** is issued.

{{<message>}}
MENU|SETITEM|(alias)|(id)|(label)|(type)|(arg1)|(arg2)|...
MENU_EVENT|SETITEM|(alias)|(id)
{{</message>}}

## Deleting an Item from a Page

Use **MENU|DELETEITEM** when you want to remove an added item. When completed, **MENU_EVENT|DELETEITEM** is issued.

{{<message>}}
MENU|DELETEITEM|(alias)|(id)
MENU_EVENT|DELETEITEM|(alias)|(id)
{{</message>}}

## Deleting an Entire Page

You can delete an entire specified page from the menu with **MENU|DELETE**. When completed, **MENU_EVENT|DELETE** is issued.

{{<message>}}
MENU|DELETE|(alias)
MENU_EVENT|DELETE|(alias)
{{</message>}}