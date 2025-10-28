---
title: Prompt Responses
slug: prompting
---
# Prompt Responses

In voice-interaction systems, communication is mainly via speech and gestures, but when presenting choices or having the user explicitly select what they want, touch (or mouse clicks) can also be an effective input modality.

MMDAgent-EX can display arbitrary message dialogs. You can simply show a message and dismiss it with an external tap, or present choices to the user and receive one of their selection responses.

You can use this to get user reactions or branch processing based on their choice.

## PROMPT_SHOW

To display a prompt, send the **PROMPT_SHOW** message. `(main text)` is the description, and `item text 0`, `item text 1`, ... are the choices. You can use `""` and `\n` in each text.

{{<message>}}
PROMPT_SHOW|(main text)|(item text 0)|(item text 1)|...
{{</message>}}

Example:

{{<message>}}
PROMPT_SHOW|"main text"|item1|item2|item3
{{</message>}}

![prompt](/images/prompt.png)

When you send **PROMPT_SHOW**, the prompt shown above will appear. The system continues running in the background while the prompt is displayed.

The user selects an item by key or tap, or cancels by tapping outside the dialog. The prompt then disappears and **PROMPT_EVENT_SELECTED** is sent with the number of the selected item (0-based; -1 for cancel).

{{<message>}}
PROMPT_EVENT_SELECTED|(selected number or -1 for cancel)
{{</message>}}