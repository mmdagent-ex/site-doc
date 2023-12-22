

---
title: Format of PACKAGE_DESC.txt
slug: package-desc-format
---

# Format of PACKAGE_DESC.txt

## Basics

```text
# Specify the mdf file to launch.
# If not specified, it will search the content folder and launch from the .mdf file 
# in the deepest folder hierarchy.
execMDFFile=some/where/foobar.mdf

# The text name to display in bookmarks and history.
# If not specified, the file name will be used.
# If you only write "label=", the text name will not be output.
#label=string

# The image file to display in bookmarks and history.
# It will be displayed together with the above label specification 
# (if label=, it will be image only).
# It is best to create it with an aspect ratio of 7:1, as it will be extended to 7:1.
# If not specified, a file named banner.png will be searched for.
# If banner.png does not exist, the image will not be used.
#image=hoge.png

# Specify the README file you want the content user to read.
# If specified, it will be displayed in full screen when the content is launched for the first time.
# It must be a text file (UTF-8).
#readme=readme.txt

# Specify whether the user is forced to agree after displaying the README file.
# If set to true, two buttons, Accept and Decline, will be displayed at the bottom of the README,
# and you can prevent playback if you press Decline.
# If you set it to true, you must also specify the above readme.
#readmeForceAgreement=true
```

## Security-related

```text
# Disallow browsing in the built-in browser
nonBrowse=true

# Disallow launching on desktop OS (Win/Mac/Linux)
nonDesktop=true
```

## Auto-update related

Automatically update certain files during content playback. At specified intervals, it asks the server of the content source for updates to the specified files, and if there are updates on the server side, it downloads only those files in the background.

Normally, the web content is checked for updates and new differences are downloaded at the timing of content startup. In addition to this, by using this option, you can update any file in the background without stopping the content during content startup.

```text
# Specify the file name to try auto-check for updates and background update.
autoUpdateFiles=xxx.mdf[,xxx.fst,…]

# Specify the interval for automatic checks in seconds
autoUpdatePeriod=20
```

## Data Collection

This setting uploads the logs recorded with the `LOG_START` and `LOG_FINISH` functions to the server. When using, pay close attention to operation so as not to become stealth collection, such as obtaining user consent.

```text
# Enable the function to upload logs to the server.
# Specify the server URL to send.
#logUploadURL=url_string

# Use when specifying the HTTP version string.
# The default is "HTTP/1.1"
#logUploadHTTPVersion=STRING

# Specify the log identification string
# Specify when you want to embed the name and version of the content in the log.
#logIdentifier=string
```

## Plugin_Kafka Related

```text
# Broker address for Apache Kafka logging.
kafkaBroker=host:port

# Partition number of the broker to connect.
kafkaPartition=partition_number

# Producer name to connect. When this option is specified, the app will
# connect to the Kafka server as “producer” at startup, and start
# sending all  #logs to the topic channel at real time.
#
# The app can be either producer or consumer, but not both.
# Do not specify both KafkaProducerTopic and KafkaConsumerTopic.
kafkaProducerTopic=topic_string

# Consumer name to connect. When this option is specified, the app will
# connect to the Kafka server as “consumer” at content startup, and start
# receiving feeded messages from the topic channel and processing them
# at real time.
#
# The app can act either producer or consumer, but not both.
# Do not specify both KafkaProducerTopic and KafkaConsumerTopic.
kafkaConsumerTopic=topic_string

# Compression codec.
kafkaCodec=codec_string
```
