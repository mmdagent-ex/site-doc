---
title: Menu definition
slug: menu
---
# Menu definition

MMDAgent-EX can open the menu with the menu button or the `/` key.

You can add new menus via messages. By embedding them in content scripts you can add content-specific menus. Below is an explanation of how to add and remove menus via messages.

## Add a new page to the menu

Use **MENU|ADD** to add a new page to the menu. Specify a new alias name. The alias must be unique. On completion, **MENU_EVENT|ADD** is emitted.

{{<message>}}
MENU|ADD|(alias)
MENU_EVENT|ADD|(alias)
{{</message>}}

## Add an item to a page

You can add an item to a menu page that emits a specific message when selected. Use **MENU|SETITEM** to add it. `(alias)` specifies the page, `(id)` specifies the position of the item in that page (topmost is 0). `(label)` is the display text, and the following `(type)|(arg1)|(arg2)|...` fields describe the message that will be sent when the menu item is selected. On completion, **MENU_EVENT|SETITEM** is emitted.

{{<message>}}
MENU|SETITEM|(alias)|(id)|(label)|(type)|(arg1)|(arg2)|...
MENU_EVENT|SETITEM|(alias)|(id)
{{</message>}}

## Delete an item from a page

Use **MENU|DELETEITEM** to delete an item you previously added. On completion, **MENU_EVENT|DELETEITEM** is emitted.

{{<message>}}
MENU|DELETEITEM|(alias)|(id)
MENU_EVENT|DELETEITEM|(alias)|(id)
{{</message>}}

## Delete an entire page

Use **MENU|DELETE** to remove an entire page from the menu. On completion, **MENU_EVENT|DELETE** is emitted.

{{<message>}}
MENU|DELETE|(alias)
MENU_EVENT|DELETE|(alias)
{{</message>}}