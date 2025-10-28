---
title: Browser-based message testing environment
slug: message-test
---
# Browser-based message testing environment

To make development easier, a way to easily try messages via a web browser is provided. With MMDAgent-EX running, open http://localhost:50000/ in a browser on the same machine.

- <a href="http://localhost:50000" target="_blank">http://localhost:50000</a> (opens in a new window when clicked)

The browser connects to the running MMDAgent-EX and opens a page like the following.

<img alt="test message page snapshot" src="/images/test_message.png"/>

You can enter a message in this text box and press the Send button to send any message to the running MMDAgent-EX. Try entering the following [prompt display message](../prompting).

```text
PROMPT_SHOW|"This is test"|Yes|OK|"I got it"
```

Press Send; if a prompt dialog like the following appears, it's working.

<img alt="test message prompt snapshot" src="/images/test_message_prompt.png"/>

This lets you send arbitrary messages to the running MMDAgent-EX at http://localhost:50000/ to verify behavior -- feel free to use it.

## Configuration

You can change the port number in the .mdf. You can also disable this feature.

{{<mdf>}}
# set to false to disable the internal http server feature
http_server=true

# set port number to listen
http_server_port=50000
{{</mdf>}}