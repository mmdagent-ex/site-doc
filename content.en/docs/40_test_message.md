---
title: Browser-based Operational Testing Environment
slug: message-test
---
# Browser interface for testing message

MMDAgent-EX is a messaging system where all the commands and events are managed through messages.  It is best to know MMDAgent-EX by knowing messages practically.

MMDAgent-EX has Web browser interface for instant message posting test.  While MMDAgent-EX is running, open http://localhost:50000/ with a web browser on the same machine.

- <a href="http://localhost:50000" target="_blank">http://localhost:50000</a> (← Click to open in a new window)

The browser will open a page like this:

<img alt="test message page snapshot" src="/images/test_message.png"/>

By typing a message into the text box and pressing the Send button, then the message will be sent to MMDAgent-EX and processed.  You can send any message.

For example, enter the following [message](../prompting) to the text box and send.

```text
PROMPT_SHOW|"This is test"|Yes|OK|"I got it"
```

When you press the Send button, a prompt dialog like the one below appears on MMDAgent-EX.

<img alt="test message prompt snapshot" src="/images/test_message_prompt.png"/>

In this way, you can send any message to the running MMDAgent-EX and check its operation via http://localhost:50000/.

## Configuration 

There are some options in .mdf to configure this feature:

{{<mdf>}}
# set to false to disable the internal http server feature
http_server=true

# set port number to listen
http_server_port=50000
{{</mdf>}}