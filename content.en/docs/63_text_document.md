

---
title: Document Display
slug: text-document
---

# Document Display

You can display long text documents in full screen. Users can scroll through and read the text. You can also attach buttons to capture user reactions. While displaying, you cannot cancel until you press a button, and most other screen operations cannot be performed. This can be used to present content that the user must read, such as having them read the content's README, terms of service, etc.

## Displaying Text Files as Documents

You can display the contents of a text file as a document. Use the **INFOTEXT_FILE** message as follows. The fourth argument and beyond can be omitted.

- First argument: Path of the text file
- Second argument: Title label
- Third argument: Selection button labels - separated by commas. Example: "Yes,No,Cancel"
- Fourth argument (optional): Character scale (default: 1.0)
- Fifth argument (optional): Background color - in hexadecimal "RRGGBBAA". Example: White=FFFFFFFF
- Sixth argument (optional): Text color - same as above

{{<message>}}
INFOTEXT_FILE|(filepath)|(titleLabel)|(buttonLabels)|(scale)|(BACKGROUNDCOLOR)|(TEXTCOLOR)
{{</message>}}

Example: Display README.txt

{{<message>}}
INFOTEXT_FILE|README.txt|"read me"|OK,NO
{{</message>}}

![infotext](/images/infotext.png)

When the display starts, an **INFOTEXT_EVENT_SHOW** message is issued.

{{<message>}}
INFOTEXT_EVENT_SHOW
{{</message>}}

The display ends when the user selects one of the selection button labels. At that time, **INFOTEXT_EVENT_CLOSE** is issued along with the label of the button that was pressed.

{{<message>}}
INFOTEXT_EVENT_CLOSE|(selectedButtonLabel)
{{</message>}}

## Displaying Strings as Documents

You can also specify the content to be displayed with a message instead of a file. Use the **INFOTEXT_STRING** message instead of **INFOTEXT_FILE**. Specify the string you want to display directly in the first argument. The method of specifying the second argument and beyond is exactly the same as **INFOTEXT_FILE**.

{{<message>}}
INFOTEXT_STRING|textbody|(titleLabel)|(buttonLabels)|(scale)|(BACKGROUNDCOLOR)|(TEXTCOLOR)
{{</message>}}

As with **INFOTEXT_FILE**, an **INFOTEXT_EVENT_SHOW** message is issued when the display starts, and an **INFOTEXT_EVENT_CLOSE** message is issued when it ends.