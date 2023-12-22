

---
title: Responding to Prompts
slug: prompting
---

# Responding to Prompts

In voice interaction systems, communication is predominantly achieved through voice and gestures. However, in instances where options are presented and the user is explicitly asked to make a choice, touch (mouse click) can also serve as an effective modality.

With MMDAgent-EX, you can display any message dialog. You can simply display a message and end it with an external tap, or present options to the user and receive a selection response.

This feature can be used to garner responses from the user or to branch the process based on the selection.

## PROMPT_SHOW

To display a prompt, you issue a **PROMPT_SHOW** message. `(main text)` is the description, and `item text 0`, `item text 1`, ... are the options. You can use `""` or `\n` to specify each text.

{{<message>}}
PROMPT_SHOW|(main text)|(item text 0)|(item text 1)|...
{{</message>}}

Example:

{{<message>}}
PROMPT_SHOW|"main text"|item1|item2|item3
{{</message>}}

![prompt](/images/prompt.png)

When you issue **PROMPT_SHOW**, the prompt display begins as shown above. The system continues to operate in the background while the prompt is displayed.

Users can select an item by key or tap, or cancel by tapping outside the dialog. Afterwards, the prompt disappears, and **PROMPT_EVENT_SELECTED** is issued along with the number of the selected item (0 onwards, -1 for cancel).

{{<message>}}
PROMPT_EVENT_SELECTED|(selected number or -1 for cancel)
{{</message>}}