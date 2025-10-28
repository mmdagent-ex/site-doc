---
title: Document Display
slug: text-document
---
# Document Display

You can show long text documents in a full-screen view. Users can scroll through the text to read it. You can also add buttons to capture user reactions. While the document is displayed it cannot be canceled until a button is pressed, and most other screen operations are disabled. This is useful for presenting content the user must read, such as a README or terms of service.

## Displaying a Text File

You can display the contents of a text file as a document. Use the **INFOTEXT_FILE** message as shown below. Arguments from the 4th onward are optional.

- 1st argument: path to the text file
- 2nd argument: title label
- 3rd argument: selection button labels, separated by commas. Example: "Yes,No,Cancel"
- 4th argument (optional): text scale (default: 1.0)
- 5th argument (optional): background color in 8-digit hex "RRGGBBAA", e.g. white = FFFFFFFF
- 6th argument (optional): text color, same format

{{<message>}}
INFOTEXT_FILE|(filepath)|(titleLabel)|(buttonLabels)|(scale)|(BACKGROUNDCOLOR)|(TEXTCOLOR)
{{</message>}}

Example: display README.txt

{{<message>}}
INFOTEXT_FILE|README.txt|"read me"|OK,NO
{{</message>}}

![infotext](/images/infotext.png)

When the display starts, the **INFOTEXT_EVENT_SHOW** message is emitted.

{{<message>}}
INFOTEXT_EVENT_SHOW
{{</message>}}

When the user selects one of the button labels the display ends. At that time **INFOTEXT_EVENT_CLOSE** is emitted together with the label of the pressed button.

{{<message>}}
INFOTEXT_EVENT_CLOSE|(selecteDButtonLabel)
{{</message>}}

## Displaying a String as a Document

Instead of a file, you can provide the content to display directly in a message. Use **INFOTEXT_STRING** in place of **INFOTEXT_FILE**. Specify the string to display as the 1st argument. The 2nd and subsequent arguments work exactly the same as for **INFOTEXT_FILE**.

{{<message>}}
INFOTEXT_STRING|textbody|(titleLabel)|(buttonLabels)|(scale)|(BACKGROUNDCOLOR)|(TEXTCOLOR)
{{</message>}}

As with **INFOTEXT_FILE**, **INFOTEXT_EVENT_SHOW** is emitted when the display starts, and **INFOTEXT_EVENT_CLOSE** when it ends.